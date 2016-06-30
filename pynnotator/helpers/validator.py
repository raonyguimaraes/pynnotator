#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
from subprocess import call
from pynnotator import settings

toolname = 'validator'

env = os.environ.copy()
env['PERL5LIB'] = settings.vcftools_dir_perl

class Validator(object):
    def __init__(self, vcf_file=None):
        
        self.vcf_file = vcf_file

        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
        #create folder validator if it doesn't exists
        if not os.path.exists('validator'):
            os.makedirs('validator')
    
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
            command = '%s/bgzip -c %s > validator/%s.gz' % (settings.htslib_dir, self.vcf_file, self.filename)
            call(command, shell=True)
        else:
            command = 'cp %s validator/' % (self.vcf_file)
            call(command, shell=True)

        command = '%s/tabix -p vcf validator/%s.gz' % (settings.htslib_dir, self.filename)
        call(command, shell=True)

        command = '%s/vcf-validator validator/%s.gz 2>validator/validation.log' % (settings.vcftools_dir_perl, self.filename)

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
    parser = argparse.ArgumentParser(description='Annotate a VCF File with VAlIDATOR.')
    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()
    validator = Validator(args.vcf_file)
    validator.run()