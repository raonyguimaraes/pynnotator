
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

        # print   'func pred'
        
        # print('merge cadd_dann')
        #cadd_dann
        command = "java -Xmx%s -jar \
        %s/SnpSift.jar \
        annotate -noId -info dbNSFP_SIFT_score,dbNSFP_SIFT_converted_rankscore,dbNSFP_SIFT_pred,dbNSFP_Uniprot_acc_Polyphen2,dbNSFP_Uniprot_id_Polyphen2,dbNSFP_Uniprot_aapos_Polyphen2,dbNSFP_Polyphen2_HDIV_score,dbNSFP_Polyphen2_HDIV_rankscore,dbNSFP_Polyphen2_HDIV_pred,dbNSFP_Polyphen2_HVAR_score,dbNSFP_Polyphen2_HVAR_rankscore,dbNSFP_Polyphen2_HVAR_pred,dbNSFP_LRT_score,dbNSFP_LRT_converted_rankscore,dbNSFP_LRT_pred,dbNSFP_LRT_Omega,dbNSFP_MutationTaster_score,dbNSFP_MutationTaster_converted_rankscore,dbNSFP_MutationTaster_pred,dbNSFP_MutationTaster_model,dbNSFP_MutationTaster_AAE,dbNSFP_MutationAssessor_UniprotID,dbNSFP_MutationAssessor_variant,dbNSFP_MutationAssessor_score,dbNSFP_MutationAssessor_rankscore,dbNSFP_MutationAssessor_pred,dbNSFP_FATHMM_score,dbNSFP_FATHMM_converted_rankscore,dbNSFP_FATHMM_pred,dbNSFP_PROVEAN_score,dbNSFP_PROVEAN_converted_rankscore,dbNSFP_PROVEAN_pred,dbNSFP_Transcript_id_VEST3,dbNSFP_Transcript_var_VEST3,dbNSFP_VEST3_score,dbNSFP_VEST3_rankscore,dbNSFP_MetaSVM_score,dbNSFP_MetaSVM_rankscore,dbNSFP_MetaSVM_pred,dbNSFP_MetaLR_score,dbNSFP_MetaLR_rankscore,dbNSFP_MetaLR_pred,dbNSFP_Reliability_index,dbNSFP_CADD_raw,dbNSFP_CADD_raw_rankscore,dbNSFP_CADD_phred,dbNSFP_DANN_score,dbNSFP_DANN_rankscore,dbNSFP_fathmm,dbNSFP_fathmm,dbNSFP_fathmm,dbNSFP_fathmm,dbNSFP_Eigen,dbNSFP_Eigen,dbNSFP_Eigen,dbNSFP_Eigen,dbNSFP_Eigen,dbNSFP_GenoCanyon_score,dbNSFP_GenoCanyon_score_rankscore,dbNSFP_integrated_fitCons_score,dbNSFP_integrated_fitCons_rankscore,dbNSFP_integrated_confidence_value,dbNSFP_GM12878_fitCons_score,dbNSFP_GM12878_fitCons_rankscore,dbNSFP_GM12878_confidence_value,dbNSFP_H1,dbNSFP_H1,dbNSFP_H1,dbNSFP_HUVEC_fitCons_score,dbNSFP_HUVEC_fitCons_rankscore,dbNSFP_HUVEC_confidence_value,dbNSFP_GERP,dbNSFP_GERP,dbNSFP_GERP,dbNSFP_phyloP100way_vertebrate,dbNSFP_phyloP100way_vertebrate_rankscore,dbNSFP_phyloP20way_mammalian,dbNSFP_phyloP20way_mammalian_rankscore,dbNSFP_phastCons100way_vertebrate,dbNSFP_phastCons100way_vertebrate_rankscore,dbNSFP_phastCons20way_mammalian,dbNSFP_phastCons20way_mammalian_rankscore,dbNSFP_SiPhy_29way_pi,dbNSFP_SiPhy_29way_logOdds,dbNSFP_SiPhy_29way_logOdds_rankscore,dbNSFP_clinvar_rs,dbNSFP_clinvar_clnsig,dbNSFP_clinvar_trait,dbNSFP_clinvar_golden_stars \
        ../func_pred/func_pred.vcf \
        1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf \
        > func_pred.1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf  \
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
        func_pred.1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf \
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