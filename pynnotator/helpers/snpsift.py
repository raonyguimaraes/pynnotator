#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
import csv

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with Snpsift.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

args = parser.parse_args()

class SnpSift(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        
        #create folder snpeff if it doesn't exists
        if not os.path.exists('snpsift'):
            os.makedirs('snpsift')
        #enter inside folder
        # os.chdir('snpsift')
        
    
    def run(self):
        tstart = datetime.now()
        print tstart, 'Starting snpsift annotation: ', self.vcffile
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print tend, 'Finished snpsift annotation, it took: ', annotation_time        


    #convert and annotate the vcf file to snpeff
    def annotate(self):
        
         
        # BASE_DIR = os.getcwd()
        #print BASE_DIR
        
        #dbNFSP
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar dbnsfp \
        -f Uniprot_acc,Uniprot_id,Uniprot_aapos,Interpro_domain,cds_strand,refcodon,SLR_test_statistic,codonpos,fold-degenerate,Ancestral_allele,Ensembl_geneid,Ensembl_transcriptid,aapos,aapos_SIFT,aapos_FATHMM,SIFT_score,SIFT_converted_rankscore,SIFT_pred,Polyphen2_HDIV_score,Polyphen2_HDIV_rankscore,Polyphen2_HDIV_pred,Polyphen2_HVAR_score,Polyphen2_HVAR_rankscore,Polyphen2_HVAR_pred,LRT_score,LRT_converted_rankscore,LRT_pred,MutationTaster_score,MutationTaster_converted_rankscore,MutationTaster_pred,MutationAssessor_score,MutationAssessor_rankscore,MutationAssessor_pred,FATHMM_score,FATHMM_rankscore,FATHMM_pred,RadialSVM_score,RadialSVM_rankscore,RadialSVM_pred,LR_score,LR_rankscore,LR_pred,Reliability_index,VEST3_score,VEST3_rankscore,CADD_raw,CADD_raw_rankscore,CADD_phred,GERP++_NR,GERP++_RS,GERP++_RS_rankscore,phyloP46way_primate,phyloP46way_primate_rankscore,phyloP46way_placental,phyloP46way_placental_rankscore,phyloP100way_vertebrate,phyloP100way_vertebrate_rankscore,phastCons46way_primate,phastCons46way_primate_rankscore,phastCons46way_placental,phastCons46way_placental_rankscore,phastCons100way_vertebrate,phastCons100way_vertebrate_rankscore,SiPhy_29way_pi,SiPhy_29way_logOdds,SiPhy_29way_logOdds_rankscore,LRT_Omega,UniSNP_ids,1000Gp1_AC,1000Gp1_AF,1000Gp1_AFR_AC,1000Gp1_AFR_AF,1000Gp1_EUR_AC,1000Gp1_EUR_AF,1000Gp1_AMR_AC,1000Gp1_AMR_AF,1000Gp1_ASN_AC,1000Gp1_ASN_AF,ESP6500_AA_AF,ESP6500_EA_AF \
        -db %s \
        %s \
        > snpsift/dbnfsp.vcf \
        "% (java_path, snpsift_dir, dbnsfp, self.vcffile)

        # print command
        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        # if p == 0:
        #     print 'This vcf was annotated by snpsift with Success'
        # else:
        #     print 'Sorry this vcf could not be anotated by snpsift'

        

        # 
        # By default it adds ALL database INFO fields.
        # You can use the '-info' command line option if you only want select only a subset of fields from db.vcf file.
        
        #Annotate with 1000genomes
        # command = "java -Xmx40G -jar \
        # %s/SnpSift.jar \
        # annotate -name 1000genomes. \
        # %s \
        # %s \
        # > snpsift/1000genomes.vcf \
        # "% (snpsift_dir, genomes1k, self.vcffile)
        
        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        # #Annotate with dbsnp138
        # command = "java -Xmx40G -jar \
        # %s/SnpSift.jar \
        # annotate \
        # %s \
        # %s.1000genomes.vcf \
        # > %s.1000genomes.dbsnp138.vcf \
        # "% (snpsift_dir, dbsnp, self.filename, self.filename)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        # #Annotate with clinvar
        # command = "java -Xmx40G -jar \
        # %s/SnpSift.jar \
        # annotate \
        # %s \
        # %s.1000genomes.dbsnp138.vcf \
        # > %s.1000genomes.dbsnp138.clinvar.vcf \
        # "% (snpsift_dir, clinvar, self.filename, self.filename)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        # #Annotate with ESP6500
        # command = "java -Xmx40G -jar \
        # %s/SnpSift.jar \
        # annotate \
        # %s \
        # %s.1000genomes.dbsnp138.clinvar.vcf \
        # > %s.1000genomes.dbsnp138.clinvar.esp.vcf \
        # "% (snpsift_dir, esp, self.filename, self.filename)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        #VARTYPE
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar \
        varType \
       %s \
        > snpsift/snpsift.final.vcf \
        "% (java_path, snpsift_dir, self.vcffile)

        # print 'vartype', command

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        #java -jar SnpSift.jar   test.vcf | grep -v "^#" | head


        #-info OM #to annotate all things from first VCF file
        # print command


        #annotate mutations present at omim from clinvar_00-latest.vcf 42109 mutations
        # command = "java -Xmx40G -jar \
        # %s/SnpSift.jar \
        # annotate \
        # %s/../dbsnp138/clinvar_00-latest.vcf \
        # ../%s \
        # > clinvar.vcf \
        # "% (snpsift_dir, snpsift_dir, self.vcffile)
        # #-info OM #to annotate all things from first VCF file
        # # print command

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)
        # if p == 0:
        #     print 'This vcf was annotated by snpsift and clinvar with success'
        # else:
        #     print 'Sorry this vcf could not be anotated by snpsift'



if  __name__ == '__main__' :
    snpsift = SnpSift(args.vcffile)
    snpsift.run()