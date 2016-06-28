#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
import pysam

from settings import *

parser = argparse.ArgumentParser(description='Annotate a VCF File with DbNSFP.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

args = parser.parse_args()

dbnfsp_header = '''##INFO=<ID=dbNSFP_GERP++_RS,Number=A,Type=Float,Description="Field 'GERP++_RS' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_ASN_AF,Number=A,Type=Float,Description="Field '1000Gp1_ASN_AF' from dbNSFP">
##INFO=<ID=dbNSFP_Ensembl_geneid,Number=A,Type=String,Description="Field 'Ensembl_geneid' from dbNSFP">
##INFO=<ID=dbNSFP_CADD_phred,Number=A,Type=Float,Description="Field 'CADD_phred' from dbNSFP">
##INFO=<ID=dbNSFP_FATHMM_score,Number=A,Type=Float,Description="Field 'FATHMM_score' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_ASN_AC,Number=A,Type=Integer,Description="Field '1000Gp1_ASN_AC' from dbNSFP">
##INFO=<ID=dbNSFP_GERP++_RS_rankscore,Number=A,Type=Float,Description="Field 'GERP++_RS_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_MutationTaster_pred,Number=A,Type=Character,Description="Field 'MutationTaster_pred' from dbNSFP">
##INFO=<ID=dbNSFP_SiPhy_29way_logOdds_rankscore,Number=A,Type=Float,Description="Field 'SiPhy_29way_logOdds_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_phastCons46way_placental_rankscore,Number=A,Type=Float,Description="Field 'phastCons46way_placental_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_FATHMM_pred,Number=A,Type=Character,Description="Field 'FATHMM_pred' from dbNSFP">
##INFO=<ID=dbNSFP_phastCons100way_vertebrate,Number=A,Type=Float,Description="Field 'phastCons100way_vertebrate' from dbNSFP">
##INFO=<ID=dbNSFP_MutationTaster_score,Number=A,Type=Float,Description="Field 'MutationTaster_score' from dbNSFP">
##INFO=<ID=dbNSFP_VEST3_rankscore,Number=A,Type=Float,Description="Field 'VEST3_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_fold-degenerate,Number=A,Type=Integer,Description="Field 'fold-degenerate' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_AMR_AC,Number=A,Type=Integer,Description="Field '1000Gp1_AMR_AC' from dbNSFP">
##INFO=<ID=dbNSFP_MutationAssessor_score,Number=A,Type=Float,Description="Field 'MutationAssessor_score' from dbNSFP">
##INFO=<ID=dbNSFP_ESP6500_EA_AF,Number=A,Type=Float,Description="Field 'ESP6500_EA_AF' from dbNSFP">
##INFO=<ID=dbNSFP_phyloP46way_primate_rankscore,Number=A,Type=Float,Description="Field 'phyloP46way_primate_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_LRT_pred,Number=A,Type=Character,Description="Field 'LRT_pred' from dbNSFP">
##INFO=<ID=dbNSFP_phastCons100way_vertebrate_rankscore,Number=A,Type=Float,Description="Field 'phastCons100way_vertebrate_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_AMR_AF,Number=A,Type=Float,Description="Field '1000Gp1_AMR_AF' from dbNSFP">
##INFO=<ID=dbNSFP_LRT_Omega,Number=A,Type=Float,Description="Field 'LRT_Omega' from dbNSFP">
##INFO=<ID=dbNSFP_GERP++_NR,Number=A,Type=Float,Description="Field 'GERP++_NR' from dbNSFP">
##INFO=<ID=dbNSFP_FATHMM_rankscore,Number=A,Type=Float,Description="Field 'FATHMM_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_Interpro_domain,Number=A,Type=String,Description="Field 'Interpro_domain' from dbNSFP">
##INFO=<ID=dbNSFP_MutationAssessor_pred,Number=A,Type=Character,Description="Field 'MutationAssessor_pred' from dbNSFP">
##INFO=<ID=dbNSFP_SiPhy_29way_logOdds,Number=A,Type=Float,Description="Field 'SiPhy_29way_logOdds' from dbNSFP">
##INFO=<ID=dbNSFP_LRT_score,Number=A,Type=Float,Description="Field 'LRT_score' from dbNSFP">
##INFO=<ID=dbNSFP_phyloP100way_vertebrate,Number=A,Type=Float,Description="Field 'phyloP100way_vertebrate' from dbNSFP">
##INFO=<ID=dbNSFP_cds_strand,Number=A,Type=Character,Description="Field 'cds_strand' from dbNSFP">
##INFO=<ID=dbNSFP_VEST3_score,Number=A,Type=Float,Description="Field 'VEST3_score' from dbNSFP">
##INFO=<ID=dbNSFP_RadialSVM_score,Number=A,Type=Float,Description="Field 'RadialSVM_score' from dbNSFP">
##INFO=<ID=dbNSFP_RadialSVM_pred,Number=A,Type=Character,Description="Field 'RadialSVM_pred' from dbNSFP">
##INFO=<ID=dbNSFP_LR_score,Number=A,Type=Float,Description="Field 'LR_score' from dbNSFP">
##INFO=<ID=dbNSFP_LR_pred,Number=A,Type=Character,Description="Field 'LR_pred' from dbNSFP">
##INFO=<ID=dbNSFP_phastCons46way_placental,Number=A,Type=Float,Description="Field 'phastCons46way_placental' from dbNSFP">
##INFO=<ID=dbNSFP_CADD_raw_rankscore,Number=A,Type=Float,Description="Field 'CADD_raw_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_SIFT_converted_rankscore,Number=A,Type=Float,Description="Field 'SIFT_converted_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_phyloP100way_vertebrate_rankscore,Number=A,Type=Float,Description="Field 'phyloP100way_vertebrate_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_MutationAssessor_rankscore,Number=A,Type=Float,Description="Field 'MutationAssessor_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_Uniprot_acc,Number=A,Type=String,Description="Field 'Uniprot_acc' from dbNSFP">
##INFO=<ID=dbNSFP_codonpos,Number=A,Type=Integer,Description="Field 'codonpos' from dbNSFP">
##INFO=<ID=dbNSFP_Polyphen2_HDIV_score,Number=A,Type=Float,Description="Field 'Polyphen2_HDIV_score' from dbNSFP">
##INFO=<ID=dbNSFP_UniSNP_ids,Number=A,Type=String,Description="Field 'UniSNP_ids' from dbNSFP">
##INFO=<ID=dbNSFP_SIFT_pred,Number=A,Type=Character,Description="Field 'SIFT_pred' from dbNSFP">
##INFO=<ID=dbNSFP_SiPhy_29way_pi,Number=A,Type=String,Description="Field 'SiPhy_29way_pi' from dbNSFP">
##INFO=<ID=dbNSFP_LR_rankscore,Number=A,Type=Float,Description="Field 'LR_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_CADD_raw,Number=A,Type=Float,Description="Field 'CADD_raw' from dbNSFP">
##INFO=<ID=dbNSFP_LRT_converted_rankscore,Number=A,Type=Float,Description="Field 'LRT_converted_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_aapos_FATHMM,Number=A,Type=String,Description="Field 'aapos_FATHMM' from dbNSFP">
##INFO=<ID=dbNSFP_aapos,Number=A,Type=Integer,Description="Field 'aapos' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_AFR_AF,Number=A,Type=Float,Description="Field '1000Gp1_AFR_AF' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_AFR_AC,Number=A,Type=Integer,Description="Field '1000Gp1_AFR_AC' from dbNSFP">
##INFO=<ID=dbNSFP_refcodon,Number=A,Type=String,Description="Field 'refcodon' from dbNSFP">
##INFO=<ID=dbNSFP_SLR_test_statistic,Number=A,Type=Float,Description="Field 'SLR_test_statistic' from dbNSFP">
##INFO=<ID=dbNSFP_Uniprot_aapos,Number=A,Type=Integer,Description="Field 'Uniprot_aapos' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_AC,Number=A,Type=Integer,Description="Field '1000Gp1_AC' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_AF,Number=A,Type=Float,Description="Field '1000Gp1_AF' from dbNSFP">
##INFO=<ID=dbNSFP_aapos_SIFT,Number=A,Type=String,Description="Field 'aapos_SIFT' from dbNSFP">
##INFO=<ID=dbNSFP_SIFT_score,Number=A,Type=Float,Description="Field 'SIFT_score' from dbNSFP">
##INFO=<ID=dbNSFP_Reliability_index,Number=A,Type=Integer,Description="Field 'Reliability_index' from dbNSFP">
##INFO=<ID=dbNSFP_MutationTaster_converted_rankscore,Number=A,Type=Float,Description="Field 'MutationTaster_converted_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_Uniprot_id,Number=A,Type=String,Description="Field 'Uniprot_id' from dbNSFP">
##INFO=<ID=dbNSFP_Ensembl_transcriptid,Number=A,Type=String,Description="Field 'Ensembl_transcriptid' from dbNSFP">
##INFO=<ID=dbNSFP_phastCons46way_primate,Number=A,Type=Float,Description="Field 'phastCons46way_primate' from dbNSFP">
##INFO=<ID=dbNSFP_ESP6500_AA_AF,Number=A,Type=Float,Description="Field 'ESP6500_AA_AF' from dbNSFP">
##INFO=<ID=dbNSFP_RadialSVM_rankscore,Number=A,Type=Float,Description="Field 'RadialSVM_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_Polyphen2_HVAR_score,Number=A,Type=Float,Description="Field 'Polyphen2_HVAR_score' from dbNSFP">
##INFO=<ID=dbNSFP_Ancestral_allele,Number=A,Type=Character,Description="Field 'Ancestral_allele' from dbNSFP">
##INFO=<ID=dbNSFP_phyloP46way_placental,Number=A,Type=Float,Description="Field 'phyloP46way_placental' from dbNSFP">
##INFO=<ID=dbNSFP_phyloP46way_primate,Number=A,Type=Float,Description="Field 'phyloP46way_primate' from dbNSFP">
##INFO=<ID=dbNSFP_Polyphen2_HDIV_pred,Number=A,Type=Character,Description="Field 'Polyphen2_HDIV_pred' from dbNSFP">
##INFO=<ID=dbNSFP_Polyphen2_HDIV_rankscore,Number=A,Type=Float,Description="Field 'Polyphen2_HDIV_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_EUR_AF,Number=A,Type=Float,Description="Field '1000Gp1_EUR_AF' from dbNSFP">
##INFO=<ID=dbNSFP_phyloP46way_placental_rankscore,Number=A,Type=Float,Description="Field 'phyloP46way_placental_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_Polyphen2_HVAR_rankscore,Number=A,Type=Float,Description="Field 'Polyphen2_HVAR_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_phastCons46way_primate_rankscore,Number=A,Type=Float,Description="Field 'phastCons46way_primate_rankscore' from dbNSFP">
##INFO=<ID=dbNSFP_Polyphen2_HVAR_pred,Number=A,Type=Character,Description="Field 'Polyphen2_HVAR_pred' from dbNSFP">
##INFO=<ID=dbNSFP_1000Gp1_EUR_AC,Number=A,Type=Integer,Description="Field '1000Gp1_EUR_AC' from dbNSFP">
'''

class Dbnsfp(object):
    def __init__(self, vcffile=None):
        
        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
        self.dbnfsp_reader = pysam.Tabixfile(dbnsfp)
        self.header = self.dbnfsp_reader.header.next().strip().split('\t')
        # for item in self.dbnfsp_reader.header:
        #     print 'item',item
        #     #self.header.append(item)
        #print self.header
        
        #create folder snpeff if it doesn't exists
        if not os.path.exists('dbnfsp'):
            os.makedirs('dbnfsp')
        #enter inside folder
        os.chdir('dbnfsp')
        
    
    def run(self):
        tstart = datetime.now()
        print tstart, 'Starting dbnfsp annotation: ', self.vcffile
        
        self.annotate()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print tend, 'Finished dbnfsp annotation, it took: ', annotation_time        

    def check_ref_alt(self, variant, ann):
        #compare REF
        if variant[3] == ann[2]:
            alts = variant[4].split(',')
            alts_ann = ann[3].split(',')
            #compare ALT
            for alt in alts:
                if alt in alts_ann:
                    return True
        return False
    #convert and annotate the vcf file to snpeff
    def annotate(self):
        #print 'Hello'
        #print self.dbnfsp_reader
        vcf_reader = open('../%s' % (self.vcffile))
        vcf_writer = open('dbnsfp.vcf', 'w')
        
        for line in vcf_reader:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    vcf_writer.writelines(dbnfsp_header)
                vcf_writer.writelines(line)
            else:
                variant = line.split('\t')
                variant[0] = variant[0].replace('chr', '')
                index = '%s-%s' % (variant[0], variant[1])
                #print index
                try:
                    records = self.dbnfsp_reader.fetch(variant[0], int(variant[1])-1, int(variant[1]))
                except ValueError:
                    records = []
                for record in records:
                    ann = record.strip().split('\t')

                    if self.check_ref_alt(variant, ann):
                        new_ann = []
                        #this is the column from where to start annotation
                        start_index = 11
                        start_index = 108
                        #only freequencies 108 - 175
                        for k, item in enumerate(self.header[start_index:]):
                            # print k, item, ann[k+8]
                            if ann[k+start_index] != '.':
                                new_ann.append('dbnsfp.%s=%s' % (item, ann[k+start_index].replace(';', '|')))
                        variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
                vcf_writer.writelines("\t".join(variant))
                    


if  __name__ == '__main__' :
    dbnsfp = Dbnsfp(args.vcffile)
    dbnsfp.run()