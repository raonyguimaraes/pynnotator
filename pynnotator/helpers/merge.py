#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import pysam
from collections import OrderedDict
from datetime import datetime

from pynnotator import settings
from subprocess import call
toolname = 'merge'


class Merge(object):
    def __init__(self, vcffile=None):

        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        self.basedir = os.getcwd()

        # create folder merge if it doesn't exists
        if not os.path.exists('merge'):
            os.makedirs('merge')
        # enter inside folder
        os.chdir('merge')

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting merge: ', self.vcffile)

        self.merge()

        tend = datetime.now()
        annotation_time = tend - tstart
        print(tend, 'Finished merge, it took: ', annotation_time)

        # merge VCF Files with VariantAnnotator

    def merge(self):

        # print(BASE_DIR)

        files = ['../snpeff/snpeff.output.vcf', '../vep/vep.output.sorted.vcf', '../snpsift/snpsift.final.vcf']
        for file in files:
            command = 'bgzip {}'.format(file)
            call(command, shell=True)
            command = 'tabix -p vcf {}.gz'.format(file)
            call(command, shell=True)


        config = open('config.toml', 'w')
        config.write("""[[annotation]]
file="{}/snpsift/snpsift.final.vcf.gz"
fields = ["VARTYPE", "SNP", "MNP", "INS", "DEL", "MIXED", "HOM", "HET"]
ops=["first", "first", "first", "first", "first", "first", "first", "first"]

[[annotation]]
file="{}/dbsnp/{}"
fields = ["ID", "RS", "RSPOS", "RV", "VP", "GENEINFO", "dbSNPBuildID", "SAO", "SSR", "WGT", "VC", "PM", "TPA", "PMC", "S3D", "SLO", "NSF", "NSM", "NSN", "REF", "SYN", "U3", "U5", "ASS", "DSS", "INT", "R3", "R5", "OTH", "CFL", "ASP", "MUT", "VLD", "G5A", "G5", "HD", "GNO", "KGPhase1", "KGPhase3", "CDA", "LSD", "MTP", "OM", "NOC", "WTD", "NOV", "NC", "CAF", "COMMON", "TOPMED"]
ops=["first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first"]

[[annotation]]
file="{}/dbsnp/{}"
fields = ["AF_ESP", "AF_EXAC", "AF_TGP", "ALLELEID", "CLNDN", "CLNDNINCL", "CLNDISDB", "CLNDISDBINCL", "CLNHGVS", "CLNREVSTAT", "CLNSIG", "CLNSIGCONF", "CLNSIGINCL", "CLNVC", "CLNVCSO", "CLNVI", "DBVARID", "GENEINFO", "MC", "ORIGIN", "RS", "SSR", ]
ops=["first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first"]

[[annotation]]
file="{}/1000genomes/ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz"
fields = ["CIEND", "CIPOS", "CS", "END", "IMPRECISE", "MC", "MEINFO", "MEND", "MLEN", "MSTART", "SVLEN", "SVTYPE", "TSD", "AC", "AF", "NS", "AN", "EAS_AF", "EUR_AF", "AFR_AF", "AMR_AF", "SAS_AF", "DP", "AA", "VT", "EX_TARGET", "MULTI_ALLELIC", "OLD_VARIANT"]
ops=["first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first", "first"]

[[annotation]]
file="{}/decipher/HI_Predictions_Version3.bed.gz"
names=["HI_PREDICTION"]
columns=[4]
ops=["uniq"]

[[annotation]]
file="{}/ensembl/homo_sapiens_clinically_associated.vcf.gz"
names = ["ensembl_clin_ClinVar_201706", "ensembl_clin_dbSNP_150", "ensembl_clin_HGMD", "ensembl_clin_PhenCode", "ensembl_clin_COSMIC_81", "ensembl_clin_ESP_20141103", "ensembl_clin_TSA", "ensembl_clin_E_Cited", "ensembl_clin_E_Multiple_observations", "ensembl_clin_E_Freq", "ensembl_clin_E_Hapmap", "ensembl_clin_E_Phenotype_or_Disease", "ensembl_clin_E_ESP", "ensembl_clin_E_1000G", "ensembl_clin_E_ExAC", "ensembl_clin_CLIN_risk_factor", "ensembl_clin_CLIN_protective", "ensembl_clin_CLIN_confers_sensitivity", "ensembl_clin_CLIN_other", "ensembl_clin_CLIN_drug_response", "ensembl_clin_CLIN_uncertain_significance", "ensembl_clin_CLIN_benign", "ensembl_clin_CLIN_likely_pathogenic", "ensembl_clin_CLIN_pathogenic", "ensembl_clin_CLIN_likely_benign", "ensembl_clin_CLIN_histocompatibility", "ensembl_clin_CLIN_not_provided", "ensembl_clin_CLIN_association", "ensembl_clin_MA", "ensembl_clin_MAF", "ensembl_clin_MAC", "ensembl_clin_AA"]
fields = ["ClinVar_201706", "dbSNP_150", "HGMD", "PhenCode", "COSMIC_81", "ESP_20141103", "TSA", "E_Cited", "E_Multiple_observations", "E_Freq", "E_Hapmap", "E_Phenotype_or_Disease", "E_ESP", "E_1000G", "E_ExAC", "CLIN_risk_factor", "CLIN_protective", "CLIN_confers_sensitivity", "CLIN_other", "CLIN_drug_response", "CLIN_uncertain_significance", "CLIN_benign", "CLIN_likely_pathogenic", "CLIN_pathogenic", "CLIN_likely_benign", "CLIN_histocompatibility", "CLIN_not_provided", "CLIN_association", "MA", "MAF", "MAC", "AA"]
ops=["first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first"]

[[annotation]]
file="{}/ensembl/homo_sapiens_phenotype_associated.vcf.gz"
names = ["ensembl_phen_ClinVar_201706","ensembl_phen_dbSNP_150","ensembl_phen_HGMD","ensembl_phen_PhenCode","ensembl_phen_COSMIC_81","ensembl_phen_ESP_20141103","ensembl_phen_TSA","ensembl_phen_E_Cited","ensembl_phen_E_Multiple_observations","ensembl_phen_E_Freq","ensembl_phen_E_Hapmap","ensembl_phen_E_Phenotype_or_Disease","ensembl_phen_E_ESP","ensembl_phen_E_1000G","ensembl_phen_E_ExAC","ensembl_phen_CLIN_risk_factor","ensembl_phen_CLIN_protective","ensembl_phen_CLIN_confers_sensitivity","ensembl_phen_CLIN_other","ensembl_phen_CLIN_drug_response","ensembl_phen_CLIN_uncertain_significance","ensembl_phen_CLIN_benign","ensembl_phen_CLIN_likely_pathogenic","ensembl_phen_CLIN_pathogenic","ensembl_phen_CLIN_likely_benign","ensembl_phen_CLIN_histocompatibility","ensembl_phen_CLIN_not_provided","ensembl_phen_CLIN_association","ensembl_phen_MA","ensembl_phen_MAF","ensembl_phen_MAC","ensembl_phen_AA"]
fields = ["ClinVar_201706", "dbSNP_150", "HGMD", "PhenCode", "COSMIC_81", "ESP_20141103", "TSA", "E_Cited", "E_Multiple_observations", "E_Freq", "E_Hapmap", "E_Phenotype_or_Disease", "E_ESP", "E_1000G", "E_ExAC", "CLIN_risk_factor", "CLIN_protective", "CLIN_confers_sensitivity", "CLIN_other", "CLIN_drug_response", "CLIN_uncertain_significance", "CLIN_benign", "CLIN_likely_pathogenic", "CLIN_pathogenic", "CLIN_likely_benign", "CLIN_histocompatibility", "CLIN_not_provided", "CLIN_association", "MA", "MAF", "MAC", "AA"]
ops=["first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first"]

[[annotation]]
file="{}/snpeff/snpeff.output.vcf.gz"
fields = ["ANN"]
names = ["snpeff_eff"]
ops=["first"]

[[annotation]]
file="{}/vep/vep.output.sorted.vcf.gz"
fields = ["CSQ"]
names = ["vep_csq"]
ops=["first"]

            """.format(self.basedir, settings.data_dir, settings.dbsnp_file, settings.data_dir, settings.clinvar_file, settings.data_dir, settings.data_dir,settings.data_dir,settings.data_dir,self.basedir, self.basedir))
