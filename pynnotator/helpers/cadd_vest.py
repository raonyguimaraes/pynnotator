#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pysam
import argparse
from datetime import datetime
import os, shutil
# import shlex, subprocess

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with DbNSFP.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

args = parser.parse_args()

dbnfsp_header = '''##INFO=<ID=dbNSFP_VEST3_score,Number=A,Type=Float,Description="VEST 3.0 score. Score ranges from 0 to 1. The larger the score the more likely the mutation may cause functional change. In case there are multiple scores for the same variant, the largest score (most damaging) is presented. Please refer to Carter et al., (2013) BMC Genomics. 14(3) 1-16 for details.">
##INFO=<ID=dbNSFP_VEST3_rankscore,Number=A,Type=Float,Description="VEST3 scores were ranked among all VEST3 scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of VEST3 scores in dbNSFP. The scores range from 0 to 1.">
##INFO=<ID=dbNSFP_CADD_raw,Number=A,Type=Float,Description="CADD raw score for funtional prediction of a SNP. Please refer to Kircher et al. (2014) Nature Genetics 46(3):310-5 for details. The larger the score the more likely the SNP has damaging effect.">
##INFO=<ID=dbNSFP_CADD_raw_rankscore,Number=A,Type=Float,Description="CADD raw scores were ranked among all CADD raw scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of CADD raw scores in dbNSFP">
##INFO=<ID=dbNSFP_CADD_phred,Number=A,Type=Float,Description="CADD phred-like score. This is phred-like rank score based on whole genome CADD raw scores. Please refer to Kircher et al. (2014) Nature Genetics 46(3):310-5 for details. The larger the score the more likely the SNP has damaging effect.">
'''

dbnfsp_start = 54 # this is the index where to start annotating
dbnfsp_end = 62 # this is the index where to finish annotating

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

class Dbnsfp(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        self.dbnfsp_reader = pysam.Tabixfile(dbnsfp)
        self.header = self.dbnfsp_reader.header.next().strip().split('\t')
        
        # print 'test'
        # for item in self.dbnfsp_reader.header:
        #     print 'item',item
        #     #self.header.append(item)
        #print self.header
        
        #create folder snpeff if it doesn't exists
        if not os.path.exists('cadd_vest'):
            os.makedirs('cadd_vest')
        #enter inside folder
        # os.chdir('cadd_vest')
        
    
    def run(self):
        tstart = datetime.now()
        print tstart, 'Starting cadd_vest annotation: ', self.vcffile
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print tend, 'Finished cadd_vest annotation, it took: ', annotation_time        
    def check_ref_alt(self, variant, ann):
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
    def annotate(self):
        #print 'Hello'
        #print self.dbnfsp_reader
        vcf_reader = open('%s' % (self.vcffile))
        vcf_writer = open('cadd_vest/cadd_vest.vcf', 'w')
        
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
                    records = self.dbnfsp_reader.fetch(variant[0], int(variant[1])-1, int(variant[1]))
                except:
                    records = []
                for record in records:
                    ann = record.strip().split('\t')

                    if self.check_ref_alt(variant, ann):
                        new_ann = []
                        #this annotated all cadd and vest from dbnfsp2.9
                        for k, item in enumerate(self.header[vest_start:vest_end]):
                            idx = k+vest_start
                            if ann[idx] != '.':
                                new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))
                        for k, item in enumerate(self.header[cadd_start:cadd_end]):
                            idx = k+cadd_start
                            if ann[idx] != '.':
                                new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))


                        variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
                vcf_writer.writelines("\t".join(variant))
                    


if  __name__ == '__main__' :
    dbnsfp = Dbnsfp(args.vcffile)
    dbnsfp.run()