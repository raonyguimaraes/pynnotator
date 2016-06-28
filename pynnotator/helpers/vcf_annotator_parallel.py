#!/usr/bin/env python
# -*- coding: utf-8 -*-
#parallel https://code.google.com/p/pysam/issues/detail?id=105
#Running from tests
#python ../scripts/vcf_annotator_parallel.py 
#-n 8 
#-i ../samples/sample.1000.vcf 
#-r 1000genomes dbsnp clinvar esp6500 
#-a ../data/1000genomes/ALL.autosomes.phase3_shapeit2_mvncall_integrated_v5.20130502.sites.vcf.gz ../data/dbsnp/00-All.vcf.gz ../data/dbsnp/clinvar-latest.vcf.gz ../data/esp6500/esp6500si.vcf.gz


import pp

import pysam
import argparse
from datetime import datetime
import os, shutil
import gzip
# import shlex, subprocess

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with DbNSFP.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')
parser.add_argument('-r', dest='resources', required=True, metavar='1000genomes', nargs='+', help='string to be added to annotated fields')
parser.add_argument('-a', dest='annfiles', required=True, metavar='1000genomes.vcf.gz', nargs='+', help='a VCF file to use for annotation')
parser.add_argument('-n', dest='cores', required=True, metavar='4', help='number of cores to use')

args = parser.parse_args()

toolname = 'pynnotator'

cores = int(args.cores)
prefix = 'pynnotator'
if not os.path.exists(prefix):
    os.makedirs(prefix)

def partition(lst, n):
        division = len(lst) / float(n)
        return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n) ]

def splitvcf(vcffile, annheader):
    # print 'numero de cores', cores
    vcf_reader = open('%s' % (vcffile))
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
def annotate(vcffile, out_prefix, dbnsfp, args):

    resources = args.resources
    annfiles = {}
    for n, value in enumerate(args.annfiles):
        annfiles[n] = {}
        annfiles[n]['resource'] = args.resources[n]
        annfiles[n]['file'] = value
        annfiles[n]['reader'] = pysam.Tabixfile(annfiles[n]['file'])

    
    
    vcflist = []
    #read first vcf to be annotated
    # print 'vcffile', vcffile
    vcffile = open('%s' % (vcffile), 'r')

    outvcffile = open('pynnotator/pynnotator.%s.vcf' % (out_prefix), 'w')

    for line in vcffile:
        if not line.startswith('#'):
            
            variant = line.split('\t')
            variant[0] = variant[0].replace('chr', '')
            index = '%s-%s' % (variant[0], variant[1])
            # print 'index', index

            for key, annfile in annfiles.items():
                # vcf_reader = vcf.Reader(filename=annfile['file'])
                try:
                    records = annfiles[key]['reader'].fetch(variant[0], int(variant[1])-1, int(variant[1]))
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
                            new_ann.append('%s.%s' % (resources[key], k))
                        variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
                    #add rs_ID
                    if resources[key] == 'dbsnp':
                        variant[2] = row[2]


            outvcffile.writelines("\t".join(variant))
    
    #END OF VCF_ANNOTATOR

annfiles = {}
for n, value in enumerate(args.annfiles):
    annfiles[n] = {}
    annfiles[n]['resource'] = args.resources[n]
    annfiles[n]['file'] = value
    annfiles[n]['reader'] = pysam.Tabixfile(annfiles[n]['file'])

ann_dict = {}
annheader = {}
for key, annfile in annfiles.items():
    #print key, annfile
    annfile = gzip.open(annfile['file'],'r')
    ann_dict[key] = {}
    annheader[key] = []
    for line in annfile:
        if line.startswith('#'):
            if line.startswith('##INFO'):
                row = line.split('=')
                row[2] = '%s.%s' % (args.resources[key], row[2])
                info = "=".join(row)
                annheader[key].append(info)
        else:
            break

splitvcf(args.vcffile, annheader)

job_server = pp.Server() 
prefix = 'pynnotator'
# Define your jobs
jobs = []
final_parts = []
for n in range(0,cores):
    index = n+1
    part = '%s/part.%s.vcf' % (prefix, index)
    
    job = job_server.submit(annotate, (part, index, dbnsfp,args), modules=('pysam','gzip'))
    jobs.append(job)
    final_file = 'pynnotator/pynnotator.%s.vcf' % (index)
    final_parts.append(final_file)

for job in jobs:
    job()


# parts = ['%s/cadd_vest.%s.vcf' % (prefix, index+1) for index in range(0,cores)]
# print parts

command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/pynnotator.vcf' % (prefix)
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