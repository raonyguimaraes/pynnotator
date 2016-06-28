# -*- coding: utf-8 -*-

#this script can annotate one VCF using multiple VCFs files that are compressed and indexed
#bgzip dbsnp138.vcf
#tabix -p vcf dbsnp138.vcf.gz

#python ../scripts/vcf_annotator.py 
#-i mm13173_14.ug.target1.vcf 
#-r 1000genomes dbsnp clinvar esp6500 
#-a ../data/1000genomes/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz ../data/dbsnp138/00-All.vcf.gz ../data/dbsnp138/clinvar_00-latest.vcf.gz ../data/ESP6500/ESP6500.vcf.gz

from settings import *

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
import gzip
import pysam

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with multiple VCFs')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')
parser.add_argument('-r', dest='resources', required=True, metavar='1000genomes', nargs='+', help='string to be added to annotated fields')
parser.add_argument('-a', dest='annfiles', required=True, metavar='1000genomes.vcf.gz', nargs='+', help='a VCF file to use for annotation')

args = parser.parse_args()

toolname = 'pyannotator'

class Genomes1k(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        #base_dir = os.path.dirname(os.path.realpath(__file__))

        self.resources = args.resources

        self.annfiles = {}
        for n, value in enumerate(args.annfiles):
            self.annfiles[n] = {}
            self.annfiles[n]['resource'] = args.resources[n]
            self.annfiles[n]['file'] = value
            self.annfiles[n]['reader'] = pysam.Tabixfile(self.annfiles[n]['file'])
            # vcf.Reader(filename=)


        self.filename = os.path.splitext(os.path.basename(str(self.vcffile)))[0]
        
        #create folder 1000genomes if it doesn't exists
        if not os.path.exists('pynnotator'):
            os.makedirs('pynnotator')
        #enter inside folder, why?
        # os.chdir('pyannotator')

    
    def run(self):
        tstart = datetime.now()
        print tstart, 'Starting annotation: ', self.vcffile
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print tend, 'Finished annotation, it took: ', annotation_time        
    def check_ref_alt(self, variant, row):
        #compare REF
        if variant[3] == row[3]:
            alts = variant[4].split(',')
            alts_row = row[4].split(',')
            #compare ALT
            for alt in alts:
                if alt in alts_row:
                    return True
        return False

    #Annotate a VCF file with another VCF file
    def annotate(self):

        # for key, annfile in self.annfiles.items():

        ann_dict = {}
        annheader = {}
        for key, annfile in self.annfiles.items():
            #print key, annfile
            annfile = gzip.open(annfile['file'],'r')
            ann_dict[key] = {}
            annheader[key] = []
            for line in annfile:
                if line.startswith('#'):
                    if line.startswith('##INFO'):
                        row = line.split('=')
                        row[2] = '%s.%s' % (self.resources[key], row[2])
                        info = "=".join(row)
                        annheader[key].append(info)
                else:
                    break
        
        vcflist = []
        #read first vcf to be annotated
        vcffile = open('%s' % (self.vcffile), 'r')
        outvcffile = open('pynnotator/pynnotator.vcf', 'w')

        for line in vcffile:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    for key in annheader:
                        outvcffile.writelines(annheader[key])
                outvcffile.writelines(line)
                
            else:
                variant = line.split('\t')
                variant[0] = variant[0].replace('chr', '')
                index = '%s-%s' % (variant[0], variant[1])
                # print 'index', index

                for key, annfile in self.annfiles.items():
                    # vcf_reader = vcf.Reader(filename=annfile['file'])
                    try:
                        records = self.annfiles[key]['reader'].fetch(variant[0], int(variant[1])-1, int(variant[1]))
                        # if variant[1] in ['103059260', '103182605']:
                        #     print 'achou! ', records
                        #     for record in records:
                        #         print record
                        #         row = record.split('\t')
                        #         print row

                    except:
                        records = []
                    for record in records:

                        row = record.split('\t')
                        
                        #compare REF and ALT Columns to check if they are the same
                        #ex. G C can also be C G in another VCF
                        #ex2. G C,A should match also G A and G C
                                                    
                        if self.check_ref_alt(variant, row):

                            info = row[7].split(';')
                            new_ann = []
                            for k in info:
                                new_ann.append('%s.%s' % (self.resources[key], k))
                            variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
                        #add rs_ID
                        if self.resources[key] == 'dbsnp':
                            variant[2] = row[2]


                outvcffile.writelines("\t".join(variant))

if  __name__ == '__main__' :
    genomes1k = Genomes1k(args.vcffile)
    genomes1k.run()