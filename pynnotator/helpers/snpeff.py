#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
from datetime import datetime

from pynnotator import settings
from subprocess import run

class Snpeff(object):
    def __init__(self, vcffile=None):

        self.vcffile = vcffile
        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        # create folder snpeff if it doesn't exists
        if not os.path.exists('snpeff'):
            os.makedirs('snpeff')

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting snpEff annotation: ', self.vcffile)

        self.annotate()

        tend = datetime.now()
        annotation_time = tend - tstart
        print(tend, 'Finished snpEff annotation, it took: ', annotation_time)
        

    # convert and annotate the vcf file to snpeff
    def annotate(self):

        BASE_DIR = os.getcwd()
        # print BASE_DIR
        # -canon to report only canonical transcript, -o gatk to report only one #GRCh37.64
        # true
        # snpeff 4.0
        command = """java -Xmx%s -jar %s/snpEff.jar \
        -c %s/snpEff.config \
        %s %s \
        -no-downstream \
        -no-intergenic \
        -no intragenic \
        -onlyProtein \
        -no-intron \
        -no-upstream \
        -noNextProt \
        -no-utr -canon -classic \
        >snpeff/snpeff.output.vcf""" % (
            settings.snpEff_memory, settings.snpeff_dir, settings.snpeff_dir, settings.snpeff_database, self.vcffile)
        # print(command)


        # 

        p = subprocess.call(command,
                            cwd=os.getcwd(),
                            shell=True)

        tend = datetime.now()

        command = 'mv snpEff_genes.txt snpEff_summary.html snpeff/'
        run(command, shell=True)
        
        # if p == 0:
        #     print(tend, 'This vcf was annotated by snpEff with Success.')
        # else:
        #     print(tend, 'Sorry this vcf could not be anotated by snpeff.')
        return p


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate a VCF File with Snpeff.')

    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    snpeff = Snpeff(args.vcffile)
    snpeff.run()
