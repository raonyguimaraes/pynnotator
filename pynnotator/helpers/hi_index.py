#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
import csv

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with HI_INDEX.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

args = parser.parse_args()

toolname = 'hi_index'

#enable perl5_lib
os.environ["PERL5LIB"] = "%s/lib/perl5/site_perl/" % (vcf_tools_path)
env = os.environ.copy()
env['PERL5LIB'] = "%s/lib/perl5/site_perl/" % (vcf_tools_path)


class Hi_index(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        
        #create folder hi_index if it doesn't exists
        if not os.path.exists('hi_index'):
            os.makedirs('hi_index')
        #enter inside folder
        # os.chdir('hi_index')
        
    
    def run(self):
        tstart = datetime.now()
        print tstart, 'Starting hi_index annotation: ', self.vcffile
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print tend, 'Finished hi_index annotation, it took: ', annotation_time        

    #Annotate vcf file with Haploinsuficiency Index
    def annotate(self):

        command = '%s/bgzip -c %s > hi_index/%s.vcf.gz' % (tabix_path, self.vcffile, self.filename)
        os.system(command)

        command = '%s/tabix -p vcf hi_index/%s.vcf.gz' % (tabix_path, self.filename)
        os.system(command)

        # print 'wwwwwwwwwwwwwwwwwworked!!'
      
        command = 'zcat hi_index/%s.vcf.gz | %s/bin/vcf-annotate \
        -a %s \
        --fill-type \
        -d key=INFO,ID=HI_INDEX,Number=1,Type=String,Description=\'Haploinsuficiency Index\' \
        -c CHROM,FROM,TO,INFO/HI_INDEX > hi_index/hi_index.vcf \
        ' % (self.filename, vcf_tools_path, hi_data)

        # print command
        
                # os.system(command)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            env=env, 
            shell=True)

        # print p
        if p == 0:
            print 'This vcf was annotated by %s' % (toolname)
        else:
            print 'Sorry this vcf could not be annotated by %s' % (toolname)

        

if  __name__ == '__main__' :
    hi_index = Hi_index(args.vcffile)
    hi_index.run()