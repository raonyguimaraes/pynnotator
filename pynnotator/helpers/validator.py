#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
import csv
from subprocess import call

from pynnotator import settings


parser = argparse.ArgumentParser(description='Annotate a VCF File with VAlIDATOR.')
parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

args = parser.parse_args()

toolname = 'validator'

env = os.environ.copy()
env['PERL5LIB'] = settings.vcftools_dir_perl

class Validator(object):
    def __init__(self, vcf_file=None):
        
        self.vcf_file = vcf_file

        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
        self.vcf_path = os.path.dirname(self.vcf_file)
        self.validation_path = os.path.join(self.vcf_path, 'validator')
        
        #create folder validator if it doesn't exists
        if not os.path.exists(self.validation_path):
            os.makedirs(self.validation_path)
    
    def run(self):

        tstart = datetime.now()
        print(tstart, 'Starting validator: ', self.vcf_file)
        
        std = self.validate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished validator, it took: ', annotation_time)        
        
        return std

    #Validate vcf file with Vcftools
    def validate(self):
        #check if file is in .gz format
        if not self.vcf_file.endswith('.gz'):
            command = '%s/bgzip -c %s > %s/%s.gz' % (settings.htslib_dir, self.vcf_file, self.validation_path, self.filename)
            call(command, shell=True)
        else:
            command = 'cp %s %s/' % (self.vcf_file, self.validation_path)
            call(command, shell=True)

        command = '%s/tabix -p vcf %s/%s.gz' % (settings.htslib_dir, self.validation_path, self.filename)
        call(command, shell=True)

        command = '%s/vcf-validator %s/%s.gz 2>%s/validation.log' % (settings.vcftools_dir_perl, self.validation_path, self.filename, self.validation_path)

        # print 'validator command', command
        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            env=env, 
            shell=True)

        
        if p == 0:
            print('This vcf was sucessfully validated by vcf-validator')
        else:
            print('Sorry this vcf could not be validated!')
        return p

if  __name__ == '__main__' :
    validator = Validator(args.vcf_file)
    validator.run()