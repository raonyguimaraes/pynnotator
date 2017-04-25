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


# cores = int(args.cores)
# prefix = 'func_pred'
# if not os.path.exists(prefix):
#     os.makedirs(prefix)

class FUNC_PRED_Annotator(object):

    def __init__(self, vcf_file=None, cores=None):
        
        self.vcf_file = vcf_file
        self.dbnfsp_header = open('%s/dbnsfp/header.vcf' % (settings.data_dir)).readlines()


        # print('self.resources', self.resources)
        self.cores = int(cores)

        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
        #create folder validator if it doesn't exists
        if not os.path.exists('func_pred'):
            os.makedirs('func_pred')

    def run(self):

        tstart = datetime.now()

        print(tstart, 'Starting func pred annotator: ', self.vcf_file)
        
        # std = self.annotator()

        self.splitvcf(self.vcf_file)

        pool = mp.Pool()
        pool.map(self.annotate, range(1,self.cores+1))
        # pool.close()
        # pool.join()

        prefix = 'func_pred'
        # # Define your jobs
        # jobs = []
        final_parts = []
        for n in range(0,self.cores):
            index = n+1
            final_file = 'func_pred/func_pred.%s.vcf' % (index)
            final_parts.append(final_file)
        
        command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/func_pred.vcf' % (prefix)
        std = os.system(command)

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished func pred, it took: ', annotation_time)


    def partition(self, lst, n):
            division = len(lst) / float(n)
            return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n) ]

    def splitvcf(self, vcffile):
        # print('split file', vcffile)
        # print 'numero de cores', cores
        prefix = 'func_pred'
        vcf_reader = open('%s' % (vcffile))
        header_writer = open('%s/header.vcf' % (prefix), 'w')
        body_writer = open('%s/body.vcf' % (prefix), 'w')
        
        count_lines = 0
        for line in vcf_reader:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    header_writer.writelines(self.dbnfsp_header)
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
        
        # 24    SIFT_score: SIFT score (SIFTori).
        # 105 HUVEC_confidence_value: 0 - highly significant scores (approx. p<.003); 1 - significant scores

        #188   clinvar_rs: rs number from the clinvar data set
        #191 clinvar_golden_stars: ClinVar Review Status summary.
        
        func_pred_start = 23
        func_pred_end = 105
        
        clinvar_start = 187
        clinvar_end = 191


        # print 'input',vcffile, out_prefix, dbnsfp 
        dbnfsp_reader = pysam.Tabixfile(settings.dbnsfp, 'r')
        
        # print('header')
        for item in dbnfsp_reader.header:
            header = item.decode('utf-8').strip().split('\t')

        # header = dbnfsp_reader.header.next().strip().split('\t')

        vcffile = 'func_pred/part.%s.vcf' % (out_prefix)

        vcf_reader = open('%s' % (vcffile))
        vcf_writer = open('func_pred/func_pred.%s.vcf' % (out_prefix), 'w')
        
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
                        
                        for k, item in enumerate(header[func_pred_start:func_pred_end]):
                            idx = k+func_pred_start
                            if ann[idx] != '.':
                                new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))

                        for k, item in enumerate(header[clinvar_start:clinvar_end]):
                            idx = k+clinvar_start
                            if ann[idx] != '.':
                                new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|').replace(' ', '_')))

                        variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
                vcf_writer.writelines("\t".join(variant))


if  __name__ == '__main__' :
    
    
    parser = argparse.ArgumentParser(description='Annotate a VCF File with DbNSFP.')

    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    parser.add_argument('-n', dest='cores', required=True, metavar='4', help='number of cores to use')

    args = parser.parse_args()

    func_pred = FUNC_PRED_Annotator(args.vcf_file, args.cores)
    func_pred.run()



# def annotate(vcffile, index, dbnsfp):
#     print 'vcf', vcffile, index
#     # filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
#     dbnfsp_reader = pysam.Tabixfile(dbnsfp)

# splitvcf(args.vcffile)

# # job_server = pp.Server()
# prefix = 'func_pred'
# # Define your jobs
# jobs = []
# final_parts = []
# for n in range(0,cores):
#     index = n+1
#     part = '%s/part.%s.vcf' % (prefix, index)
    
#     job = Process(target=annotate, args=(part, index, args.dbnsfp))
#     final_file = 'func_pred/func_pred.%s.vcf' % (index)
#     final_parts.append(final_file)
#     jobs.append(job)


# for job in jobs:
#     job.start()

# for job in jobs:
#     job.join()

# command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/func_pred.vcf' % (prefix)
# os.system(command)
# #merge all files 
