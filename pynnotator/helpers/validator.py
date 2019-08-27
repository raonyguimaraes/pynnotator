#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import os
import subprocess
from subprocess import call, check_output
from datetime import datetime
import logging

from pynnotator import settings


toolname = 'validator'

env = os.environ.copy()
env['PERL5LIB'] = settings.vcftools_dir_perl

class Validator(object):
    def __init__(self, vcf_file=None):

        self.vcf_file = vcf_file
        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
        
        logging.basicConfig(filename='validation.log',level=logging.DEBUG)

        # create folder validator if it doesn't exists
        if not os.path.exists('validator'):
            os.makedirs('validator')

    def log(self, msg):
        
        logging.info(msg)
        print(msg)


    def run(self):

        tstart = datetime.now()
        msg = "{} Starting validator: {}".format(tstart, self.vcf_file)
        
        self.log(msg)

        std = self.validate()

        tend = datetime.now()
        annotation_time = tend - tstart
        
        msg = "{} Finished validator, it took: {}".format(tend, annotation_time)
        self.log(msg)

        return std

    # Validate vcf file with Vcftools
    def validate(self):
        # check if file is in .gz format

        # if not self.vcf_file.endswith('.gz'):
        #     command = '%s/bgzip -c %s > validator/%s.vcf.gz' % (settings.htslib_dir, self.vcf_file, self.filename)
        #     call(command, shell=True)
        # else:
        command = 'cp %s validator/' % (self.vcf_file)
        call(command, shell=True)

        # command = '%s/tabix -p vcf validator/%s.vcf.gz' % (settings.htslib_dir, self.filename)
        # call(command, shell=True)
        
        command = '%s/vcf_validator -i validator/%s.vcf 1>validator/validation.log 2>&1' % (
            settings.vcf_validator_dir, self.filename)

        try:
            output = check_output(command, shell=True)
            logging.info('Command Output: %s' % (output))
        except subprocess.CalledProcessError as e:
            
            msg =  "Error {}".format(e.output.decode('utf-8'))
            self.log(msg)

        command = 'tail validator/validation.log'
        call(command, shell=True)        
                
        time_end = datetime.now()
        command = 'rm validator/%s.vcf' % (self.filename)
        call(command, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate a VCF File with VAlIDATOR.')
    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()
    validator = Validator(args.vcf_file)
    validator.run()
