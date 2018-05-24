#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import pysam
from collections import OrderedDict
from datetime import datetime

from pynnotator import settings

toolname = 'merge'


class Merge(object):
    def __init__(self, vcffile=None):

        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        self.header = open('%s/scripts/header.vcf' % (settings.BASE_DIR)).readlines()

        # create folder merge if it doesn't exists
        if not os.path.exists('merge'):
            os.makedirs('merge')
        # enter inside folder
        os.chdir('merge')

        self.annotation_files = OrderedDict()

        pysam.tabix_index('../snpeff/snpeff.output.vcf', preset='vcf')

        self.annotation_files['snpeff'] = {
            'info': 'EFF',
            'file': pysam.Tabixfile('../snpeff/snpeff.output.vcf.gz', 'r', encoding="utf-8")
        }

        pysam.tabix_index('../vep/vep.output.sorted.vcf', preset='vcf')

        self.annotation_files['vep'] = {
            'info': 'CSQ',
            'file': pysam.Tabixfile('../vep/vep.output.sorted.vcf.gz', 'r', encoding="utf-8")
        }

        pysam.tabix_index('../snpsift/snpsift.final.vcf', preset='vcf')

        self.annotation_files['vartype'] = {
            'info': 'VARTYPE,SNP,MNP,INS,DEL,MIXED,HOM,HET',
            'file': pysam.Tabixfile('../snpsift/snpsift.final.vcf.gz', 'r', encoding="utf-8")
        }

        self.dbsnp = pysam.Tabixfile(settings.dbsnp, 'r', encoding="utf-8")

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting merge: ', self.vcffile)

        self.merge()

        tend = datetime.now()
        annotation_time = tend - tstart
        print(tend, 'Finished merge, it took: ', annotation_time)

        # merge VCF Files with VariantAnnotator

    def merge(self):

        BASE_DIR = os.getcwd()

        # get headers from files
        headers = []
        for annotation in self.annotation_files:
            # print(annotation, self.annotation_files[annotation])
            info = self.annotation_files[annotation]['info'].split(',')
            # print(info)
            ann_vcf_file = self.annotation_files[annotation]['file']

        output = open('annotation.final.vcf', 'w')
        input_vcf = open(self.vcffile)
        for line in input_vcf:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    # write extra header
                    # for tag in headers:
                    #     # print(tag)
                    #     output.writelines(tag + '\n')
                    output.writelines(self.header)
                    output.writelines(line)
                else:
                    output.writelines(line)
            else:
                # here annotation comes!
                variant = line.split('\t')
                variant[0] = variant[0].replace('chr', '')
                index = '%s-%s' % (variant[0], variant[1])
                # print(variant)
                annotations = []
                for annotation in self.annotation_files:
                    info = self.annotation_files[annotation]['info'].split(',')
                    # print(info)
                    ann_vcf_file = self.annotation_files[annotation]['file']
                    try:
                        records = ann_vcf_file.fetch(variant[0], int(variant[1]) - 1, int(variant[1]))
                    except:
                        records = []
                    for record in records:

                        ann = record.split('\t')
                        # print(ann)
                        new_info = ann[7].split(';')

                        if annotation == 'pynnotator':
                            for tag in new_info:
                                string = tag.split('=')[0].split('.')[0]
                                if string in self.pynnotator_tags:
                                    annotations.append(tag)
                        else:
                            # print(info)
                            for tag in new_info:
                                string = tag.split('=')[0]
                                if string in info:
                                    annotations.append(tag)
                                    # print(annotations)

                new_info = variant[7] + ';' + ";".join(annotations)
                # print(new_info)
                variant[7] = new_info

                # now dbsnp

                try:
                    records = self.dbsnp.fetch(variant[0], int(variant[1]) - 1, int(variant[1]))
                except:
                    records = []
                rsids = []
                for record in records:
                    # print(record, variant)
                    row = record.split('\t')
                    rsid = row[2]

                    check_flag = False
                    if variant[3] == row[3]:
                        alts = variant[4].split(',')
                        alts_row = row[4].split(',')
                        # compare ALT
                        for alt in alts:
                            if alt in alts_row:
                                check_flag = True
                    if check_flag:
                        rsids.append(rsid)

                if len(rsids) > 0:
                    variant[2] = ",".join(rsids)

                new_line = "\t".join(variant)
                output.writelines(new_line)
                # index()
        output.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MERGE all VCF Files from previous methods.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    merge = Merge(args.vcffile)
    merge.run()
