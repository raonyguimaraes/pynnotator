#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import multiprocessing as mp
import os
import pysam
from datetime import datetime
from pynnotator import settings
from subprocess import run

class Dbnsfp(object):
    def __init__(self, vcf_file=None):
        
            self.vcf_file = vcf_file
            self.dbnfsp_header = open('%s/dbnsfp/header.vcf' % (settings.data_dir)).readlines()
            
            self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
            # create folder validator if it doesn't exists
            if not os.path.exists('dbnfsp'):
                os.makedirs('dbnfsp')

    def run(self):

            tstart = datetime.now()

            print(tstart, 'Starting DBNSFP annotator: ', self.vcf_file)

            
            command = """java -Xmx%s -jar %s/SnpSift.jar \
            dbnsfp -v -db %s %s > dbnfsp/dbnfsp.annotated.vcf \
                """ % (
                    settings.snpsift_memory, settings.snpeff_dir, settings.dbnsfp, self.vcf_file)
            run(command,shell=True)

            tend = datetime.now()
            annotation_time = tend - tstart
            print(tend, 'Finished DBNSFP, it took: ', annotation_time)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Annotate a VCF File with DbNSFP.')
    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()
    dbnfsp = Dbnsfp(args.vcf_file)
    dbnfsp.run()
