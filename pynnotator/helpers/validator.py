#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
import os
import subprocess
from subprocess import call, run, check_output
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

        # print(tend, 'Finished validator, it took: ', annotation_time)

        return std

    # Validate vcf file with Vcftools
    def validate(self):
        # check if file is in .gz format

        if not self.vcf_file.endswith('.gz'):
            command = '%s/bgzip -c %s > validator/%s.vcf.gz' % (settings.htslib_dir, self.vcf_file, self.filename)
            call(command, shell=True)
        else:
            command = 'cp %s validator/' % (self.vcf_file)
            call(command, shell=True)

        command = '%s/tabix -p vcf validator/%s.vcf.gz' % (settings.htslib_dir, self.filename)
        call(command, shell=True)

        # command = '%s/vcf-validator validator/%s.vcf.gz 2>validator/validation.log' % (
            # settings.vcftools_dir_perl, self.filename)
        
        command = '%s/vcf_validator -i validator/%s.vcf.gz 2>validator/validation.log' % (
            settings.vcf_validator_dir, self.filename)

        # try:
        #     retcode = call(command, shell=True)
        #     if retcode < 0:
        #         print("Child was terminated by signal", -retcode, file=sys.stderr)
        #     else:
        #         print("Child returned", retcode, file=sys.stderr)
        #         print(call)
        # except OSError as e:
        #     print("Execution failed:", e, file=sys.stderr)        
        # print 'validator command', command
        try:
            output = check_output(command, shell=True)
            logging.info('Command Output: %s' % (output))
        except subprocess.CalledProcessError as e:
            
            msg =  "Error {}".format(e.output.decode('utf-8'))
            self.log(msg)

            # logging.info('Error Output: %s' % (e.output.decode('utf-8')))
            
        # p = subprocess.call(command,
        #                     cwd=os.getcwd(),
        #                     env=env,
        #                     shell=True)

                
        time_end = datetime.now()
        command = 'rm validator/%s.vcf.gz*' % (self.filename)
        run(command, shell=True)

        # if p == 0:
        #     print(time_end, 'This vcf was sucessfully validated by vcf-validator!')
        # else:
        #     print(time_end, 'Sorry this vcf could not be validated!')
        # return p


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate a VCF File with VAlIDATOR.')
    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()
    validator = Validator(args.vcf_file)
    validator.run()
