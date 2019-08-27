#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from threading import Thread

from . import settings
from .helpers import validator, sanity_check, snpeff, vep, decipher, snpsift, vcf_annotator, dbnsfp, merge, hgmd

import logging

# add Python2 compatibility
# http://stackoverflow.com/questions/25156768/cant-pickle-type-instancemethod-using-pythons-multiprocessing-pool-apply-a

if sys.version_info[0] < 3:
    import copy_reg
    import types

    def _pickle_method(m):
        if m.im_self is None:
            return getattr, (m.im_class, m.im_func.func_name)
        else:
            return getattr, (m.im_self, m.im_func.func_name)


    copy_reg.pickle(types.MethodType, _pickle_method)


## end of python2 compatibility        


class Annotator(object):
    is_validated = False

    def __init__(self, vcf_file=None):

        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]

        self.vcf_file = os.path.abspath(vcf_file)

        # this is used to create the folder with the right name
        self.filename = self.filename.replace('.vcf.gz', '').replace('.vcf', '')

        logging.basicConfig(filename='%s.log' % (self.filename) ,level=logging.DEBUG)

        # create a folder for the annotation if it doesn't exists, 
        # or delete and create if the folder already exists
        self.ann_name = "ann_%s" % (self.filename)

        #delete folder
        if os.path.exists(self.ann_name):
            shutil.rmtree(self.ann_name)

        os.makedirs(self.ann_name)
        os.chdir(self.ann_name)

    def run(self):

        tstart = datetime.now()

        if self.vcf_file.endswith('.vcf.gz'):
            path = os.path.dirname(self.vcf_file)
            new_name = '%s/%s/%s.vcf' % (path, self.ann_name, self.filename)
            command = 'gunzip -c -d %s > %s' % (self.vcf_file, new_name)
            self.shell(command)
            self.vcf_file = new_name
        else:
            path = os.path.dirname(self.vcf_file)
            new_name = '%s/%s/%s.vcf' % (path, self.ann_name, self.filename)
            command = 'cp %s %s' % (self.vcf_file, new_name)
            self.shell(command)
            self.vcf_file = new_name

        # run vcftools vcf-validator on this file 
        # validator = Thread(target=self.validator)
        # validator.start()
        # # wait the process to finish before continue to the next steps 
        # validator.join()

        # #Check if the vcf file is validated
        # if(self.is_validated):#

        threads = []

        sanitycheck = Thread(target=self.sanitycheck)
        sanitycheck.start()
        # #wait till finish to continue
        sanitycheck.join()

        self.vcf_file = 'sanity_check/sorted.vcf'

        snpeff = Thread(target=self.snpeff)
        threads.append(snpeff)

        vep = Thread(target=self.vep)
        threads.append(vep)

        decipher = Thread(target=self.decipher)
        threads.append(decipher)

        # hgmd = Thread(target=self.hgmd)
        # threads.append(hgmd)        

        snpsift = Thread(target=self.snpsift)
        threads.append(snpsift)

        # vcf_annotator = Thread(target=self.vcf_annotator)
        # threads.append(vcf_annotator)

        # dbnsfp = Thread(target=self.dbnsfp)  # took 0:17:40.699580
        # threads.append(dbnsfp)

        # execute all tasks in parallel
        for thread in threads:
            thread.start()
            # thread.join()#this option to make it serial

        for thread in threads:
            thread.join()

        merge = Thread(target=self.merge)
        merge.start()
        # #wait till finish to continue
        merge.join()

        vcf2csv = Thread(target=self.vcf2csv)
        vcf2csv.start()
        # #wait till finish to continue
        vcf2csv.join()


        time_end = datetime.now()
        # print(time_end, "Annotation Completed!")
        tend = datetime.now()
        execution_time = tend - tstart
        # logging.info('Finished Annotation, it took %s' % (execution_time))
        print(time_end, 'Finished Annotation, it took %s' % (execution_time))

        output = """
A       A G       T G       A       A G       T G       A
| C   C | | C   C | | A   C | C   C | | C   C | | A   C |
| | T | | | | A | | | | G | | | T | | | | A | | | | G | |
| G   G | | G   G | | T   G | G   G | | G   G | | T   G |
T       T C       A C       T       T C       A C       T
"""
        print(output)

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
            logging.info('Command Output: %s' % (p))
        except subprocess.CalledProcessError as e:
            print('CalledProcessError:', e)
            logging.info('Command Error: %s' % (e))

    # if can validate return True else return False
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
        execution_time = tend - tstart

    def sanitycheck(self):
        """
        Search and Remove variants with [0/0, ./.]
        Search and Replace chr from the beggining of the chromossomes to get positionning.    
        Sort VCF by 1...22, X, Y, MT and nothing else
        #Discard other variants
        """
        # logging.info('Starting Sanity Check...')
        tstart = datetime.now()

        # command = 'python %s/sanity_check.py -i %s' % (scripts_dir, self.vcf_file)
        # self.shell(command)

        sc = sanity_check.Sanity_check(self.vcf_file)
        std = sc.run()

        tend = datetime.now()
        execution_time = tend - tstart
        # logging.info('Finished Sanity Check, it took %s' % (execution_time))

    def snpeff(self):
        """
        Annotation with snpEff 
        """
        # calculate time thread took to finish
        # logging.info('Starting snpEff')
        tstart = datetime.now()

        se = snpeff.Snpeff(self.vcf_file)
        std = se.run()

        tend = datetime.now()
        execution_time = tend - tstart
        # logging.info('Finished snpEff, it took %s' % (execution_time))
        # print(tend, 'Finished snpEff, it took %s' % (execution_time))

        # subprocess.call(args)

    def vep(self):
        """VEP"""

        # calculate time thread took to finish
        # logging.info('Starting VEP ')
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
        execution_time = tend - tstart
        # logging.info('Finished VEP, it took %s' % (execution_time))
        # print(tend, 'Finished VEP, it took %s' % (execution_time))

    def decipher(self):
        """Decipher """

        # calculate time thread took to finish
        # logging.info('Starting HI score')
        tstart = datetime.now()

        decipher_obj = decipher.Decipher(self.vcf_file)
        decipher_obj.run()

        tend = datetime.now()
        execution_time = tend - tstart
        # logging.info('Finished HI Score, it took %s' % (execution_time))
        # print(tend, 'Finished Decipher, it took %s' % (execution_time))

    def hgmd(self):
        """Hi Index """

        # calculate time thread took to finish
        # logging.info('Starting HI score')
        tstart = datetime.now()


        if os.path.isfile(settings.hgmd_file): 

            hgmd_obj = hgmd.HGMD(self.vcf_file)
            hgmd_obj.run()

        tend = datetime.now()
        execution_time = tend - tstart
        # logging.info('Finished HI Score, it took %s' % (execution_time))
        # print('Finished HGMD, it took %s' % (execution_time))

    def merge(self):

        tstart = datetime.now()
        print(tstart, "Merging all VCF Files...")
        t_merge_start = datetime.now()
        # # #merge VCF Files
        # command = 'python %s/merge.py -i sanity_check/checked.vcf' % (scripts_dir)
        # self.shell(command)
        mg = merge.Merge(self.vcf_file)
        mg.run()

        t_merge_end = datetime.now()
        execution_time = t_merge_end - t_merge_start

    def vcf2csv(self):

        tstart = datetime.now()
        print(tstart, "Convert VCF to CSV...")
        t_vcf2csv_start = datetime.now()
        # # #merge VCF Files
        command = 'python %s/scripts/vcf2csv.py -v ../annotation.final.vcf' % (settings.BASE_DIR)
        # command = 'pwd'
        subprocess.call(command, shell=True)
        
        t_vcf2csv_end = datetime.now()
        execution_time = t_vcf2csv_end - t_vcf2csv_start

    def snpsift(self):
        """SnpSift"""

        tstart = datetime.now()

        # command = 'python %s/snpsift.py -i sanity_check/checked.vcf 2>log/snpsift.log' % (scripts_dir)
        # self.shell(command)

        ss = snpsift.SnpSift(self.vcf_file)
        ss.run()

        tend = datetime.now()
        execution_time = tend - tstart
        # logging.info('Finished annovar, it took %s' % (execution_time))
        # print(tend, 'Finished snpsift, it took %s' % (execution_time))

    def vcf_annotator(self):
        """Vcf annotator"""

        tstart = datetime.now()

        # python ../scripts/annotate_vcfs.py -i mm13173_14.ug.target1.vcf -r 1000genomes dbsnp138 clinvar esp6500 -a ../data/1000genomes/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz ../data/dbsnp138/00-All.vcf.gz ../data/dbsnp138/clinvar_00-latest.vcf.gz ../data/ESP6500/ESP6500.vcf.gz

        # command = 'python %s/vcf_annotator_parallel.py -n %s -i sanity_check/checked.vcf -r 1000genomes dbsnp clinvar esp6500 -a %s %s %s %s 2>log/pynnotator.log' % (scripts_dir, pynnotator_cores, genomes1k, dbsnp, clinvar, esp)
        # self.shell(command)

        resources = "genomes1k dbsnp clinvar esp6500 ensembl_phen ensembl_clin hgmd"  # 
        resources = resources.split(' ')
        annfiles = [
            "%s/1000genomes/%s" % (settings.data_dir, settings.genomes1k_file),
            "%s/dbsnp/%s" % (settings.data_dir, settings.dbsnp_file),
            "%s/dbsnp/%s" % (settings.data_dir, settings.clinvar_file),
            "%s/esp6500/%s" % (settings.data_dir, settings.esp_final_file),
            "%s/ensembl/%s" % (settings.data_dir, settings.ensembl_phenotype_file),
            "%s/ensembl/%s" % (settings.data_dir, settings.ensembl_clinically_file),
        ]

        if os.path.exists(settings.hgmd):
            annfiles.append("%s/hgmd/%s" % (settings.data_dir, settings.hgmd),)
        #



        # annfiles = " ".join(annfiles)
        # annfiles = ["%s/1000genomes/%s" % (settings.data_dir, settings.genomes1k_file)]

        annotator_obj = vcf_annotator.VCF_Annotator(self.vcf_file, annfiles, resources, settings.vcf_annotator_cores)

        annotator_obj.run()

        tend = datetime.now()
        execution_time = tend - tstart
        # logging.info('Finished annovar, it took %s' % (execution_time))
        # print(tend, 'Finished vcf_annotator, it took %s' % (execution_time))

    def dbnsfp(self):
        """dbnsfp"""

        tstart = datetime.now()

        # python ../scripts/annotate_vcfs.py -i mm13173_14.ug.target1.vcf -r 1000genomes dbsnp138 clinvar esp6500 -a ../data/1000genomes/ALL.wgs.integrated_phase1_v3.20101123.snps_indels_sv.sites.vcf.gz ../data/dbsnp138/00-All.vcf.gz ../data/dbsnp138/clinvar_00-latest.vcf.gz ../data/ESP6500/ESP6500.vcf.gz

        # command = 'python %s/cadd_dann.py -n %s -i sanity_check/checked.vcf 2>log/cadd_dann.log' % (scripts_dir, cadd_vest_cores)
        # self.shell(command)
        db = dbnsfp.Dbnsfp(self.vcf_file, settings.dbnsfp_cores)
        db.run()

        tend = datetime.now()
        execution_time = tend - tstart
        # logging.info('Finished annovar, it took %s' % (execution_time))
        # print(tend, 'Finished Func Pred, it took %s' % (execution_time))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Annotate a VCF File with Annotator.')
    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')
    args = parser.parse_args()

    a = Annotator(args.vcf_file)
    a.run()
