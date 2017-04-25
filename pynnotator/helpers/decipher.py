#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess

from pynnotator import settings
from subprocess import call

toolname = 'decipher'

#enable perl5_lib
env = os.environ.copy()
env['PERL5LIB'] = settings.vcftools_dir_perl

class Decipher(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile
        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        
        #create folder decipher if it doesn't exists
        if not os.path.exists('decipher'):
            os.makedirs('decipher')
    
    def run(self):

        tstart = datetime.now()
        print(tstart, 'Starting decipher annotation: ', self.vcffile)
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished decipher annotation, it took: ', annotation_time)

    #Annotate vcf file with Haploinsuficiency Index
    def annotate(self):

        command = '%s/bgzip -c %s > decipher/%s.vcf.gz' % (settings.htslib_dir, self.vcffile, self.filename)
        call(command, shell=True)

        command = '%s/tabix -p vcf decipher/%s.vcf.gz' % (settings.htslib_dir, self.filename)
        call(command, shell=True)

        command = '''zcat decipher/%s.vcf.gz | %s/vcf-annotate \
        -a %s \
        --fill-type \
        -d key=INFO,ID=HI_PREDICTIONS,Number=.,Type=String,Description=\'Haploinsuficiency Predictions\' \
        -c CHROM,FROM,TO,INFO/HI_PREDICTIONS > decipher/hi_predictions.vcf \
        ''' % (self.filename, settings.vcftools_dir_perl, settings.hi_predictions)

        # print command

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            env=env, 
            shell=True)


        time_end = datetime.now()

        if p == 0:
            print(time_end, 'This vcf was sucessfully annotated by %s!' % (toolname))
        else:
            print(time_end, 'Sorry this vcf could not be annotated by %s' % (toolname))

        

if  __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Annotate a VCF File with Decipher.')

    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    decipher = Decipher(args.vcffile)
    decipher.run()