
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess

from pynnotator import settings
from collections import OrderedDict

import pysam

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

        self.annotation_files = OrderedDict()

        pysam.tabix_index('../snpeff/snpeff.output.vcf', preset='vcf')

        self.annotation_files['snpeff'] = {
            'info':'EFF', 
            'file':pysam.Tabixfile('../snpeff/snpeff.output.vcf.gz', 'r' ,encoding="utf-8")
            }

        pysam.tabix_index('../vep/vep.output.sorted.vcf', preset='vcf')

        self.annotation_files['vep'] = {
            'info':'CSQ', 
            'file':pysam.Tabixfile('../vep/vep.output.sorted.vcf.gz', 'r', encoding="utf-8")
            }

        pysam.tabix_index('../snpsift/snpsift.final.vcf', preset='vcf')

        self.annotation_files['vartype'] = {
            'info':'VARTYPE,SNP,MNP,INS,DEL,MIXED,HOM,HET', 
            'file':pysam.Tabixfile('../snpsift/snpsift.final.vcf.gz', 'r', encoding="utf-8")
            }

        pysam.tabix_index('../hi_index/hi_index.vcf', preset='vcf')

        self.annotation_files['hi_index'] = {
            'info':'HI_INDEX', 
            'file':pysam.Tabixfile('../hi_index/hi_index.vcf.gz', 'r', encoding="utf-8")
            }

        pysam.tabix_index('../pynnotator/pynnotator.vcf', preset='vcf')

        #genomes1k dbsnp clinvar esp6500 ensembl_phen ensembl_clin
        self.pynnotator_tags = ['genomes1k', 'dbsnp', 'clinvar', 'esp6500', 'ensembl_phen', 'ensembl_clin']

        self.annotation_files['pynnotator'] = {
            'info':'ALL', 
            'file':pysam.Tabixfile('../pynnotator/pynnotator.vcf.gz', 'r', encoding="utf-8")
            }

        pysam.tabix_index('../func_pred/func_pred.vcf', preset='vcf')

        self.annotation_files['dbnfsp'] = {
            'info':'dbNSFP_SIFT_score,dbNSFP_SIFT_converted_rankscore,dbNSFP_SIFT_pred,dbNSFP_Uniprot_acc_Polyphen2,dbNSFP_Uniprot_id_Polyphen2,dbNSFP_Uniprot_aapos_Polyphen2,dbNSFP_Polyphen2_HDIV_score,dbNSFP_Polyphen2_HDIV_rankscore,dbNSFP_Polyphen2_HDIV_pred,dbNSFP_Polyphen2_HVAR_score,dbNSFP_Polyphen2_HVAR_rankscore,dbNSFP_Polyphen2_HVAR_pred,dbNSFP_LRT_score,dbNSFP_LRT_converted_rankscore,dbNSFP_LRT_pred,dbNSFP_LRT_Omega,dbNSFP_MutationTaster_score,dbNSFP_MutationTaster_converted_rankscore,dbNSFP_MutationTaster_pred,dbNSFP_MutationTaster_model,dbNSFP_MutationTaster_AAE,dbNSFP_MutationAssessor_UniprotID,dbNSFP_MutationAssessor_variant,dbNSFP_MutationAssessor_score,dbNSFP_MutationAssessor_rankscore,dbNSFP_MutationAssessor_pred,dbNSFP_FATHMM_score,dbNSFP_FATHMM_converted_rankscore,dbNSFP_FATHMM_pred,dbNSFP_PROVEAN_score,dbNSFP_PROVEAN_converted_rankscore,dbNSFP_PROVEAN_pred,dbNSFP_Transcript_id_VEST3,dbNSFP_Transcript_var_VEST3,dbNSFP_VEST3_score,dbNSFP_VEST3_rankscore,dbNSFP_MetaSVM_score,dbNSFP_MetaSVM_rankscore,dbNSFP_MetaSVM_pred,dbNSFP_MetaLR_score,dbNSFP_MetaLR_rankscore,dbNSFP_MetaLR_pred,dbNSFP_Reliability_index,dbNSFP_CADD_raw,dbNSFP_CADD_raw_rankscore,dbNSFP_CADD_phred,dbNSFP_DANN_score,dbNSFP_DANN_rankscore,dbNSFP_fathmm-MKL_coding_score,dbNSFP_fathmm-MKL_coding_rankscore,dbNSFP_fathmm-MKL_coding_pred,dbNSFP_fathmm-MKL_coding_group,dbNSFP_Eigen-raw,dbNSFP_Eigen-phred,dbNSFP_Eigen-raw_rankscore,dbNSFP_Eigen-PC-raw,dbNSFP_Eigen-PC-raw_rankscore,dbNSFP_GenoCanyon_score,dbNSFP_GenoCanyon_score_rankscore,dbNSFP_integrated_fitCons_score,dbNSFP_integrated_fitCons_rankscore,dbNSFP_integrated_confidence_value,dbNSFP_GM12878_fitCons_score,dbNSFP_GM12878_fitCons_rankscore,dbNSFP_GM12878_confidence_value,dbNSFP_H1-hESC_fitCons_score,dbNSFP_H1-hESC_fitCons_rankscore,dbNSFP_H1-hESC_confidence_value,dbNSFP_HUVEC_fitCons_score,dbNSFP_HUVEC_fitCons_rankscore,dbNSFP_HUVEC_confidence_value,dbNSFP_GERP++_NR,dbNSFP_GERP++_RS,dbNSFP_GERP++_RS_rankscore,dbNSFP_phyloP100way_vertebrate,dbNSFP_phyloP100way_vertebrate_rankscore,dbNSFP_phyloP20way_mammalian,dbNSFP_phyloP20way_mammalian_rankscore,dbNSFP_phastCons100way_vertebrate,dbNSFP_phastCons100way_vertebrate_rankscore,dbNSFP_phastCons20way_mammalian,dbNSFP_phastCons20way_mammalian_rankscore,dbNSFP_SiPhy_29way_pi,dbNSFP_SiPhy_29way_logOdds,dbNSFP_SiPhy_29way_logOdds_rankscore,dbNSFP_clinvar_rs,dbNSFP_clinvar_clnsig,dbNSFP_clinvar_trait,dbNSFP_clinvar_golden_stars', 
            'file':pysam.Tabixfile('../func_pred/func_pred.vcf.gz', 'r', encoding="utf-8")
            }

        self.dbsnp = pysam.Tabixfile(settings.dbsnp, 'r', encoding="utf-8")
    
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

        #get headers from files
        headers = []
        for annotation in self.annotation_files:
            # print(annotation, self.annotation_files[annotation])
            info = self.annotation_files[annotation]['info'].split(',')
            # print(info)
            ann_vcf_file = self.annotation_files[annotation]['file']

            for line in ann_vcf_file.header:

                line = line.decode('utf-8')

                # print(annotation)
                if annotation == 'pynnotator':
                    for tag in self.pynnotator_tags:
                        string = '##INFO=<ID=%s.' % (tag)
                        if line.startswith(string):
                            headers.append(line)
                else:
                    for tag in info:
                        string = '##INFO=<ID=%s,' % (tag)
                        if line.startswith(string):
                            headers.append(line)
                
        output = open('annotation.final.vcf', 'w')
        input_vcf = open('../sanity_check/checked.vcf')
        for line in input_vcf:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    #write extra header
                    for tag in headers:
                        output.writelines(tag+'\n')
                    output.writelines(line)
                else:
                    output.writelines(line)
            else:
                #here annotation comes!
                variant = line.split('\t')
                variant[0] = variant[0].replace('chr', '')
                index = '%s-%s' % (variant[0], variant[1])
                # print(variant)
                annotations = []
                for annotation in self.annotation_files:
                    info = self.annotation_files[annotation]['info'].split(',')
                    # print(info)
                    ann_vcf_file = self.annotation_files[annotation]['file']
                    try:
                        records = ann_vcf_file.fetch(variant[0], int(variant[1])-1, int(variant[1]))
                    except:
                        records = []
                    for record in records:
                        
                        ann = record.split('\t')
                        # print(ann)
                        new_info = ann[7].split(';')

                        if annotation == 'pynnotator':
                            for tag in new_info:
                                string = tag.split('=')[0].split('.')[0]
                                if string in self.pynnotator_tags:
                                    annotations.append(tag)
                        else:
                        # print(info)
                            for tag in new_info:
                                string = tag.split('=')[0]
                                if string in info:
                                    annotations.append(tag)
                        # print(annotations)
                            
                new_info = variant[7]+';'+";".join(annotations)
                # print(new_info)
                variant[7] = new_info

                #now dbsnp
                
                try:
                    records = self.dbsnp.fetch(variant[0], int(variant[1])-1, int(variant[1]))
                except:
                    records = []
                rsids = []
                for record in records:
                    # print(record, variant)
                    row = record.split('\t')
                    rsid = row[2]

                    check_flag = False
                    if variant[3] == row[3]:
                        alts = variant[4].split(',')
                        alts_row = row[4].split(',')
                        #compare ALT
                        for alt in alts:
                            if alt in alts_row:
                                check_flag = True
                    if check_flag:
                        rsids.append(rsid)
                
                if len(rsids) > 0:
                    variant[2] = ",".join(rsids)

                new_line = "\t".join(variant)
                output.writelines(new_line)

                # index()


        output.close()
        #merge 5 vcfs: snpeff, vep, snpsift, hi_index and hgmd 
        # print('merge snpeff')
        #snpeff
        # command = "java -Xmx%s -jar \
        # %s/SnpSift.jar \
        # annotate -info EFF -noId \
        # ../snpeff/snpeff.output.vcf \
        # ../sanity_check/checked.vcf \
        # > snpeff.vcf \
        # "% (settings.snpsift_merge_memory, settings.snpeff_dir)
        # print(command)
        
        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)
        # # print 'snpeff'
        # # print('merge vep')
        # #vep
        # command = "java -Xmx%s -jar \
        # %s/SnpSift.jar \
        # annotate -info CSQ -noId \
        # ../vep/vep.output.sorted.vcf \
        # snpeff.vcf \
        # > snpeff.vep.vcf \
        # "% (settings.snpsift_merge_memory, settings.snpeff_dir)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)
        # # print('merge snpsift')
        # #snpsift
        # command = "java -Xmx%s -jar \
        # %s/SnpSift.jar \
        # annotate -info VARTYPE,SNP,MNP,INS,DEL,MIXED,HOM,HET -noId \
        # ../snpsift/snpsift.final.vcf \
        # snpeff.vep.vcf \
        # > snpsift.snpeff.vep.vcf \
        # "% (settings.snpsift_merge_memory, settings.snpeff_dir)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        # # print('merge hi_index')
        # #hi_index
        # command = "java -Xmx%s -jar \
        # %s/SnpSift.jar \
        # annotate -info HI_INDEX -noId \
        # ../hi_index/hi_index.vcf \
        # snpsift.snpeff.vep.vcf \
        # > hi_index.snpsift.snpeff.vep.vcf \
        # "% (settings.snpsift_merge_memory, settings.snpeff_dir)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)
        
        # # print('merge pynnotator')
        # #pynnotator - 1000genomes, dbsnp, clinvar, esp6500, ensembl
        # command = "java -Xmx%s -jar \
        # %s/SnpSift.jar \
        # annotate -noId \
        # ../pynnotator/pynnotator.vcf \
        # hi_index.snpsift.snpeff.vep.vcf \
        # > 1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf  \
        # " % (settings.snpsift_merge_memory, settings.snpeff_dir)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        # # print   'func pred'
        
        # # print('merge cadd_dann')
        # #cadd_dann
        # command = "java -Xmx%s -jar \
        # %s/SnpSift.jar \
        # annotate -noId -info dbNSFP_SIFT_score,dbNSFP_SIFT_converted_rankscore,dbNSFP_SIFT_pred,dbNSFP_Uniprot_acc_Polyphen2,dbNSFP_Uniprot_id_Polyphen2,dbNSFP_Uniprot_aapos_Polyphen2,dbNSFP_Polyphen2_HDIV_score,dbNSFP_Polyphen2_HDIV_rankscore,dbNSFP_Polyphen2_HDIV_pred,dbNSFP_Polyphen2_HVAR_score,dbNSFP_Polyphen2_HVAR_rankscore,dbNSFP_Polyphen2_HVAR_pred,dbNSFP_LRT_score,dbNSFP_LRT_converted_rankscore,dbNSFP_LRT_pred,dbNSFP_LRT_Omega,dbNSFP_MutationTaster_score,dbNSFP_MutationTaster_converted_rankscore,dbNSFP_MutationTaster_pred,dbNSFP_MutationTaster_model,dbNSFP_MutationTaster_AAE,dbNSFP_MutationAssessor_UniprotID,dbNSFP_MutationAssessor_variant,dbNSFP_MutationAssessor_score,dbNSFP_MutationAssessor_rankscore,dbNSFP_MutationAssessor_pred,dbNSFP_FATHMM_score,dbNSFP_FATHMM_converted_rankscore,dbNSFP_FATHMM_pred,dbNSFP_PROVEAN_score,dbNSFP_PROVEAN_converted_rankscore,dbNSFP_PROVEAN_pred,dbNSFP_Transcript_id_VEST3,dbNSFP_Transcript_var_VEST3,dbNSFP_VEST3_score,dbNSFP_VEST3_rankscore,dbNSFP_MetaSVM_score,dbNSFP_MetaSVM_rankscore,dbNSFP_MetaSVM_pred,dbNSFP_MetaLR_score,dbNSFP_MetaLR_rankscore,dbNSFP_MetaLR_pred,dbNSFP_Reliability_index,dbNSFP_CADD_raw,dbNSFP_CADD_raw_rankscore,dbNSFP_CADD_phred,dbNSFP_DANN_score,dbNSFP_DANN_rankscore,dbNSFP_fathmm,dbNSFP_fathmm,dbNSFP_fathmm,dbNSFP_fathmm,dbNSFP_Eigen,dbNSFP_Eigen,dbNSFP_Eigen,dbNSFP_Eigen,dbNSFP_Eigen,dbNSFP_GenoCanyon_score,dbNSFP_GenoCanyon_score_rankscore,dbNSFP_integrated_fitCons_score,dbNSFP_integrated_fitCons_rankscore,dbNSFP_integrated_confidence_value,dbNSFP_GM12878_fitCons_score,dbNSFP_GM12878_fitCons_rankscore,dbNSFP_GM12878_confidence_value,dbNSFP_H1,dbNSFP_H1,dbNSFP_H1,dbNSFP_HUVEC_fitCons_score,dbNSFP_HUVEC_fitCons_rankscore,dbNSFP_HUVEC_confidence_value,dbNSFP_GERP,dbNSFP_GERP,dbNSFP_GERP,dbNSFP_phyloP100way_vertebrate,dbNSFP_phyloP100way_vertebrate_rankscore,dbNSFP_phyloP20way_mammalian,dbNSFP_phyloP20way_mammalian_rankscore,dbNSFP_phastCons100way_vertebrate,dbNSFP_phastCons100way_vertebrate_rankscore,dbNSFP_phastCons20way_mammalian,dbNSFP_phastCons20way_mammalian_rankscore,dbNSFP_SiPhy_29way_pi,dbNSFP_SiPhy_29way_logOdds,dbNSFP_SiPhy_29way_logOdds_rankscore,dbNSFP_clinvar_rs,dbNSFP_clinvar_clnsig,dbNSFP_clinvar_trait,dbNSFP_clinvar_golden_stars \
        # ../func_pred/func_pred.vcf \
        # 1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf \
        # > func_pred.1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf  \
        # "% (settings.snpsift_merge_memory, settings.snpeff_dir)


        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        # # print('merge dbsnp')
        # #dbsnp
        # command = "java -Xmx%s -jar \
        # %s/SnpSift.jar \
        # annotate -id \
        # %s \
        # func_pred.1kgenomes.dbsnp.clinvar.esp.hi_index.snpsift.snpeff.vep.vcf \
        # > annotation.final.vcf  \
        # "% (settings.snpsift_merge_memory, settings.snpeff_dir,settings.dbsnp)


        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        # if p == 0:
        #     print('This vcf was succesfully merged')
        # else:
        #     print('Sorry this vcf could not be merged')


if  __name__ == '__main__' :

    parser = argparse.ArgumentParser(description='MERGE all VCF Files from previous methods.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')
    
    args = parser.parse_args()

    merge = Merge(args.vcffile)
    merge.run()