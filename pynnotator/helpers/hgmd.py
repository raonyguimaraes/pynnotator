#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
from datetime import datetime
from subprocess import call

from pynnotator import settings

toolname = 'hgmd'


class HGMD(object):
    def __init__(self, vcffile=None):

        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        # create folder vep if it doesn't exists
        if not os.path.exists('hgmd'):
            os.makedirs('hgmd')
            # enter inside folder
            # os.chdir('vep')

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting hgmd annotation: ', self.vcffile)

        self.annotate()

        tend = datetime.now()
        annotation_time = tend - tstart
        print(tend, 'Finished hgmd annotation, it took: ', annotation_time)

    # convert and annotate the vcf file to vep
    def annotate(self):

        if self.vcffile.endswith('.gz'):
            command = 'cp %s hgmd/hgmd.raw.vcf.gz' % (self.vcffile)
        else:
            command = 'bgzip -c %s > hgmd/hgmd.raw.vcf.gz' % (self.vcffile)
        
        call(command, shell=True)

        command = 'tabix -p vcf hgmd/hgmd.raw.vcf.gz'
        call(command, shell=True)

        command = '''bcftools annotate -a %s/hgmd/%s -c INFO hgmd/hgmd.raw.vcf.gz > hgmd/hgmd.vcf
        ''' % (settings.data_dir, settings.hgmd)

        command = '''zcat hgmd/hgmd.raw.vcf.gz | %s/vcf-annotate \
        -a %s \
        --fill-type \
        -d key=INFO,ID=CLASS,Number=1,Type=String,Description=\"Mutation Category, https://portal.biobase-international.com/hgmd/pro/global.php#cats\" \
        -d key=INFO,ID=MUT,Number=1,Type=String,Description=\"HGMD mutant allele\" \
        -d key=INFO,ID=GENE,Number=1,Type=String,Description=\"Gene symbol\" \
        -d key=INFO,ID=STRAND,Number=1,Type=String,Description=\"Gene strand\" \
        -d key=INFO,ID=DNA,Number=1,Type=String,Description=\"DNA annotation\" \
        -d key=INFO,ID=PROT,Number=1,Type=String,Description=\"Protein annotation\" \
        -d key=INFO,ID=DB,Number=1,Type=String,Description=\"dbSNP identifier, build 146\" \
        -d key=INFO,ID=PHEN,Number=1,Type=String,Description=\"HGMD primary phenotype\" \
        -c CHROM,FROM,TO,INFO/CLASS,INFO/MUT,INFO/GENE,INFO/STRAND,INFO/DNA,INFO/PROT,INFO/DB,INFO/PHEN > hgmd/hgmd.vcf 2>hgmd/hgmd.errors.txt \
        ''' % (settings.vcftools_dir_perl, settings.hgmd_file)

        # print(command)
        call(command, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate a VCF File with HGMD.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    hgmd = HGMD(args.vcffile)
    hgmd.run()
