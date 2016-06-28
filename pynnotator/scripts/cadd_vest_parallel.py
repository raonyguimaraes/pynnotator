#!/usr/bin/env python
# -*- coding: utf-8 -*-
#parallel https://code.google.com/p/pysam/issues/detail?id=105


import pp

import pysam
import argparse
from datetime import datetime
import os, shutil
# import shlex, subprocess

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with DbNSFP.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')
parser.add_argument('-n', dest='cores', required=True, metavar='4', help='number of cores to use')

args = parser.parse_args()

dbnfsp_header = '''##INFO=<ID=dbNSFP_VEST3_score,Number=A,Type=Float,Description="VEST 3.0 score. Score ranges from 0 to 1. The larger the score the more likely the mutation may cause functional change. In case there are multiple scores for the same variant, the largest score (most damaging) is presented. Please refer to Carter et al., (2013) BMC Genomics. 14(3) 1-16 for details.">
##INFO=<ID=dbNSFP_VEST3_rankscore,Number=A,Type=Float,Description="VEST3 scores were ranked among all VEST3 scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of VEST3 scores in dbNSFP. The scores range from 0 to 1.">
##INFO=<ID=dbNSFP_CADD_raw,Number=A,Type=Float,Description="CADD raw score for funtional prediction of a SNP. Please refer to Kircher et al. (2014) Nature Genetics 46(3):310-5 for details. The larger the score the more likely the SNP has damaging effect.">
##INFO=<ID=dbNSFP_CADD_raw_rankscore,Number=A,Type=Float,Description="CADD raw scores were ranked among all CADD raw scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of CADD raw scores in dbNSFP">
##INFO=<ID=dbNSFP_CADD_phred,Number=A,Type=Float,Description="CADD phred-like score. This is phred-like rank score based on whole genome CADD raw scores. Please refer to Kircher et al. (2014) Nature Genetics 46(3):310-5 for details. The larger the score the more likely the SNP has damaging effect.">
'''

cores = int(args.cores)
prefix = 'cadd_vest'
if not os.path.exists(prefix):
    os.makedirs(prefix)

def partition(lst, n):
        division = len(lst) / float(n)
        return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n) ]

def splitvcf(vcffile):
    # print 'numero de cores', cores
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

    groups = partition(list(vcf_reader.readlines()), cores)
    for c, group in enumerate(groups):
        # print 'group', len(group)
        # print 'c', c
        part = c + 1
        part_writer = open('%s/part.%s.vcf' % (prefix, part), 'w')
        for line in group:
            part_writer.writelines(line)

def  check_ref_alt(variant, ann):
    #compare REF
    if variant[3] == ann[2]:
        alts = variant[4].split(',')
        alts_ann = ann[3].split(',')
        #compare ALT
        for alt in alts:
            if alt in alts_ann:
                return True
    return False

    #convert and annotate the vcf file to snpeff
def annotate(vcffile, out_prefix, dbnsfp):
    #print 'Hello'
    #print self.dbnfsp_reader
    #header is at:
    # 55 VEST3_score
    # 56  VEST3_rankscore
    # 60  CADD_raw
    # 61  CADD_raw_rankscore
    # 62  CADD_phred: 

    vest_start = 54
    vest_end = 56
    cadd_start = 59 
    cadd_end = 62


    # print 'input',vcffile, out_prefix, dbnsfp 
    dbnfsp_reader = pysam.Tabixfile(dbnsfp)
    header = dbnfsp_reader.header.next().strip().split('\t')

    
    vcf_reader = open('%s' % (vcffile))
    vcf_writer = open('cadd_vest/cadd_vest.%s.vcf' % (out_prefix), 'w')
    
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
                    #this annotated all cadd and vest from dbnfsp2.5
                    # for k, item in enumerate(header[dbnfsp_start:dbnfsp_end]):
                    #     idx = k+dbnfsp_start
                    #     if ann[idx] != '.':
                    #         new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))

                    for k, item in enumerate(header[vest_start:vest_end]):
                        idx = k+vest_start
                        if ann[idx] != '.':
                            new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))
                    for k, item in enumerate(header[cadd_start:cadd_end]):
                        idx = k+cadd_start
                        if ann[idx] != '.':
                            new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))

                    variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
            vcf_writer.writelines("\t".join(variant))
# def annotate(vcffile, index, dbnsfp):
#     print 'vcf', vcffile, index
#     # filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
#     dbnfsp_reader = pysam.Tabixfile(dbnsfp)

splitvcf(args.vcffile)

job_server = pp.Server() 
prefix = 'cadd_vest'
# Define your jobs
jobs = []
final_parts = []
for n in range(0,cores):
    index = n+1
    part = '%s/part.%s.vcf' % (prefix, index)
    job = job_server.submit(annotate, (part, index, dbnsfp), modules=('pysam',))
    final_file = 'cadd_vest/cadd_vest.%s.vcf' % (index)
    final_parts.append(final_file)

    jobs.append(job)
for job in jobs:
    job()


# parts = ['%s/cadd_vest.%s.vcf' % (prefix, index+1) for index in range(0,cores)]
# print parts

command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/cadd_vest.vcf' % (prefix)
os.system(command)
#merge all files 

# job1 = job_server.submit(annotate, ('%s/part.1.vcf' % (prefix), 1, dbnsfp), modules=('pysam',))
# job2 = job_server.submit(annotate, ('%s/part.2.vcf' % (prefix), 2, dbnsfp), modules=('pysam',))
# job3 = job_server.submit(annotate, ('%s/part.3.vcf' % (prefix), 3, dbnsfp), modules=('pysam',))
# job4 = job_server.submit(annotate, ('%s/part.4.vcf' % (prefix), 4, dbnsfp), modules=('pysam',))

# # Compute and retrieve answers for the jobs.
# job1()
# job2()
# job3()
# job4()