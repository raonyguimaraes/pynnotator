#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import pysam
from collections import OrderedDict
from datetime import datetime

from pynnotator import settings

toolname = 'merge'


class Merge(object):
    def __init__(self, vcffile=None):

        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        self.header = open('%s/scripts/header.vcf' % (settings.BASE_DIR)).readlines()

        # create folder merge if it doesn't exists
        if not os.path.exists('merge'):
            os.makedirs('merge')
        # enter inside folder
        os.chdir('merge')

        self.annotation_files = OrderedDict()

        pysam.tabix_index('../snpeff/snpeff.output.vcf', preset='vcf')

        self.annotation_files['snpeff'] = {
            'info': 'EFF',
            'file': pysam.Tabixfile('../snpeff/snpeff.output.vcf.gz', 'r', encoding="utf-8")
        }

        pysam.tabix_index('../vep/vep.output.sorted.vcf', preset='vcf')

        self.annotation_files['vep'] = {
            'info': 'CSQ',
            'file': pysam.Tabixfile('../vep/vep.output.sorted.vcf.gz', 'r', encoding="utf-8")
        }

        pysam.tabix_index('../snpsift/snpsift.final.vcf', preset='vcf')

        self.annotation_files['vartype'] = {
            'info': 'VARTYPE,SNP,MNP,INS,DEL,MIXED,HOM,HET',
            'file': pysam.Tabixfile('../snpsift/snpsift.final.vcf.gz', 'r', encoding="utf-8")
        }

        pysam.tabix_index('../decipher/hi_predictions.vcf', preset='vcf')

        self.annotation_files['decipher'] = {
            'info': 'HI_PREDICTIONS',
            'file': pysam.Tabixfile('../decipher/hi_predictions.vcf.gz', 'r', encoding="utf-8")
        }

        pysam.tabix_index('../pynnotator/pynnotator.vcf', preset='vcf')

        # genomes1k dbsnp clinvar esp6500 ensembl_phen ensembl_clin
        self.pynnotator_tags = ['genomes1k', 'dbsnp', 'clinvar', 'esp6500', 'ensembl_phen', 'ensembl_clin', 'hgmd']

        self.annotation_files['pynnotator'] = {
            'info': 'ALL',
            'file': pysam.Tabixfile('../pynnotator/pynnotator.vcf.gz', 'r', encoding="utf-8")
        }

        # pysam.tabix_index('../dbnsfp/dbnsfp.vcf', preset='vcf')

        # self.annotation_files['dbnsfp'] = {
        #     'info': 'dbNSFP_chr,dbNSFP_pos(1-based),dbNSFP_ref,dbNSFP_alt,dbNSFP_aaref,dbNSFP_aaalt,dbNSFP_rs_dbSNP150,dbNSFP_hg19_chr,dbNSFP_hg19_pos(1-based),dbNSFP_hg18_chr,dbNSFP_hg18_pos(1-based),dbNSFP_genename,dbNSFP_cds_strand,dbNSFP_refcodon,dbNSFP_codonpos,dbNSFP_codon_degeneracy,dbNSFP_Ancestral_allele,dbNSFP_AltaiNeandertal,dbNSFP_Denisova,dbNSFP_Ensembl_geneid,dbNSFP_Ensembl_transcriptid,dbNSFP_Ensembl_proteinid,dbNSFP_aapos,dbNSFP_SIFT_score,dbNSFP_SIFT_converted_rankscore,dbNSFP_SIFT_pred,dbNSFP_Uniprot_acc_Polyphen2,dbNSFP_Uniprot_id_Polyphen2,dbNSFP_Uniprot_aapos_Polyphen2,dbNSFP_Polyphen2_HDIV_score,dbNSFP_Polyphen2_HDIV_rankscore,dbNSFP_Polyphen2_HDIV_pred,dbNSFP_Polyphen2_HVAR_score,dbNSFP_Polyphen2_HVAR_rankscore,dbNSFP_Polyphen2_HVAR_pred,dbNSFP_LRT_score,dbNSFP_LRT_converted_rankscore,dbNSFP_LRT_pred,dbNSFP_LRT_Omega,dbNSFP_MutationTaster_score,dbNSFP_MutationTaster_converted_rankscore,dbNSFP_MutationTaster_pred,dbNSFP_MutationTaster_model,dbNSFP_MutationTaster_AAE,dbNSFP_MutationAssessor_UniprotID,dbNSFP_MutationAssessor_variant,dbNSFP_MutationAssessor_score,dbNSFP_MutationAssessor_rankscore,dbNSFP_MutationAssessor_pred,dbNSFP_FATHMM_score,dbNSFP_FATHMM_converted_rankscore,dbNSFP_FATHMM_pred,dbNSFP_PROVEAN_score,dbNSFP_PROVEAN_converted_rankscore,dbNSFP_PROVEAN_pred,dbNSFP_Transcript_id_VEST3,dbNSFP_Transcript_var_VEST3,dbNSFP_VEST3_score,dbNSFP_VEST3_rankscore,dbNSFP_MetaSVM_score,dbNSFP_MetaSVM_rankscore,dbNSFP_MetaSVM_pred,dbNSFP_MetaLR_score,dbNSFP_MetaLR_rankscore,dbNSFP_MetaLR_pred,dbNSFP_Reliability_index,dbNSFP_M-CAP_score,dbNSFP_M-CAP_rankscore,dbNSFP_M-CAP_pred,dbNSFP_REVEL_score,dbNSFP_REVEL_rankscore,dbNSFP_MutPred_score,dbNSFP_MutPred_rankscore,dbNSFP_MutPred_protID,dbNSFP_MutPred_AAchange,dbNSFP_MutPred_Top5features,dbNSFP_CADD_raw,dbNSFP_CADD_raw_rankscore,dbNSFP_CADD_phred,dbNSFP_DANN_score,dbNSFP_DANN_rankscore,dbNSFP_fathmm-MKL_coding_score,dbNSFP_fathmm-MKL_coding_rankscore,dbNSFP_fathmm-MKL_coding_pred,dbNSFP_fathmm-MKL_coding_group,dbNSFP_Eigen_coding_or_noncoding,dbNSFP_Eigen-raw,dbNSFP_Eigen-phred,dbNSFP_Eigen-PC-raw,dbNSFP_Eigen-PC-phred,dbNSFP_Eigen-PC-raw_rankscore,dbNSFP_GenoCanyon_score,dbNSFP_GenoCanyon_score_rankscore,dbNSFP_integrated_fitCons_score,dbNSFP_integrated_fitCons_rankscore,dbNSFP_integrated_confidence_value,dbNSFP_GM12878_fitCons_score,dbNSFP_GM12878_fitCons_rankscore,dbNSFP_GM12878_confidence_value,dbNSFP_H1-hESC_fitCons_score,dbNSFP_H1-hESC_fitCons_rankscore,dbNSFP_H1-hESC_confidence_value,dbNSFP_HUVEC_fitCons_score,dbNSFP_HUVEC_fitCons_rankscore,dbNSFP_HUVEC_confidence_value,dbNSFP_GERP++_NR,dbNSFP_GERP++_RS,dbNSFP_GERP++_RS_rankscore,dbNSFP_phyloP100way_vertebrate,dbNSFP_phyloP100way_vertebrate_rankscore,dbNSFP_phyloP20way_mammalian,dbNSFP_phyloP20way_mammalian_rankscore,dbNSFP_phastCons100way_vertebrate,dbNSFP_phastCons100way_vertebrate_rankscore,dbNSFP_phastCons20way_mammalian,dbNSFP_phastCons20way_mammalian_rankscore,dbNSFP_SiPhy_29way_pi,dbNSFP_SiPhy_29way_logOdds,dbNSFP_SiPhy_29way_logOdds_rankscore,dbNSFP_1000Gp3_AC,dbNSFP_1000Gp3_AF,dbNSFP_1000Gp3_AFR_AC,dbNSFP_1000Gp3_AFR_AF,dbNSFP_1000Gp3_EUR_AC,dbNSFP_1000Gp3_EUR_AF,dbNSFP_1000Gp3_AMR_AC,dbNSFP_1000Gp3_AMR_AF,dbNSFP_1000Gp3_EAS_AC,dbNSFP_1000Gp3_EAS_AF,dbNSFP_1000Gp3_SAS_AC,dbNSFP_1000Gp3_SAS_AF,dbNSFP_TWINSUK_AC,dbNSFP_TWINSUK_AF,dbNSFP_ALSPAC_AC,dbNSFP_ALSPAC_AF,dbNSFP_ESP6500_AA_AC,dbNSFP_ESP6500_AA_AF,dbNSFP_ESP6500_EA_AC,dbNSFP_ESP6500_EA_AF,dbNSFP_ExAC_AC,dbNSFP_ExAC_AF,dbNSFP_ExAC_Adj_AC,dbNSFP_ExAC_Adj_AF,dbNSFP_ExAC_AFR_AC,dbNSFP_ExAC_AFR_AF,dbNSFP_ExAC_AMR_AC,dbNSFP_ExAC_AMR_AF,dbNSFP_ExAC_EAS_AC,dbNSFP_ExAC_EAS_AF,dbNSFP_ExAC_FIN_AC,dbNSFP_ExAC_FIN_AF,dbNSFP_ExAC_NFE_AC,dbNSFP_ExAC_NFE_AF,dbNSFP_ExAC_SAS_AC,dbNSFP_ExAC_SAS_AF,dbNSFP_ExAC_nonTCGA_AC,dbNSFP_ExAC_nonTCGA_AF,dbNSFP_ExAC_nonTCGA_Adj_AC,dbNSFP_ExAC_nonTCGA_Adj_AF,dbNSFP_ExAC_nonTCGA_AFR_AC,dbNSFP_ExAC_nonTCGA_AFR_AF,dbNSFP_ExAC_nonTCGA_AMR_AC,dbNSFP_ExAC_nonTCGA_AMR_AF,dbNSFP_ExAC_nonTCGA_EAS_AC,dbNSFP_ExAC_nonTCGA_EAS_AF,dbNSFP_ExAC_nonTCGA_FIN_AC,dbNSFP_ExAC_nonTCGA_FIN_AF,dbNSFP_ExAC_nonTCGA_NFE_AC,dbNSFP_ExAC_nonTCGA_NFE_AF,dbNSFP_ExAC_nonTCGA_SAS_AC,dbNSFP_ExAC_nonTCGA_SAS_AF,dbNSFP_ExAC_nonpsych_AC,dbNSFP_ExAC_nonpsych_AF,dbNSFP_ExAC_nonpsych_Adj_AC,dbNSFP_ExAC_nonpsych_Adj_AF,dbNSFP_ExAC_nonpsych_AFR_AC,dbNSFP_ExAC_nonpsych_AFR_AF,dbNSFP_ExAC_nonpsych_AMR_AC,dbNSFP_ExAC_nonpsych_AMR_AF,dbNSFP_ExAC_nonpsych_EAS_AC,dbNSFP_ExAC_nonpsych_EAS_AF,dbNSFP_ExAC_nonpsych_FIN_AC,dbNSFP_ExAC_nonpsych_FIN_AF,dbNSFP_ExAC_nonpsych_NFE_AC,dbNSFP_ExAC_nonpsych_NFE_AF,dbNSFP_ExAC_nonpsych_SAS_AC,dbNSFP_ExAC_nonpsych_SAS_AF,dbNSFP_gnomAD_exomes_AC,dbNSFP_gnomAD_exomes_AN,dbNSFP_gnomAD_exomes_AF,dbNSFP_gnomAD_exomes_AFR_AC,dbNSFP_gnomAD_exomes_AFR_AN,dbNSFP_gnomAD_exomes_AFR_AF,dbNSFP_gnomAD_exomes_AMR_AC,dbNSFP_gnomAD_exomes_AMR_AN,dbNSFP_gnomAD_exomes_AMR_AF,dbNSFP_gnomAD_exomes_ASJ_AC,dbNSFP_gnomAD_exomes_ASJ_AN,dbNSFP_gnomAD_exomes_ASJ_AF,dbNSFP_gnomAD_exomes_EAS_AC,dbNSFP_gnomAD_exomes_EAS_AN,dbNSFP_gnomAD_exomes_EAS_AF,dbNSFP_gnomAD_exomes_FIN_AC,dbNSFP_gnomAD_exomes_FIN_AN,dbNSFP_gnomAD_exomes_FIN_AF,dbNSFP_gnomAD_exomes_NFE_AC,dbNSFP_gnomAD_exomes_NFE_AN,dbNSFP_gnomAD_exomes_NFE_AF,dbNSFP_gnomAD_exomes_SAS_AC,dbNSFP_gnomAD_exomes_SAS_AN,dbNSFP_gnomAD_exomes_SAS_AF,dbNSFP_gnomAD_exomes_OTH_AC,dbNSFP_gnomAD_exomes_OTH_AN,dbNSFP_gnomAD_exomes_OTH_AF,dbNSFP_gnomAD_genomes_AC,dbNSFP_gnomAD_genomes_AN,dbNSFP_gnomAD_genomes_AF,dbNSFP_gnomAD_genomes_AFR_AC,dbNSFP_gnomAD_genomes_AFR_AN,dbNSFP_gnomAD_genomes_AFR_AF,dbNSFP_gnomAD_genomes_AMR_AC,dbNSFP_gnomAD_genomes_AMR_AN,dbNSFP_gnomAD_genomes_AMR_AF,dbNSFP_gnomAD_genomes_ASJ_AC,dbNSFP_gnomAD_genomes_ASJ_AN,dbNSFP_gnomAD_genomes_ASJ_AF,dbNSFP_gnomAD_genomes_EAS_AC,dbNSFP_gnomAD_genomes_EAS_AN,dbNSFP_gnomAD_genomes_EAS_AF,dbNSFP_gnomAD_genomes_FIN_AC,dbNSFP_gnomAD_genomes_FIN_AN,dbNSFP_gnomAD_genomes_FIN_AF,dbNSFP_gnomAD_genomes_NFE_AC,dbNSFP_gnomAD_genomes_NFE_AN,dbNSFP_gnomAD_genomes_NFE_AF,dbNSFP_gnomAD_genomes_OTH_AC,dbNSFP_gnomAD_genomes_OTH_AN,dbNSFP_gnomAD_genomes_OTH_AF,dbNSFP_clinvar_rs,dbNSFP_clinvar_clnsig,dbNSFP_clinvar_trait,dbNSFP_clinvar_golden_stars,dbNSFP_Interpro_domain,dbNSFP_GTEx_V6p_gene,dbNSFP_GTEx_V6p_tissue,dbNSFP_Gene_old_names,dbNSFP_Gene_other_names,dbNSFP_Uniprot_acc(HGNC/Uniprot),dbNSFP_Uniprot_id(HGNC/Uniprot),dbNSFP_Entrez_gene_id,dbNSFP_CCDS_id,dbNSFP_Refseq_id,dbNSFP_ucsc_id,dbNSFP_MIM_id,dbNSFP_Gene_full_name,dbNSFP_Pathway(Uniprot),dbNSFP_Pathway(BioCarta)_short,dbNSFP_Pathway(BioCarta)_full,dbNSFP_Pathway(ConsensusPathDB),dbNSFP_Pathway(KEGG)_id,dbNSFP_Pathway(KEGG)_full,dbNSFP_Function_description,dbNSFP_Disease_description,dbNSFP_MIM_phenotype_id,dbNSFP_MIM_disease,dbNSFP_Trait_association(GWAS),dbNSFP_GO_biological_process,dbNSFP_GO_cellular_component,dbNSFP_GO_molecular_function,dbNSFP_Tissue_specificity(Uniprot),dbNSFP_Expression(egenetics),dbNSFP_Expression(GNF/Atlas),dbNSFP_Interactions(IntAct),dbNSFP_Interactions(BioGRID),dbNSFP_Interactions(ConsensusPathDB),dbNSFP_P(HI),dbNSFP_P(rec),dbNSFP_Known_rec_info,dbNSFP_RVIS_EVS,dbNSFP_RVIS_percentile_EVS,dbNSFP_LoF-FDR_ExAC,dbNSFP_RVIS_ExAC,dbNSFP_RVIS_percentile_ExAC,dbNSFP_GHIS,dbNSFP_ExAC_pLI,dbNSFP_ExAC_pRec,dbNSFP_ExAC_pNull,dbNSFP_ExAC_nonTCGA_pLI,dbNSFP_ExAC_nonTCGA_pRec,dbNSFP_ExAC_nonTCGA_pNull,dbNSFP_ExAC_nonpsych_pLI,dbNSFP_ExAC_nonpsych_pRec,dbNSFP_ExAC_nonpsych_pNull,dbNSFP_ExAC_del.score,dbNSFP_ExAC_dup.score,dbNSFP_ExAC_cnv.score,dbNSFP_ExAC_cnv_flag,dbNSFP_GDI,dbNSFP_GDI-Phred,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_Gene,dbNSFP_LoFtool_score,dbNSFP_SORVA_LOF_MAF0.005_HetOrHom,dbNSFP_SORVA_LOF_MAF0.005_HomOrCompoundHet,dbNSFP_SORVA_LOF_MAF0.001_HetOrHom,dbNSFP_SORVA_LOF_MAF0.001_HomOrCompoundHet,dbNSFP_SORVA_LOForMissense_MAF0.005_HetOrHom,dbNSFP_SORVA_LOForMissense_MAF0.005_HomOrCompoundHet,dbNSFP_SORVA_LOForMissense_MAF0.001_HetOrHom,dbNSFP_SORVA_LOForMissense_MAF0.001_HomOrCompoundHet,dbNSFP_Essential_gene,dbNSFP_MGI_mouse_gene,dbNSFP_MGI_mouse_phenotype,dbNSFP_ZFIN_zebrafish_gene,dbNSFP_ZFIN_zebrafish_structure,dbNSFP_ZFIN_zebrafish_phenotype_quality,dbNSFP_ZFIN_zebrafish_phenotype_tag',            'file': pysam.Tabixfile('../dbnsfp/dbnsfp.vcf.gz', 'r', encoding="utf-8")
        # }

        self.dbsnp = pysam.Tabixfile(settings.dbsnp, 'r', encoding="utf-8")

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting merge: ', self.vcffile)

        self.merge()

        tend = datetime.now()
        annotation_time = tend - tstart
        print(tend, 'Finished merge, it took: ', annotation_time)

        # merge VCF Files with VariantAnnotator

    def merge(self):

        BASE_DIR = os.getcwd()

        # get headers from files
        headers = []
        for annotation in self.annotation_files:
            # print(annotation, self.annotation_files[annotation])
            info = self.annotation_files[annotation]['info'].split(',')
            # print(info)
            ann_vcf_file = self.annotation_files[annotation]['file']

            # for line in str(ann_vcf_file.header):
            #     # print(annotation)
            #     if annotation == 'pynnotator':
            #         for tag in self.pynnotator_tags:
            #             string = '##INFO=<ID=%s.' % (tag)
            #             if line.startswith(string):
            #                 headers.append(line)
            #     else:
            #         for tag in info:
            #             string = '##INFO=<ID=%s,' % (tag)
            #             if line.startswith(string):
            #                 headers.append(line)

        output = open('annotation.final.vcf', 'w')
        input_vcf = open('../sanity_check/checked.vcf')
        for line in input_vcf:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    # write extra header
                    # for tag in headers:
                    #     # print(tag)
                    #     output.writelines(tag + '\n')
                    output.writelines(self.header)
                    output.writelines(line)
                else:
                    output.writelines(line)
            else:
                # here annotation comes!
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
                        records = ann_vcf_file.fetch(variant[0], int(variant[1]) - 1, int(variant[1]))
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

                new_info = variant[7] + ';' + ";".join(annotations)
                # print(new_info)
                variant[7] = new_info

                # now dbsnp

                try:
                    records = self.dbsnp.fetch(variant[0], int(variant[1]) - 1, int(variant[1]))
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
                        # compare ALT
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
        # merge 5 vcfs: snpeff, vep, snpsift, hi_index and hgmd 
        # print('merge snpeff')
        # snpeff
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MERGE all VCF Files from previous methods.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    merge = Merge(args.vcffile)
    merge.run()
