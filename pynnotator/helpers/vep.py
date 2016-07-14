#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess

from pynnotator import settings
from subprocess import call

toolname = 'vep'

class Vep(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        
        #create folder vep if it doesn't exists
        if not os.path.exists('vep'):
            os.makedirs('vep')
        #enter inside folder
        # os.chdir('vep')
        
    
    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting vep annotation: ', self.vcffile)
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished vep annotation, it took: ', annotation_time)

    #convert and annotate the vcf file to vep
    def annotate(self):

        command = '''perl %s/variant_effect_predictor.pl \
        -i %s \
        --dir %s \
        -sift b -polyphen b \
        -o vep/vep.output.vcf --vcf --cache --force_overwrite \
        --no_progress \
        --no_intergenic \
        --numbers \
        --biotype \
        --total_length \
        --coding_only \
        --pick \
        --offline \
        --symbol \
        1>vep/vep.log \
        --fork %s \
        ''' % (settings.vep_dir, self.vcffile, settings.vep_cache_dir, settings.vep_cores)
        # 1> vepreport.log \
        ##--pick \
        # condel_plugin, dbscsnv_plugin, 
        # -plugin %s \
        # --plugin %s \
        
        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        if p == 0:
            print('This vcf was annotated by %s' % (toolname))
        else:
            print('Sorry this vcf could not be annotated by %s' % (toolname))

        # command = '(grep ^# output.vep.vcf; grep -v ^# output.vep.vcf|sort -k1,1N -k2,2n) > output.vep.sorted.vcf'
        #Sort VCF file 
        

        command = '''grep '^#' vep/vep.output.vcf > vep/vep.output.sorted.vcf'''
        call(command, shell=True)
        
        command = '''grep -E -v '^X|^Y|^M|^#|^GL' vep/vep.output.vcf | sort -n -k1 -k2 >> vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        command = '''grep -E '^X' vep/vep.output.vcf | sort -k1,1d -k2,2n >> vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        command = '''grep -E '^Y' vep/vep.output.vcf | sort -k1,1d -k2,2n >> vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        command = '''grep -E '^M' vep/vep.output.vcf | sort -k1,1d -k2,2n >> vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        print('Finished sorting VCF')

if  __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Annotate a VCF File with VEP.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    vep = Vep(args.vcffile)
    vep.run()