#settings.data_dir,         

# [[annotation]]
# file="{}/gnomead/gnomad.exomes.r2.0.2.sites.vcf.bgz"
# fields = ["AC", "AF", "AN", "BaseQRankSum", "ClippingRankSum", "DB", "DP", "FS", "InbreedingCoeff", "MQ", "MQRankSum", "QD", "ReadPosRankSum", "SOR", "VQSLOD", "VQSR_culprit", "VQSR_NEGATIVE_TRAIN_SITE", "VQSR_POSITIVE_TRAIN_SITE", "GQ_HIST_ALT", "DP_HIST_ALT", "AB_HIST_ALT", "GQ_HIST_ALL", "DP_HIST_ALL", "AB_HIST_ALL", "AC_AFR", "AC_AMR", "AC_ASJ", "AC_EAS", "AC_FIN", "AC_NFE", "AC_OTH", "AC_SAS", "AC_Male", "AC_Female", "AN_AFR", "AN_AMR", "AN_ASJ", "AN_EAS", "AN_FIN", "AN_NFE", "AN_OTH", "AN_SAS", "AN_Male", "AN_Female", "AF_AFR", "AF_AMR", "AF_ASJ", "AF_EAS", "AF_FIN", "AF_NFE", "AF_OTH", "AF_SAS", "AF_Male", "AF_Female", "GC_AFR", "GC_AMR", "GC_ASJ", "GC_EAS", "GC_FIN", "GC_NFE", "GC_OTH", "GC_SAS", "GC_Male", "GC_Female", "AC_raw", "AN_raw", "AF_raw", "GC_raw", "GC", "Hom_AFR", "Hom_AMR", "Hom_ASJ", "Hom_EAS", "Hom_FIN", "Hom_NFE", "Hom_OTH", "Hom_SAS", "Hom_Male", "Hom_Female", "Hom_raw", "Hom", "STAR_AC", "STAR_AC_raw", "STAR_Hom", "POPMAX", "AC_POPMAX", "AN_POPMAX", "AF_POPMAX", "DP_MEDIAN", "DREF_MEDIAN", "GQ_MEDIAN", "AB_MEDIAN", "AS_RF", "AS_FilterStatus", "AS_RF_POSITIVE_TRAIN", "AS_RF_NEGATIVE_TRAIN", "CSQ", "AN_FIN_Male", "AN_EAS_Female", "AN_NFE_Female", "AC_AFR_Male", "AN_AMR_Female", "AF_AMR_Male", "Hemi_NFE", "Hemi_AFR", "AC_ASJ_Female", "AF_FIN_Female", "AN_ASJ_Male", "AC_OTH_Female", "GC_OTH_Male", "GC_FIN_Male", "AC_NFE_Female", "AC_EAS_Male", "AC_OTH_Male", "GC_SAS_Male", "Hemi_AMR", "AC_NFE_Male", "Hemi", "AN_FIN_Female", "GC_EAS_Male", "GC_ASJ_Female", "GC_SAS_Female", "GC_ASJ_Male", "Hemi_SAS", "AN_ASJ_Female", "AF_FIN_Male", "AN_OTH_Male", "AF_AFR_Male", "STAR_Hemi", "AF_SAS_Male", "Hemi_ASJ", "AN_SAS_Female", "AN_AFR_Female", "Hemi_raw", "AF_OTH_Male", "AC_SAS_Female", "AF_NFE_Female", "AF_EAS_Female", "AN_OTH_Female", "AF_EAS_Male", "AF_SAS_Female", "GC_AFR_Female", "AF_AFR_Female", "AC_FIN_Female", "Hemi_OTH", "GC_AMR_Male", "AC_AFR_Female", "GC_NFE_Male", "AF_AMR_Female", "GC_NFE_Female", "AN_AFR_Male", "AN_NFE_Male", "AC_AMR_Male", "GC_AMR_Female", "AC_SAS_Male", "AF_ASJ_Male", "GC_FIN_Female", "AC_EAS_Female", "AC_AMR_Female", "Hemi_FIN", "AC_FIN_Male", "GC_EAS_Female", "AF_ASJ_Female", "AF_OTH_Female", "GC_AFR_Male", "AN_SAS_Male", "AF_NFE_Male", "AN_EAS_Male", "AC_ASJ_Male", "Hemi_EAS", "AN_AMR_Male", "GC_OTH_Female", "segdup", "lcr"]
# ops=["first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first","first"]

#[[annotation]]
#file="{}/hgmd/HGMD_PRO_2017.3_hg19.vcf.gz"
#fields = ["CLASS", "MUT", "GENE", "STRAND", "DNA", "PROT", "DB", "PHEN"]
#ops=["first", "first", "first", "first", "first", "first", "first", "first"]
        
        config.close()
        command = '{}/vcfanno/vcfanno_linux64 -p {} config.toml ../{} > ../annotation.final.vcf'.format(settings.libs_dir, settings.vcfanno_cores, self.vcffile)
        call(command,shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MERGE all VCF Files from previous methods.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    merge = Merge(args.vcffile)
    merge.run()
