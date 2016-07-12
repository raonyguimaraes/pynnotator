#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess

from pynnotator import settings

class Snpeff(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        
        #create folder snpeff if it doesn't exists
        if not os.path.exists('snpeff'):
            os.makedirs('snpeff')
        #enter inside folder
        # os.chdir('snpeff')
        
    
    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting snpEff annotation: ', self.vcffile)
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished snpEff annotation, it took: ', annotation_time)        

    #convert and annotate the vcf file to snpeff
    def annotate(self):
        
         
        BASE_DIR = os.getcwd()
        #print BASE_DIR
        #-canon to report only canonical transcript, -o gatk to report only one #GRCh37.64
        #true
        #snpeff 4.0
        command = """java -Xmx%s -jar %s/snpEff.jar eff \
        -c %s/snpEff.config \
        -no-downstream \
        -no-intergenic \
        -no intragenic \
        -onlyProtein \
        -no-intron \
        -no-upstream \
        -noNextProt \
        -no-utr -canon \
        -classic -i vcf -t  %s %s \
        >snpeff/snpeff.output.vcf""" % (settings.snpEff_memory, settings.snpeff_dir, settings.snpeff_dir, settings.snpeff_database, self.vcffile)
        # print(command)
        


        #snpeff 2.0.5d
        # command = "%s/java -Xmx%s -jar %s/snpEff.jar eff \
        # -c %s/snpEff.config \
        # -v -onlyCoding true \
        # -no-downstream -no-intergenic -no-intron -no-upstream -no-utr\
        # -i vcf -o vcf %s %s \
        # >snpeff/snpeff.output.vcf" % (java_path, snpEff_memory, snpeff_dir, snpeff_dir, snpeff_database, self.vcffile)

        # print(command)
        
        # -i vcf 
        # args = shlex.split(command)
        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)
        if p == 0:
            print('This vcf was annotated by snpEff with Success')
        else:
            print('Sorry this vcf could not be anotated by snpeff')

        return p
        # command = "java -Xmx40G -jar %s/GenomeAnalysisTK.jar \
        # -T VariantAnnotator \
        # -R %s \
        # -A SnpEff \
        # --alwaysAppendDbsnpId \
        # --variant ../%s \
        # --snpEffFile snpEff_output.vcf \
        # -L ../%s \
        # -o snpeff.final.vcf \
        # --dbsnp %s \
        # --log_to_file snpeffgatkreport.log \
        # " % (gatk_dir, reference, self.vcffile, self.vcffile, dbsnp)
        # #        --logging_level ERROR
        # # print 'snpeff command', command

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)
        # if p == 0:
        #     print 'Finished running GATK VariantAnnotator after snpEff'
        # else:
        #     print 'Sorry was an error in GATK VariantAnnotator after snpEff'

# 

if  __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Annotate a VCF File with Snpeff.')

    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    snpeff = Snpeff(args.vcffile)
    snpeff.run()
