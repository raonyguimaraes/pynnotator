#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
import csv

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with Annovar.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

parser.add_argument('--log', help='write output to a log file')

args = parser.parse_args()
# print 'args: ', args
humandb_dir = '%s/humandb' % (annovar_dir)

class Annovar(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        
        #create folder annovar if it doesn't exists
        if not os.path.exists('annovar'):
            os.makedirs('annovar')
        
    
    def run(self):
        
        tstart = datetime.now()
        print tstart, 'Starting Annovar annotation: ', self.vcffile

        self.annotate()
        self.parse()

        tend = datetime.now()
        diff = tend - tstart
        print tend, 'Annovar annotation finished! It took: %s' % (diff)


    #convert and annotate the vcf file to annovar
    def annotate(self):
        
        # if self.logfile != '':
        #     logstring = "2>>annovar/%s" % self.logfile
        # else:
        #     logstring = ''
        
        command = "%s/convert2annovar.pl --format vcf4 --includeinfo %s > annovar/%s.annovar" % (annovar_dir, self.vcffile, self.filename)
        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)
        # , 
        #     stdout=log_file, 
        #     stderr=log_file
        if p == 0:
            print 'This vcf was successfully converted to annovar format'
        else:
            print 'Sorry this vcf could not be converted to annovar format'


        # if self.logfile != '':
        #     logstring = "2>>annovar/%s" % self.logfile
        # else:
        #     logstring = ''

        command = '%s/table_annovar.pl \
            annovar/%s.annovar %s -buildver hg19 -out annovar/%s -remove \
            -protocol refGene,phastConsElements46way,genomicSuperDups,esp6500si_all,1000g2012apr_all,ljb2_all,cosmic65,avsift \
            -operation g,r,r,f,f,f,f,f \
            -csvout' %(annovar_dir, self.filename, humandb_dir, self.filename)
            #2>table_annovar.log
        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)
        # , 
        #     stdout=log_file, 
        #     stderr=log_file
        if p == 0:
            print 'Annovar Finished annotating with Success!'
        else:
            print 'Sorry there was an error running annovar'

    #convert a csv file from annovar to vcf
    def parse(self):
        #choosen ones
        selectedtags = ['Func.refGene', 'Gene.refGene', 'ExonicFunc.refGene', 'AAChange.refGene', 'phastConsElements46way', 'genomicSuperDups', 'esp6500si_all', '1000g2012apr_all', 'LJB2_SIFT', 'LJB2_PolyPhen2_HDIV', 'LJB2_PP2_HDIV_Pred', 'LJB2_PolyPhen2_HVAR', 'LJB2_PolyPhen2_HVAR_Pred', 'LJB2_LRT', 'LJB2_LRT_Pred', 'LJB2_MutationTaster', 'LJB2_MutationTaster_Pred', 'LJB_MutationAssessor', 'LJB_MutationAssessor_Pred', 'LJB2_FATHMM', 'LJB2_GERP++', 'LJB2_PhyloP', 'LJB2_SiPhy', 'cosmic65', 'avsift']

        #read annovar results into an array
        annovar_output_file =  "annovar/%s.hg19_multianno.csv" % (self.filename)

        if os.path.isfile(annovar_output_file):
            annovar_file = csv.reader(open(annovar_output_file, "rb"))
            header = annovar_file.next()
            #print header
            #read all data into variants dict
            variants = {}
            for line in annovar_file:
                variant = {}

                for tag in selectedtags:
                  # ltag = tag.lower()
                    variant[tag] = line[header.index(tag)].replace(';', '|')
                
                #get the indexes for chr and position, it works!
                chr_index = header.index('Chr')
                pos_index = chr_index+1

                variant_id = "%s-%s" % (line[chr_index], line[pos_index])
                variants[variant_id] = variant
               
            #print len(variants)
            # print 'annovar debug'
            vcf_file_reader=open(self.vcffile, 'r')
            #out_file=open('%s' % (options.vcf_output), 'w')
            vcf_full=open('annovar/annovar.vcf', 'w')

            for line in vcf_file_reader:
                if line.startswith('#'):
                    # info_tag = line.split(',')[0]
                    #add annovar tags before #CHROM
                    if line.startswith('#CHROM'):
                        ann_vcf_header = []
                        for tag in selectedtags:
                            ann_vcf_header.append('##INFO=<ID=%s,Number=.,Type=String,Description="%s">\n' % (tag.replace('.', '_'), tag))
                        vcf_full.writelines("".join(ann_vcf_header))
                        vcf_full.writelines(line)
                    else:
                        vcf_full.writelines(line)
                     
                else:
                    
                    line = line.split('\t')
                    
                    string_full_annotation = ''

                    variant_id = "%s-%s" % (line[0], line[1])

                    if variant_id in variants:
                        annotation_list = []
                        for tag in selectedtags:
                            # print variants[variant_id]
                            if variants[variant_id][tag] != '':
                                tag_key = tag.replace('.', '_')
                                tag_value = variants[variant_id][tag].replace(' ', '_').replace('=', ':')
                                tag_string = '%s=%s' % (tag_key, tag_value)
                                annotation_list.append(tag_string)
                                # string_full_annotation += 
                        annotations_string = ";".join(annotation_list)
                        line[7] = '%s;%s' % (line[7], annotations_string)
                        # print line
                        vcf_full.writelines("\t".join(line))
                    else:
                        vcf_full.writelines("\t".join(line))

            vcf_full.close()
          
     
if  __name__ == '__main__' :
    annovar = Annovar(args.vcffile)
    annovar.run()