#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
from subprocess import call

from pynnotator import settings

"""
- Search and Remove genotypes with [0/0, ./.]
- Search and Replace chr from the beggining of the chromossome names
- Sort VCF by 1...22, X, Y, MT
- Remove previous snpeff annotations from VCF
- Remove annotation sumGLbyD from VCF that causes imcompatibility with snpeff
"""

toolname = 'sanity_check'

#enable perl5_lib
env = os.environ.copy()
env['PERL5LIB'] = settings.vcftools_dir_perl


class Sanity_check(object):
    def __init__(self, vcf_file=None):
        
        self.vcf_file = vcf_file
        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
        
        #create folder sanity_check if it doesn't exists
        if not os.path.exists('sanity_check'):
            os.makedirs('sanity_check')
        #enter inside folder
        # os.chdir('sanity_check')
        
    
    def run(self):

        tstart = datetime.now()
        print(tstart, 'Starting sanity_check: ', self.vcf_file)
        
        self.check()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished sanity_check, it took: ', annotation_time)        

    #sanity vcf file with Vcftools
    def check(self):

        file_vcf = open("%s" % (self.vcf_file), 'r')
        out_vcf = open('sanity_check/onlyvariants.vcf', 'w')
        for line in file_vcf:
            if line.startswith('#'):
                if not line.startswith('##INFO=<ID=EFF'):
                    if not line.startswith('##INFO=<ID=sumGLbyD'):
                        if not line.startswith('##INFO=<ID=CSQ'):
                            out_vcf.writelines(line)
            else:
                row = line.split('\t')

                #removing EFF INFO from VCF
                INFO = row[7]
                NEWINFO = []
                for info in INFO.split(";"):
                        #removing snpeff from annotations
                        if "EFF=" in info:
                            pass
                        #ugly hack to remove this field, because of some bugs in GATK/snpeff that require tyou to have a description about all fields
                        elif "sumGLbyD=" in info:
                            pass
                        elif "CSQ=" in info:
                            pass
                        else:
                            NEWINFO.append(info)
                row[7] = ";".join(NEWINFO)
                row[2] = '.'
                #remove info field from vcf
                # row[7] = ''
                genotype = row[-1].strip().split(':')[0]
                #remove chr from the beggining of chromossome name
                row[0] = row[0].replace('chr', '')
                #remove genotypes with 0/0
                forbidden = ['0/0', './.']
                if genotype not in forbidden:
                    out_vcf.writelines('\t'.join(row))

        out_vcf.close()    
        file_vcf.close()

        #remove EFF Field
        # vcf_tools_dir = '/lgc/programs/vcftools_0.1.10/bin'
        # os.environ["PERL5LIB"] = "/lgc/programs/vcftools_0.1.10/lib/perl5/site_perl/"

        # command = '%s/vcf-annotate onlyvariants.vcf -r INFO/EFF > withouteff.vcf' % (vcf_tools_dir)
        # os.system(command)

        #sort VCF
        #logging.info('Starting Sort VCF')
        #get header

        command = "grep '^#' sanity_check/onlyvariants.vcf > sanity_check/checked.vcf"
        call(command, shell=True)

        #only chromossome numbers first
        
        command = "grep -E -v '^X|^Y|^M|^#|^GL' sanity_check/onlyvariants.vcf | sort -n -k1 -k2 >> sanity_check/checked.vcf"
        call(command, shell=True)

        #only X
        command = "grep -E '^X' sanity_check/onlyvariants.vcf | sort -k1,1d -k2,2n >> sanity_check/checked.vcf"
        call(command, shell=True)

        #only Y
        command = "grep -E '^Y' sanity_check/onlyvariants.vcf | sort -k1,1d -k2,2n >> sanity_check/checked.vcf"
        call(command, shell=True)

        #only MT
        command = "grep -E '^M' sanity_check/onlyvariants.vcf | sort -k1,1d -k2,2n >> sanity_check/checked.vcf"
        call(command, shell=True)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     env=env, 
        #     shell=True)
        print('This vcf was sucessfully checked with sanity_check')

        # if p == 0:
        #     print 'This vcf was validated by vcf-sanity_check'
        # else:
        #     print 'Sorry this vcf could not be annotated by %s' % (toolname)

        

if  __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Sanity Check a VCf File')

    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    sanity_check = Sanity_check(args.vcf_file)
    sanity_check.run()
