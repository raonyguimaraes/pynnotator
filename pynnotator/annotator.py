#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import time
from datetime import datetime

import csv
import shutil
import shlex, subprocess

from threading import Thread

from pynnotator import settings

from .helpers import validator, sanity_check, snpeff, vep, hi_index, snpsift, vcf_annotator, func_pred, merge

class Annotator(object):

    is_validated = False

    def __init__(self, vcf_file=None):
        
        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]

        # create a folder for the annotation if it doesn't exists, 
        # or delete and create if the folder already exists
        ann_name = "ann_%s" % (self.filename)

        self.vcf_file = os.path.abspath(vcf_file)
        
        if os.path.exists(ann_name):
            shutil.rmtree(ann_name)

        os.makedirs(ann_name)
        os.chdir(ann_name)
        #copy vcf to ann folder and rewrite self.vcf_file
        
        print('vcf_file', self.vcf_file)
        # os.path.basename(str(vcf_file))
        
        # os.makedirs('log')
        # os.makedirs('reports')




    def run(self):
        
        tstart = datetime.now()

        #run vcftools vcf-validator on this file 
        validator = Thread(target=self.validator)
        validator.start()
        #wait the process to finish before continue to the next steps 
        validator.join()

        # #Check if thew vcf file is validated
        if(self.is_validated):#
            
            threads = []

            sanitycheck = Thread(target=self.sanitycheck)
            sanitycheck.start()
            # #wait till finish to continue
            sanitycheck.join()

            self.vcf_file = 'sanity_check/checked.vcf'

            snpeff = Thread(target=self.snpeff)
            threads.append(snpeff)

            vep = Thread(target=self.vep)
            threads.append(vep)

            hi_index = Thread(target=self.hi_index)
            threads.append(hi_index)

            snpsift = Thread(target=self.snpsift)
            threads.append(snpsift)

            vcf_annotator = Thread(target=self.vcf_annotator)
            threads.append(vcf_annotator)

            func_pred = Thread(target=self.func_pred) #took 0:17:40.699580
            threads.append(func_pred)

            #execute all tasks in parallel
            for thread in threads:
                thread.start()
                #thread.join()#this option to make it serial
            
            for thread in threads:
                thread.join()

            merge = Thread(target=self.merge)
            merge.start()
            # #wait till finish to continue
            merge.join()
            
            print("Annotation Completed!")
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
        tstart = datetime.now()
        v = validator.Validator(self.vcf_file)
        std = v.run()
        if std == 0:
            self.is_validated = True

        tend = datetime.now()
        execution_time = tend -  tstart
        
    def sanitycheck(self):
        """
        Search and Remove variants with [0/0, ./.]
        Search and Replace chr from the beggining of the chromossomes to get positionning.    
        Sort VCF by 1...22, X, Y, MT and nothing else
        #Discard other variants
        """
        #logging.info('Starting Sanity Check...')
        tstart = datetime.now()

        # command = 'python %s/sanity_check.py -i %s' % (scripts_dir, self.vcf_file)
        # self.shell(command)

        sc = sanity_check.Sanity_check(self.vcf_file)
        std = sc.run()
        
        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished Sanity Check, it took %s' % (execution_time))

    def snpeff(self):
        """
        Annotation with snpEff 
        """        
        #calculate time thread took to finish
        #logging.info('Starting snpEff')
        tstart = datetime.now()

        se = snpeff.Snpeff(self.vcf_file)
        std = se.run()

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

        vep_obj = vep.Vep(self.vcf_file)
        std = vep_obj.run()
        
        # command = 'python %s/vep.py -i sanity_check/checked.vcf' % (scripts_dir)
        # self.shell(command)

        # command = 'mv vep/vep.log log/'
        # os.system(command)
        
        # command = 'mv vep/vep.output.vcf_summary.html reports/vep_summary.html'
        # os.system(command)

        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished VEP, it took %s' % (execution_time))
        print('Finished VEP, it took %s' % (execution_time))
    
   
    def hi_index(self):
        """Hi Index """

        
        #calculate time thread took to finish
        #logging.info('Starting HI score')
        tstart = datetime.now()
        
        # command = 'python %s/hi_index.py -i sanity_check/checked.vcf' % (scripts_dir)
        # self.shell(command)

        hi = hi_index.HI_Index(self.vcf_file)
        hi.run()

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
        # command = 'python %s/merge.py -i sanity_check/checked.vcf' % (scripts_dir)
        # self.shell(command)
        mg = merge.Merge(self.vcf_file)
        mg.run()

        t_merge_end = datetime.now()
        execution_time = t_merge_end -  t_merge_start

        # logging.info('Finished Merging VCF, it took %s' % (execution_time))
        print('Finished Merging VCF, it took %s' % (execution_time))
        
        #compress annotation file to save space
        # command = '%s/bgzip merge/annotation.final.vcf' % (tabix_path)
        # os.system(command)
        # print('before merge', os.getcwd())
        #move final file one up and delete folder!
        command = 'mv annotation.final.vcf ../'
        os.system(command)

    def snpsift(self):
        """SnpSift"""
        
        tstart = datetime.now()
        
        # command = 'python %s/snpsift.py -i sanity_check/checked.vcf 2>log/snpsift.log' % (scripts_dir)
        # self.shell(command)

        ss = snpsift.SnpSift(self.vcf_file)
        ss.run()

        
        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished annovar, it took %s' % (execution_time))
        print('Finished snpsift, it took %s' % (execution_time))

    def vcf_annotator(self):
        """Vcf annotator"""
        
        tstart = datetime.now()

        #python ../scripts/annotate_vcfs.py -i mm13173_14.ug.target1.vcf -r 1000genomes dbsnp138 clinvar esp6500 -a ../data/1000genomes/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz ../data/dbsnp138/00-All.vcf.gz ../data/dbsnp138/clinvar_00-latest.vcf.gz ../data/ESP6500/ESP6500.vcf.gz

        # command = 'python %s/vcf_annotator_parallel.py -n %s -i sanity_check/checked.vcf -r 1000genomes dbsnp clinvar esp6500 -a %s %s %s %s 2>log/pynnotator.log' % (scripts_dir, pynnotator_cores, genomes1k, dbsnp, clinvar, esp)
        # self.shell(command)

        resources = "genomes1k dbsnp clinvar esp6500 ensembl_phen ensembl_clin"#    
        resources = resources.split(' ')
        annfiles = [
        "%s/1000genomes/%s" % (settings.data_dir, settings.genomes1k_file),
        "%s/dbsnp/%s" % (settings.data_dir, settings.dbsnp_file),
        "%s/dbsnp/%s" % (settings.data_dir, settings.clinvar_file),
        "%s/esp6500/%s" % (settings.data_dir, settings.esp_final_file),
        "%s/ensembl/%s" % (settings.data_dir, settings.ensembl_phenotype_file),
        "%s/ensembl/%s" % (settings.data_dir, settings.ensembl_clinically_file),
        ]
        #
 


        # annfiles = " ".join(annfiles)

        # annfiles = ["%s/1000genomes/%s" % (settings.data_dir, settings.genomes1k_file)]

        annotator_obj =  vcf_annotator.VCF_Annotator(self.vcf_file, annfiles, resources, settings.vcf_annotator_cores)

        annotator_obj.run()
        
        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished annovar, it took %s' % (execution_time))
        print('Finished vcf_annotator, it took %s' % (execution_time))
    def func_pred(self):
        """func_pred"""
        
        tstart = datetime.now()

        #python ../scripts/annotate_vcfs.py -i mm13173_14.ug.target1.vcf -r 1000genomes dbsnp138 clinvar esp6500 -a ../data/1000genomes/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz ../data/dbsnp138/00-All.vcf.gz ../data/dbsnp138/clinvar_00-latest.vcf.gz ../data/ESP6500/ESP6500.vcf.gz

        # command = 'python %s/cadd_dann.py -n %s -i sanity_check/checked.vcf 2>log/cadd_dann.log' % (scripts_dir, cadd_vest_cores)
        # self.shell(command)
        fp = func_pred.FUNC_PRED_Annotator(self.vcf_file, settings.func_pred_cores)
        fp.run()
        
        tend = datetime.now()
        execution_time = tend -  tstart
        #logging.info('Finished annovar, it took %s' % (execution_time))
        print('Finished Func Pred, it took %s' % (execution_time))



if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Annotate a VCF File with Annotator.')
    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')
    args = parser.parse_args()

    a = Annotator(args.vcf_file)
    a.run()

