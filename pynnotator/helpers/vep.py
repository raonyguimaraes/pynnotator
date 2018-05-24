#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
from datetime import datetime
from subprocess import call

from pynnotator import settings

toolname = 'vep'


class Vep(object):
    def __init__(self, vcffile=None):

        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        # create folder vep if it doesn't exists
        if not os.path.exists('vep'):
            os.makedirs('vep')
            # enter inside folder
            # os.chdir('vep')

    def install(self):
        print('install')

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting vep annotation: ', self.vcffile)

        self.annotate()

        tend = datetime.now()
        annotation_time = tend - tstart
        print(tend, 'Finished vep annotation, it took: ', annotation_time)

    # convert and annotate the vcf file to vep
    def annotate(self):

        command = '''perl %s/vep \
        -i %s \
        --cache \
        --dir %s \
        --offline \
        --format vcf \
        -o vep/vep.output.vcf --vcf --force_overwrite \
        --assembly GRCh37 \
        -sift b -polyphen b \
        -plugin dbNSFP,%s,MutationTaster_score,MutationTaster_converted_rankscore,MutationTaster_pred,MutationTaster_model,MutationTaster_AAE,M-CAP_score,M-CAP_rankscore,M-CAP_pred,CADD_raw,CADD_raw_rankscore,CADD_phred,1000Gp3_AC,1000Gp3_AF,1000Gp3_EUR_AC,1000Gp3_EUR_AF,TWINSUK_AC,TWINSUK_AF,ALSPAC_AC,ALSPAC_AF,gnomAD_exomes_AC,gnomAD_exomes_AN,gnomAD_exomes_AF,gnomAD_genomes_AC,gnomAD_genomes_AN,gnomAD_genomes_AF \
        --no_progress \
        --no_intergenic \
        --numbers \
        --biotype \
        --total_length \
        --coding_only \
        --pick \
        --symbol \
        1>vep/vep.log \
        --fork %s \
        ''' % (settings.vep_dir, self.vcffile, settings.vep_cache_dir, settings.dbnsfp, settings.vep_cores)
        # 1> vepreport.log \
        ##--pick \
        # condel_plugin, dbscsnv_plugin, 
        # -plugin %s \
        # --plugin %s \

        p = subprocess.call(command,
                            cwd=os.getcwd(),
                            shell=True)

        tend = datetime.now()

        # if p == 0:
        #     print(tend, 'This vcf was sucessfully annotated by %s!' % (toolname))
        # else:
        #     print(tend, 'Sorry this vcf could not be annotated by %s' % (toolname))

        # command = '(grep ^# output.vep.vcf; grep -v ^# output.vep.vcf|sort -k1,1N -k2,2n) > output.vep.sorted.vcf'
        # Sort VCF file 


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

        tend = datetime.now()
        # print(tend, 'Finished sorting vep vcf.')

        command = 'rm vep/vep.output.vcf'
        call(command, shell=True)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate a VCF File with VEP.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    vep = Vep(args.vcffile)
    vep.run()
