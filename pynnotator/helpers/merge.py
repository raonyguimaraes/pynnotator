
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess

from pynnotator import settings

toolname = 'merge'

class Merge(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        
        #create folder merge if it doesn't exists
        if not os.path.exists('merge'):
            os.makedirs('merge')
        #enter inside folder
        os.chdir('merge')
        
    
    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting merge: ', self.vcffile)
        
        self.merge()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished merge, it took: ', annotation_time)        

    #merge VCF Files with VariantAnnotator
    def merge(self):

        BASE_DIR = os.getcwd()

        #merge 5 vcfs: snpeff, vep, snpsift, hi_index and hgmd 
        # print('merge snpeff')
        #snpeff
        command = "java -Xmx%s -jar \
        %s/SnpSift.jar \
        annotate -info EFF -noId \
        ../snpeff/snpeff.output.vcf \
        ../sanity_check/checked.vcf \
        > snpeff.vcf \
        "% (settings.snpsift_merge_memory, settings.snpeff_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)
        # print 'snpeff'
        # print('merge vep')
        #vep
        command = "java -Xmx%s -jar \
        %s/SnpSift.jar \
        annotate -info CSQ -noId \
        ../vep/vep.output.sorted.vcf \
        snpeff.vcf \
        > snpeff.vep.vcf \
        "% (settings.snpsift_merge_memory, settings.snpeff_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)
        # print('merge snpsift')
        #snpsift
        command = "java -Xmx%s -jar \
        %s/SnpSift.jar \
        annotate -info VARTYPE,SNP,MNP,INS,DEL,MIXED,HOM,HET -noId \
        ../snpsift/snpsift.final.vcf \
        snpeff.vep.vcf \
        > snpsift.snpeff.vep.vcf \
        "% (settings.snpsift_merge_memory, settings.snpeff_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        # print('merge hi_index')
        #hi_index
        command = "java -Xmx%s -jar \
        %s/SnpSift.jar \
        annotate -info HI_INDEX -noId \
        ../hi_index/hi_index.vcf \
        snpsift.snpeff.vep.vcf \
        > hi_index.snpsift.snpeff.vep.vcf \
        "% (settings.snpsift_merge_memory, settings.snpeff_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        # #hgmd
        # command = "java -Xmx40G -jar \
        # %s/SnpSift.jar \
        # annotate -info HGMD -noId \
        # ../hgmd/hgmd.vcf \
        # hi_index.snpsift.snpeff.vep.vcf \
        # > hgmd.hi_index.snpsift.snpeff.vep.vcf  \
        # "% (settings.snpeff_dir)


        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)
        
        # print('merge pynnotator')
        #pynnotator - 1000genomes, dbsnp, clinvar, esp6500, ensembl
        command = "java -Xmx%s -jar \
        %s/SnpSift.jar \
        annotate -noId \
        ../pynnotator/pynnotator.vcf \
        hi_index.snpsift.snpeff.vep.vcf \
        > 1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf  \
        " % (settings.snpsift_merge_memory, settings.snpeff_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        # print   'cadd vest'
        
        # print('merge cadd_dann')
        #cadd_dann
        command = "java -Xmx%s -jar \
        %s/SnpSift.jar \
        annotate -noId -info dbNSFP_DANN_score,dbNSFP_DANN_rankscore,dbNSFP_CADD_raw,dbNSFP_CADD_raw_rankscore,dbNSFP_CADD_phred \
        ../cadd_dann/cadd_dann.vcf \
        1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf \
        > cadd_dann.1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf  \
        "% (settings.snpsift_merge_memory, settings.snpeff_dir)


        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        # print('merge dbsnp')
        #dbsnp
        command = "java -Xmx%s -jar \
        %s/SnpSift.jar \
        annotate -id \
        %s \
        cadd_dann.1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf \
        > annotation.final.vcf  \
        "% (settings.snpsift_merge_memory, settings.snpeff_dir,settings.dbsnp)


        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        if p == 0:
            print('This vcf was succesfully merged')
        else:
            print('Sorry this vcf could not be merged')


if  __name__ == '__main__' :

    parser = argparse.ArgumentParser(description='MERGE all VCF Files from previous methods.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')
    args = parser.parse_args()

    merge = Merge(args.vcffile)
    merge.run()