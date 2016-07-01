#!/usr/bin/env python
# -*- coding: utf-8 -*-
#parallel https://code.google.com/p/pysam/issues/detail?id=105


# import pp

import multiprocessing as mp

import pysam
import argparse

from datetime import datetime
import os, shutil
# import shlex, subprocess
from pynnotator import settings

dbnfsp_header = '''##INFO=<ID=dbNSFP_DANN_score,Number=A,Type=Float,Description="DANN is a functional prediction score retrained based on the training data     of CADD using deep neural network. Scores range from 0 to 1. A larger number indicate a higher probability to be damaging. More information of this score can be found in doi: 10.1093/bioinformatics/btu703.">
##INFO=<ID=dbNSFP_DANN_rankscore,Number=A,Type=Float,Description="DANN scores were ranked among all DANN scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of DANN scores in dbNSFP">
##INFO=<ID=dbNSFP_CADD_raw,Number=A,Type=Float,Description="CADD raw score for funtional prediction of a SNP. Please refer to Kircher et al. (2014) Nature Genetics 46(3):310-5 for details. The larger the score the more likely the SNP has damaging effect.">
##INFO=<ID=dbNSFP_CADD_raw_rankscore,Number=A,Type=Float,Description="CADD raw scores were ranked among all CADD raw scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of CADD raw scores in dbNSFP">
##INFO=<ID=dbNSFP_CADD_phred,Number=A,Type=Float,Description="CADD phred-like score. This is phred-like rank score based on whole genome CADD raw scores. Please refer to Kircher et al. (2014) Nature Genetics 46(3):310-5 for details. The larger the score the more likely the SNP has damaging effect.">
'''

# cores = int(args.cores)
# prefix = 'cadd_dann'
# if not os.path.exists(prefix):
#     os.makedirs(prefix)

class CADD_DANN_Annotator(object):

    def __init__(self, vcf_file=None, cores=None):
        
        self.vcf_file = vcf_file

        # print('self.resources', self.resources)
        self.cores = int(cores)

        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
        #create folder validator if it doesn't exists
        if not os.path.exists('cadd_dann'):
            os.makedirs('cadd_dann')

    def run(self):

        tstart = datetime.now()

        print(tstart, 'Starting cadd dann annotator: ', self.vcf_file)
        
        # std = self.annotator()

        self.splitvcf(self.vcf_file)

        pool = mp.Pool()
        pool.map(self.annotate, range(1,self.cores+1))
        # pool.close()
        # pool.join()

        prefix = 'cadd_dann'
        # # Define your jobs
        # jobs = []
        final_parts = []
        for n in range(0,self.cores):
            index = n+1
            final_file = 'cadd_dann/cadd_dann.%s.vcf' % (index)
            final_parts.append(final_file)
        
        command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/cadd_dann.vcf' % (prefix)
        std = os.system(command)

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished vcf annotator, it took: ', annotation_time)


    def partition(self, lst, n):
            division = len(lst) / float(n)
            return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n) ]

    def splitvcf(self, vcffile):
        # print('split file', vcffile)
        # print 'numero de cores', cores
        prefix = 'cadd_dann'
        vcf_reader = open('%s' % (vcffile))
        header_writer = open('%s/header.vcf' % (prefix), 'w')
        body_writer = open('%s/body.vcf' % (prefix), 'w')
        
        count_lines = 0
        for line in vcf_reader:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    header_writer.writelines(dbnfsp_header)
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
        #print 'Hello'
        #print self.dbnfsp_reader
        #header is at:
        # 67      CADD_raw: 
        # 68      CADD_raw_rankscore: 
        # 69      CADD_phred: 
        
        # 70      DANN_score: 
        # 71      DANN_rankscore: 
        dann_start = 69
        dann_end = 71
        cadd_start = 66 
        cadd_end = 69


        # print 'input',vcffile, out_prefix, dbnsfp 
        dbnfsp_reader = pysam.Tabixfile(settings.dbnsfp, 'r')
        
        # print('header')
        for item in dbnfsp_reader.header:
            header = item.decode('utf-8').strip().split('\t')

        # header = dbnfsp_reader.header.next().strip().split('\t')

        vcffile = 'cadd_dann/part.%s.vcf' % (out_prefix)

        vcf_reader = open('%s' % (vcffile))
        vcf_writer = open('cadd_dann/cadd_dann.%s.vcf' % (out_prefix), 'w')
        
        for line in vcf_reader:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    vcf_writer.writelines(dbnfsp_header)
                vcf_writer.writelines(line)
            else:
                variant = line.split('\t')
                variant[0] = variant[0].replace('chr', '')
                index = '%s-%s' % (variant[0], variant[1])
                #print index
                try:
                    records = dbnfsp_reader.fetch(variant[0], int(variant[1])-1, int(variant[1]))
                except:
                    records = []
                    
                for record in records:
                    ann = record.strip().split('\t')

                    ispresent = False
                    if variant[3] == ann[2]:
                        alts = variant[4].split(',')
                        alts_ann = ann[3].split(',')
                        #compare ALT
                        for alt in alts:
                            if alt in alts_ann:
                                ispresent = True

                    if ispresent:
                        new_ann = []
                        #this annotated all cadd and dann from dbnfsp2.5
                        # for k, item in enumerate(header[dbnfsp_start:dbnfsp_end]):
                        #     idx = k+dbnfsp_start
                        #     if ann[idx] != '.':
                        #         new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))

                        for k, item in enumerate(header[dann_start:dann_end]):
                            idx = k+dann_start
                            if ann[idx] != '.':
                                new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))
                        for k, item in enumerate(header[cadd_start:cadd_end]):
                            idx = k+cadd_start
                            if ann[idx] != '.':
                                new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))

                        variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
                vcf_writer.writelines("\t".join(variant))


if  __name__ == '__main__' :
    
    
    parser = argparse.ArgumentParser(description='Annotate a VCF File with DbNSFP.')

    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    parser.add_argument('-n', dest='cores', required=True, metavar='4', help='number of cores to use')

    args = parser.parse_args()

    cadd_dann = CADD_DANN_Annotator(args.vcf_file, args.cores)
    cadd_dann.run()



# def annotate(vcffile, index, dbnsfp):
#     print 'vcf', vcffile, index
#     # filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
#     dbnfsp_reader = pysam.Tabixfile(dbnsfp)

# splitvcf(args.vcffile)

# # job_server = pp.Server()
# prefix = 'cadd_dann'
# # Define your jobs
# jobs = []
# final_parts = []
# for n in range(0,cores):
#     index = n+1
#     part = '%s/part.%s.vcf' % (prefix, index)
    
#     job = Process(target=annotate, args=(part, index, args.dbnsfp))
#     final_file = 'cadd_dann/cadd_dann.%s.vcf' % (index)
#     final_parts.append(final_file)
#     jobs.append(job)


# for job in jobs:
#     job.start()

# for job in jobs:
#     job.join()

# command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/cadd_dann.vcf' % (prefix)
# os.system(command)
# #merge all files 
