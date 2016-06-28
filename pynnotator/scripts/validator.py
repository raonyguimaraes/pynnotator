#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
import csv

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with VAlIDATOR.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

args = parser.parse_args()

toolname = 'validator'

#enable perl5_lib

# print 'vcf_tools_path', vcf_tools_path
os.environ["PERL5LIB"] = "%s/lib/perl5/site_perl/" % (vcf_tools_path)
env = os.environ.copy()
env['PERL5LIB'] = "%s/lib/perl5/site_perl/" % (vcf_tools_path)


class Validator(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        
        #create folder validator if it doesn't exists
        if not os.path.exists('validator'):
            os.makedirs('validator')
        #enter inside folder
        # os.chdir('validator')
        
    
    def run(self):

        tstart = datetime.now()
        print tstart, 'Starting validator: ', self.vcffile
        
        self.validate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print tend, 'Finished validator, it took: ', annotation_time        

    #Validate vcf file with Vcftools
    def validate(self):

        command = '%s/bgzip -c %s > validator/%s.vcf.gz' % (tabix_path, self.vcffile, self.filename)
        print 'command', command

        os.system(command)
        

        command = '%s/tabix -p vcf validator/%s.vcf.gz' % (tabix_path, self.filename)
        os.system(command)

        command = '%s/bin/vcf-validator validator/%s.vcf.gz 2>validator/validation.log' % (vcf_tools_path, self.filename)

        # print 'validator command', command


        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            env=env, 
            shell=True)

        # print p
        if p == 0:
            print 'This vcf was validated by vcf-validator'
        else:
            print 'Sorry this vcf could not be annotated by %s' % (toolname)

        

if  __name__ == '__main__' :
    validator = Validator(args.vcffile)
    validator.run()





# from optparse import OptionParser
# import time
# from datetime import datetime
# import os
# import csv 
# import shlex, subprocess

# #This script validates a VCF File using VCFTOOLS vcf-validator
# #For this returns the output of "process_result" as '' if the VCF is valid

# import logging
# logging.basicConfig(filename='validation.log', filemode="w", format='%(asctime)s %(levelname)s %(message)s',
#                             datefmt='%m/%d/%Y %I:%M:%S %p', 
#                     level=logging.DEBUG, )#, 

# # logging.info('Starting Validation')
# logging.info('Starting Validation')
# # print 'Start Validation Script'

# parser = OptionParser()
# parser.add_option("-v", dest="vcf_file",
#                   help="VCF File to Validate", metavar="VCF")

# (options, args) = parser.parse_args()

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# vcf_tools_dir = '%s/bin' % (vcf_tools_path)

# # command = "export PERL5LIB=%s/lib/perl5/site_perl/" % (vcf_tools_path)
# os.environ["PERL5LIB"] = "%s/lib/perl5/site_perl/" % (vcf_tools_path)
# env = os.environ.copy()
# env['PERL5LIB'] = "%s/lib/perl5/site_perl/" % (vcf_tools_path)

# vcffile = options.vcf_file

# filepath = os.path.dirname(os.path.abspath(options.vcf_file))
# vcffile = os.path.basename(str(options.vcf_file)) #full
# filename = os.path.splitext(vcffile)[0] #without extension

# # print os.getcwd()
# # print 'vcf validator path', vcffile
# # print os.getcwd()
# print os.getcwd()

# #compress file
# command = 'bgzip -c %s >%s.gz' % (options.vcf_file, vcffile)
# # print 'bgzip', command
# bgzip_output = os.system(command)

# # print bgzip_output
# # logging.info('bgzip Output:%s' % (bgzip_output))


# # args = shlex.split(command)
# # print 'args', args

# # try:
# #     retcode = subprocess.check_output(command, cwd=os.getcwd(), shell=True)
# #     # retcode.wait()
# # except subprocess.CalledProcessError:
# #     print '<b>something went wrong in sox: returned error code ' +\
# #       retcode + ', but we are continuing anyway...</b>'


# # os.system(command)
# # die()
# # print 'saiu bgzip'


# # variable = subprocess.check_output(["ls", "-lah"])
# # print variable


# command = 'tabix -p vcf %s.gz' % (vcffile)
# os.system(command)

# #calculate the time this script will take to finish
# # logging.info('Starting Validation')
# tstart = datetime.now()

# log_file = open('validation2.log', 'w')

# command = '%s/vcf-validator %s.gz' % (vcf_tools_dir, vcffile)#2>>validator.log
# # print command
# p = subprocess.call(command, 
#     cwd=os.getcwd(), 
#     env=env, 
#     shell=True, 
#     stdout=log_file, 
#     stderr=log_file)

# log_file.close()

# #calculate the time this script will take to finish
# tend = datetime.now()
# logging.info('Finished Validation')
# # print 'p:', p
# if p == 0:
#     print 'This vcf was validated'
#     # exit 0
# else:
#     print 'Sorry this vcf could not be validated'
#     exit(1)
