#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import pysam
from collections import OrderedDict
from datetime import datetime

from pynnotator import settings
from subprocess import run
toolname = 'merge'


class Merge(object):
    def __init__(self, vcffile=None):

        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        self.basedir = os.getcwd()

        # create folder merge if it doesn't exists
        if not os.path.exists('merge'):
            os.makedirs('merge')
        # enter inside folder
        os.chdir('merge')

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting merge: ', self.vcffile)

        self.merge()

        tend = datetime.now()
        annotation_time = tend - tstart
        print(tend, 'Finished merge, it took: ', annotation_time)

        # merge VCF Files with VariantAnnotator

    def merge(self):

        # print(BASE_DIR)

        files = ['../snpeff/snpeff.output.vcf', '../vep/vep.output.sorted.vcf', '../snpsift/snpsift.final.vcf']
        for file in files:
            command = 'bgzip {}'.format(file)
            run(command, shell=True)
            command = 'tabix -p vcf {}.gz'.format(file)
            run(command, shell=True)


        config = open('config.toml', 'w')
        config.write("""[[annotation]]
file="{}/snpeff/snpeff.output.vcf.gz"
fields = ["EFF"]
ops=["first"]

[[annotation]]
file="{}/vep/vep.output.sorted.vcf.gz"
fields = ["CSQ"]
ops=["first"]

[[annotation]]
file="{}/snpsift/snpsift.final.vcf.gz"
fields = ["VARTYPE", "SNP", "MNP", "INS", "DEL", "MIXED", "HOM", "HET"]
ops=["first", "first", "first", "first", "first", "first", "first", "first"]

[[annotation]]
file="{}/hgmd/HGMD_PRO_2017.3_hg19.vcf.gz"
fields = ["CLASS", "MUT", "GENE", "STRAND", "DNA", "PROT", "DB", "PHEN"]
ops=["first", "first", "first", "first", "first", "first", "first", "first"]

[[annotation]]
file="{}/dbsnp/All_20170403.vcf.gz"
fields = ["ID"]
ops=["first"]

[[annotation]]
file="{}/dbsnp/clinvar.vcf.gz"
fields = ["ID"]
ops=["first"]
            """.format(self.basedir, self.basedir, self.basedir, settings.data_dir, settings.data_dir, settings.data_dir))
        config.close()
        command = '{}/vcfanno/vcfanno_linux64 -p 16 config.toml {} > ../annotation.final.vcf'.format(settings.libs_dir, self.vcffile)
        run(command,shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MERGE all VCF Files from previous methods.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    merge = Merge(args.vcffile)
    merge.run()
