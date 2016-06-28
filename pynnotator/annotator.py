#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

# from settings import *

import time
from datetime import datetime

import csv
import shutil
import shlex, subprocess

from threading import Thread

parser = argparse.ArgumentParser(description='Annotate a VCF File with VEP.')
parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

args = parser.parse_args()

class Annotator:

    is_validated = False

    def __init__(self, vcffile=None):
        
        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        # create a folder for the annotation if it doesn't exists, 
        # or delete and create if the folder already exists
        ann_name = "ann_%s" % (self.filename)

        self.vcffile = os.path.abspath(vcffile)
        
        if not os.path.exists(ann_name):
            os.makedirs(ann_name)
        else:
            shutil.rmtree(ann_name)
            os.makedirs(ann_name)

        os.chdir(ann_name)
                #copy vcf to ann folder and rewrite self.vcffile
        

        #os.system('cp ../%s initial.vcf' % (vcffile))

        
        


        print('vcffile', self.vcffile)
        # os.path.basename(str(vcffile))
        
        os.makedirs('log')
        os.makedirs('reports')




    def run(self):
        
        tstart = datetime.now()

        #run vcftools vcf-validator on this file 
        validator = Thread(target=self.validator)
        validator.start()
        #wait the process to finish before continue to the next steps 
        validator.join()

        # #Check if thew vcf file is validated
        if(self.is_validated):
            
            threads = []

            sanitycheck = Thread(target=self.sanitycheck)
            sanitycheck.start()
            # #wait till finish to continue
            sanitycheck.join()

        #     #annovar = Thread(target=self.annovar)
        #     #threads.append(annovar)            

            snpeff = Thread(target=self.snpeff)
            threads.append(snpeff)

            vep = Thread(target=self.vep)
            threads.append(vep)

            hi_index = Thread(target=self.hi_index)
            threads.append(hi_index)
            
            hgmd = Thread(target=self.hgmd)
            threads.append(hgmd)

            snpsift = Thread(target=self.snpsift) #took 0:17:40.699580
            threads.append(snpsift)

            vcf_annotator = Thread(target=self.vcf_annotator) #took 0:17:40.699580
            threads.append(vcf_annotator)

            cadd_vest = Thread(target=self.cadd_vest) #took 0:17:40.699580
            threads.append(cadd_vest)
 

            
        #     # hpg_variant = Thread(target=self.hpg_variant) #1:16:52.805209
        #     # threads.append(hpg_variant)

        #     # sift_web =Thread(target=self.sift_web) #still needs validation
        #     # threads.append(sift_web)
            
            #execute all tasks in parallel
            for thread in threads:
                thread.start()
                #thread.join()#this ption to make it serial
            
            for thread in threads:
                thread.join()

            merge = Thread(target=self.merge)
            merge.start()
            # #wait till finish to continue
            merge.join()
            

            
            print("Annotation Completed!.")
            tend = datetime.now()
            execution_time = tend -  tstart
            # logging.info('Finished Annotation, it took %s' % (execution_time))
            print('Finished Annotation, it took %s' % (execution_time))

        #     print 'Delete ann'
        #     print os.getcwd()
            #remove folder
            # if options.delete_ann:
            #     command = 'rm -rf ../ann'
            #     self.shell(command)


    def log_message(self, message):
        print(message)
        # logging.info(message)
    def shell(self, command):
        # logging.info('Running Command %s' % (command))
        # logging.info('OS CWD: %s' % (os.getcwd()))
        print('Running Command %s' % (command))
        # print 'OS CWD: %s' % (os.getcwd())
        
        try:
            p = subprocess.check_output(command, 
            cwd=os.getcwd(), 
            shell=True)
            # logging.info('Command Output: %s' % (p))
        except subprocess.CalledProcessError as e:
            print('CalledProcessError:', e)

    #if can validate return True else return False
    def validator(self):
        """
        VCF Validator

        """
        #calculate time thread took to finish
        # logging.info('Starting VCF Validator...')
        # print 'Starting VCF Validator...'
        tstart = datetime.now()
        # print os.getcwd()
        command = 'python %s/validator.py -i %s 2>log/validator.log' % (scripts_dir, self.vcffile)
        
        # logging.info('Running Command %s' % (command))
        # logging.info('OS CWD: %s' % (os.getcwd()))
        print('Running Command %s' % (command))

        try:
            p = subprocess.check_output(command, 
            cwd=os.getcwd(), 
            shell=True)
            # print p
            # logging.info('Validation Output: %s' % (p))
            self.is_validated = True

        except subprocess.CalledProcessError as e:
            print('CalledProcessError:', e)
            print('This VCF Could not be Validated!')

        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished VCF Validator, it took %s' % (execution_time))

    def sanitycheck(self):
        """
        Search and Remove variants with [0/0, ./.]
        Search and Replace chr from the beggining of the chromossomes to get positionning.    
        Sort VCF by 1...22, X, Y, MT and nothing else
        #Discard other variants
        """
        #logging.info('Starting Sanity Check...')
        tstart = datetime.now()

        command = 'python %s/sanity_check.py -i %s' % (scripts_dir, self.vcffile)
        
        self.shell(command)
        
        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished Sanity Check, it took %s' % (execution_time))

    def annovar(self):
        """Annovar 2013-06-21 11:32:41 -0700 (Fri, 21 Jun 2013)  $"""
        #calculate time thread took to finish
        #logging.info('Starting Annovar 2013-06-21 11:32:41 -0700 (Fri, 21 Jun 2013) ')
        tstart = datetime.now()
        
        command = 'python %s/annovar.py -i sanity_check/checked.vcf 2>log/annovar.log' % (scripts_dir)
        self.shell(command)

        #zip and move annovar annotation
        command = 'zip annovar.hg19.csv.zip annovar/sorted.hg19_multianno.csv'
        os.system(command)


        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished annovar, it took %s' % (execution_time))
        print('Finished annovar, it took %s' % (execution_time))


    def snpeff(self):
        """
        Annotation with snpEff 
        """        
        #calculate time thread took to finish
        #logging.info('Starting snpEff')
        tstart = datetime.now()

        command = 'python %s/snpeff.py -i sanity_check/checked.vcf 2>log/snpeff.log' % (scripts_dir)        
        self.shell(command)
        
        # command = 'cat snpeff/snpeffgatkreport.log >>log/snpeff.log'
        # os.system(command)

        # command = 'mv snpeff/snpEff_summary.html reports/'
        # os.system(command)
        

        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished snpEff, it took %s' % (execution_time))
        print('Finished snpEff, it took %s' % (execution_time))

        #subprocess.call(args)

    def vep(self):
        """VEP"""
        
        #calculate time thread took to finish
        #logging.info('Starting VEP ')
        tstart = datetime.now()
        
        command = 'python %s/vep.py -i sanity_check/checked.vcf' % (scripts_dir)
        self.shell(command)

        command = 'mv vep/vep.log log/'
        os.system(command)
        
        command = 'mv vep/vep.output.vcf_summary.html reports/vep_summary.html'
        os.system(command)

        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished VEP, it took %s' % (execution_time))
        print('Finished VEP, it took %s' % (execution_time))
    
   
    def hi_index(self):
        """Hi Index """

        
        #calculate time thread took to finish
        #logging.info('Starting HI score')
        tstart = datetime.now()
        
        command = 'python %s/hi_index.py -i sanity_check/checked.vcf' % (scripts_dir)
        self.shell(command)


        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished HI Score, it took %s' % (execution_time))
        print('Finished Hi Index, it took %s' % (execution_time))

    def hgmd(self):
        """Hi Index """

        
        #calculate time thread took to finish
        #logging.info('Starting HI score')
        tstart = datetime.now()
        
        command = 'python %s/hgmd.py -i sanity_check/checked.vcf' % (scripts_dir)
        self.shell(command)


        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished HI Score, it took %s' % (execution_time))
        print('Finished HGMD, it took %s' % (execution_time))
        
   
    def merge(self):

        print("Merging all VCF Files...")
        t_merge_start = datetime.now()
        # # #merge VCF Files
        command = 'python %s/merge.py -i sanity_check/checked.vcf' % (scripts_dir)
        self.shell(command)

        t_merge_end = datetime.now()
        execution_time = t_merge_end -  t_merge_start

        # logging.info('Finished Merging VCF, it took %s' % (execution_time))
        print('Finished Merging VCF, it took %s' % (execution_time))
        
        #compress annotation file to save space
        # command = '%s/bgzip merge/annotation.final.vcf' % (tabix_path)
        # os.system(command)

        #move final file one up and delete folder!
        command = 'mv merge/annotation.final.vcf .'
        os.system(command)

    def snpsift(self):
        """SnpSift"""
        
        tstart = datetime.now()
        
        command = 'python %s/snpsift.py -i sanity_check/checked.vcf 2>log/snpsift.log' % (scripts_dir)
        self.shell(command)

        
        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished annovar, it took %s' % (execution_time))
        print('Finished snpsift, it took %s' % (execution_time))

    def vcf_annotator(self):
        """Vcf annotator"""
        
        tstart = datetime.now()

        #python ../scripts/annotate_vcfs.py -i mm13173_14.ug.target1.vcf -r 1000genomes dbsnp138 clinvar esp6500 -a ../data/1000genomes/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz ../data/dbsnp138/00-All.vcf.gz ../data/dbsnp138/clinvar_00-latest.vcf.gz ../data/ESP6500/ESP6500.vcf.gz

        command = 'python %s/vcf_annotator_parallel.py -n %s -i sanity_check/checked.vcf -r 1000genomes dbsnp clinvar esp6500 -a %s %s %s %s 2>log/pynnotator.log' % (scripts_dir, pynnotator_cores, genomes1k, dbsnp, clinvar, esp)
        self.shell(command)
        
        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished annovar, it took %s' % (execution_time))
        print('Finished vcf_annotator, it took %s' % (execution_time))
    def cadd_vest(self):
        """CADD VEST"""
        
        tstart = datetime.now()

        #python ../scripts/annotate_vcfs.py -i mm13173_14.ug.target1.vcf -r 1000genomes dbsnp138 clinvar esp6500 -a ../data/1000genomes/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz ../data/dbsnp138/00-All.vcf.gz ../data/dbsnp138/clinvar_00-latest.vcf.gz ../data/ESP6500/ESP6500.vcf.gz

        command = 'python %s/cadd_vest_parallel.py -n %s -i sanity_check/checked.vcf 2>log/cadd_vest.log' % (scripts_dir, cadd_vest_cores)
        self.shell(command)
        
        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished annovar, it took %s' % (execution_time))
        print('Finished CADD VEST, it took %s' % (execution_time))



if __name__=="__main__":
    a = Annotator(args.vcffile)
    a.run()

