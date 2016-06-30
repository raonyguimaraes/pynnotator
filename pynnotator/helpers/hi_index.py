#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess

from pynnotator import settings
from subprocess import call

toolname = 'hi_index'

#enable perl5_lib
env = os.environ.copy()
env['PERL5LIB'] = settings.vcftools_dir_perl

class HI_Index(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile
        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        
        #create folder hi_index if it doesn't exists
        if not os.path.exists('hi_index'):
            os.makedirs('hi_index')
    
    def run(self):

        tstart = datetime.now()
        print(tstart, 'Starting hi_index annotation: ', self.vcffile)
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished hi_index annotation, it took: ', annotation_time)

    #Annotate vcf file with Haploinsuficiency Index
    def annotate(self):

        command = '%s/bgzip -c %s > hi_index/%s.vcf.gz' % (settings.htslib_dir, self.vcffile, self.filename)
        call(command, shell=True)

        command = '%s/tabix -p vcf hi_index/%s.vcf.gz' % (settings.htslib_dir, self.filename)
        call(command, shell=True)

        # print 'wwwwwwwwwwwwwwwwwworked!!'
      
        command = '''zcat hi_index/%s.vcf.gz | %s/vcf-annotate \
        -a %s/%s \
        --fill-type \
        -d key=INFO,ID=HI_INDEX,Number=1,Type=String,Description=\'Haploinsuficiency Index\' \
        -c CHROM,FROM,TO,INFO/HI_INDEX > hi_index/hi_index.vcf \
        ''' % (self.filename, settings.vcftools_dir_perl, settings.hi_score_dir, settings.hi_score_file)

        # print command

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            env=env, 
            shell=True)

        # print p
        if p == 0:
            print('This vcf was annotated by %s' % (toolname))
        else:
            print('Sorry this vcf could not be annotated by %s' % (toolname))

        

if  __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Annotate a VCF File with HI_INDEX.')

    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    hi_index = HI_Index(args.vcffile)
    hi_index.run()