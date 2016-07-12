#!/usr/bin/python
# -*- coding: utf-8 -*-
#test vcf annotation in parallel on python 3

import pysam

import multiprocessing as mp
import argparse
import os
import gzip
from datetime import datetime


class VCF_Annotator(object):
    def __init__(self, vcf_file=None, ann_files=None, resources=None, cores=None):
        
        self.vcf_file = vcf_file

        self.ann_files = ann_files
        # print('self.ann_files', self.ann_files)

        self.resources = resources 
        # print('self.resources', self.resources)
        self.cores = int(cores)

        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
        #create folder validator if it doesn't exists
        if not os.path.exists('pynnotator'):
            os.makedirs('pynnotator')

        ann_dict = {}
        self.annheader = {}

        for key, annfile in enumerate(self.ann_files):
            annfile = gzip.open(annfile,'rt')
            ann_dict[key] = {}
            self.annheader[key] = []
            for line in annfile:
                if line.startswith('#'):
                    if line.startswith('##INFO'):
                        row = line.split('=')
                        #this treats HGMD-PUBLIC_20152
                        row[2] = row[2].replace('HGMD-', 'HGMD_')

                        row[2] = '%s.%s' % (self.resources[key], row[2])
                        info = "=".join(row)
                        self.annheader[key].append(info)
                else:
                    break

    def run(self):

        tstart = datetime.now()

        print(tstart, 'Starting vcf annotator: ', self.vcf_file)
        
        # std = self.annotator()

        self.splitvcf(self.vcf_file, self.annheader)

        pool = mp.Pool()
        pool.map(self.annotate, range(1,self.cores+1))
        # pool.close()
        # pool.join()

        prefix = 'pynnotator'
        # # Define your jobs
        # jobs = []
        final_parts = []
        for n in range(0,self.cores):
            index = n+1
            final_file = 'pynnotator/pynnotator.%s.vcf' % (index)
            final_parts.append(final_file)
        
        command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/pynnotator.vcf' % (prefix)
        std = os.system(command)

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished vcf annotator, it took: ', annotation_time)

    def partition(self, lst, n):
        division = len(lst) / float(n)
        return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n) ]

    def splitvcf(self, vcf_file, annheader):
        # print 'numero de cores', cores
        prefix = 'pynnotator'
        vcf_reader = open('%s' % (vcf_file))
        header_writer = open('%s/header.vcf' % (prefix), 'w')
        body_writer = open('%s/body.vcf' % (prefix), 'w')
        
        count_lines = 0
        for line in vcf_reader:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    for key in annheader:
                        header_writer.writelines(annheader[key])
                header_writer.writelines(line)
            else:
                body_writer.writelines(line)
        header_writer.close()
        body_writer.close()
        
        vcf_reader = open('%s/body.vcf' % (prefix))

        groups = self.partition(list(vcf_reader.readlines()), self.cores)
        for c, group in enumerate(groups):
            # print 'group', len(group)
            # print 'c', c
            part = c + 1
            part_writer = open('%s/part.%s.vcf' % (prefix, part), 'w')
            for line in group:
                part_writer.writelines(line)
            part_writer.close()

    #convert and annotate the vcf file to snpeff
    def annotate(self, out_prefix):

        # print('out_prefix', out_prefix)

        annfiles = {}

        for n, value in enumerate(self.ann_files):
            annfiles[n] = {}
            annfiles[n]['resource'] = self.resources[n]
            annfiles[n]['file'] = value
            annfiles[n]['reader'] = pysam.Tabixfile(annfiles[n]['file'],encoding="utf-8")

         
        vcf_file = 'pynnotator/part.%s.vcf' % (out_prefix)

        vcflist = []
        #read first vcf to be annotated
        # print 'vcf_file', vcf_file
        vcf_file = open('%s' % (vcf_file), 'r')

        outvcf_file = open('pynnotator/pynnotator.%s.vcf' % (out_prefix), 'w')

        for line in vcf_file:
            if not line.startswith('#'):
                
                variant = line.split('\t')
                variant[0] = variant[0].replace('chr', '')
                index = '%s-%s' % (variant[0], variant[1])
                # print 'index', index

                for key, annfile in annfiles.items():
                    # vcf_reader = vcf.Reader(filename=annfile['file'])
                    try:
                        records = annfiles[key]['reader'].fetch(variant[0], int(variant[1])-1, int(variant[1]))
                    except:
                        records = []
                        
                    for record in records:

                        row = record.split('\t')
                        
                        #compare REF and ALT Columns to check if they are the same
                        #ex. G C can also be C G in another VCF
                        #ex2. G C,A should match also G A and G C

                        check_flag = False
                        if variant[3] == row[3]:
                            alts = variant[4].split(',')
                            alts_row = row[4].split(',')
                            #compare ALT
                            for alt in alts:
                                if alt in alts_row:
                                    check_flag = True

                        if check_flag:

                            info = row[7].split(';')
                            new_ann = []
                            for k in info:

                                #treat k for snpsift
                                # k = k.replace('=)',')')
                                # k = k.replace('http://www.ncbi.nlm.nih.gov/pubmed?term=','PMID')
                                #remove equal signs (for snpsift)
                                # = for %3D
                                if k.count('=') > 1:
                                    new_string = k.split('=', 1)
                                    # print(new_string)
                                    new_string[1] = new_string[1].replace('=', '')
                                    k = '%s=%s' % (new_string[0], new_string[1])
                                    # print(k)
                                k = k.replace('HGMD-', 'HGMD_')
                                new_ann.append('%s.%s' % (self.resources[key], k))

                            variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
                        #add rs_ID
                        if self.resources[key] == 'dbsnp':
                            variant[2] = row[2]


                outvcf_file.writelines("\t".join(variant))


if  __name__ == '__main__' :
    
    parser = argparse.ArgumentParser(description='Annotate a VCF File with multiple VCFs.')

    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')
    parser.add_argument('-r', dest='resources', required=True, metavar='1000genomes', nargs='+', help='string to be added to annotated fields')
    parser.add_argument('-a', dest='ann_files', required=True, metavar='1000genomes.vcf.gz', nargs='+', help='a VCF file to use for annotation')
    parser.add_argument('-n', dest='cores', required=True, metavar='4', help='number of cores to use')

    args = parser.parse_args()

    vcf_annotator = VCF_Annotator(args.vcf_file, args.ann_files, args.resources, args.cores)    
    vcf_annotator.run()

