#!/usr/bin/python
# -*- coding: utf-8 -*-

#script to convert vcf to csv
import os
import csv

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-v", dest="vcf_file",
                  help="VCF File to Annotate", metavar="VCF")
(options, args) = parser.parse_args()

vcffile = options.vcf_file

vep_tags = 'Allele|Consequence|IMPACT|SYMBOL|Gene|Feature_type|Feature|BIOTYPE|EXON|INTRON|HGVSc|HGVSp|cDNA_position|CDS_position|Protein_position|Amino_acids|Codons|Existing_variation|DISTANCE|STRAND|FLAGS|SYMBOL_SOURCE|HGNC_ID|SIFT|PolyPhen|1000Gp3_AC|1000Gp3_AF|1000Gp3_AFR_AC|1000Gp3_AFR_AF|1000Gp3_AMR_AC|1000Gp3_AMR_AF|1000Gp3_EAS_AC|1000Gp3_EAS_AF|1000Gp3_EUR_AC|1000Gp3_EUR_AF|1000Gp3_SAS_AC|1000Gp3_SAS_AF|ALSPAC_AC|ALSPAC_AF|AltaiNeandertal|Ancestral_allele|CADD_phred|CADD_raw|CADD_raw_rankscore|DANN_rankscore|DANN_score|Denisova|ESP6500_AA_AC|ESP6500_AA_AF|ESP6500_EA_AC|ESP6500_EA_AF|Eigen-PC-phred|Eigen-PC-raw|Eigen-PC-raw_rankscore|Eigen-phred|Eigen-raw|Eigen_coding_or_noncoding|Ensembl_geneid|Ensembl_proteinid|Ensembl_transcriptid|ExAC_AC|ExAC_AF|ExAC_AFR_AC|ExAC_AFR_AF|ExAC_AMR_AC|ExAC_AMR_AF|ExAC_Adj_AC|ExAC_Adj_AF|ExAC_EAS_AC|ExAC_EAS_AF|ExAC_FIN_AC|ExAC_FIN_AF|ExAC_NFE_AC|ExAC_NFE_AF|ExAC_SAS_AC|ExAC_SAS_AF|ExAC_nonTCGA_AC|ExAC_nonTCGA_AF|ExAC_nonTCGA_AFR_AC|ExAC_nonTCGA_AFR_AF|ExAC_nonTCGA_AMR_AC|ExAC_nonTCGA_AMR_AF|ExAC_nonTCGA_Adj_AC|ExAC_nonTCGA_Adj_AF|ExAC_nonTCGA_EAS_AC|ExAC_nonTCGA_EAS_AF|ExAC_nonTCGA_FIN_AC|ExAC_nonTCGA_FIN_AF|ExAC_nonTCGA_NFE_AC|ExAC_nonTCGA_NFE_AF|ExAC_nonTCGA_SAS_AC|ExAC_nonTCGA_SAS_AF|ExAC_nonpsych_AC|ExAC_nonpsych_AF|ExAC_nonpsych_AFR_AC|ExAC_nonpsych_AFR_AF|ExAC_nonpsych_AMR_AC|ExAC_nonpsych_AMR_AF|ExAC_nonpsych_Adj_AC|ExAC_nonpsych_Adj_AF|ExAC_nonpsych_EAS_AC|ExAC_nonpsych_EAS_AF|ExAC_nonpsych_FIN_AC|ExAC_nonpsych_FIN_AF|ExAC_nonpsych_NFE_AC|ExAC_nonpsych_NFE_AF|ExAC_nonpsych_SAS_AC|ExAC_nonpsych_SAS_AF|FATHMM_converted_rankscore|FATHMM_pred|FATHMM_score|GERP++_NR|GERP++_RS|GERP++_RS_rankscore|GM12878_confidence_value|GM12878_fitCons_score|GM12878_fitCons_score_rankscore|GTEx_V6p_gene|GTEx_V6p_tissue|GenoCanyon_score|GenoCanyon_score_rankscore|H1-hESC_confidence_value|H1-hESC_fitCons_score|H1-hESC_fitCons_score_rankscore|HUVEC_confidence_value|HUVEC_fitCons_score|HUVEC_fitCons_score_rankscore|Interpro_domain|LRT_Omega|LRT_converted_rankscore|LRT_pred|LRT_score|M-CAP_pred|M-CAP_rankscore|M-CAP_score|MetaLR_pred|MetaLR_rankscore|MetaLR_score|MetaSVM_pred|MetaSVM_rankscore|MetaSVM_score|MutPred_AAchange|MutPred_Top5features|MutPred_protID|MutPred_rankscore|MutPred_score|MutationAssessor_UniprotID|MutationAssessor_pred|MutationAssessor_score|MutationAssessor_score_rankscore|MutationAssessor_variant|MutationTaster_AAE|MutationTaster_converted_rankscore|MutationTaster_model|MutationTaster_pred|MutationTaster_score|PROVEAN_converted_rankscore|PROVEAN_pred|PROVEAN_score|Polyphen2_HDIV_pred|Polyphen2_HDIV_rankscore|Polyphen2_HDIV_score|Polyphen2_HVAR_pred|Polyphen2_HVAR_rankscore|Polyphen2_HVAR_score|REVEL_rankscore|REVEL_score|Reliability_index|SIFT_converted_rankscore|SIFT_pred|SIFT_score|SiPhy_29way_logOdds|SiPhy_29way_logOdds_rankscore|SiPhy_29way_pi|TWINSUK_AC|TWINSUK_AF|Transcript_id_VEST3|Transcript_var_VEST3|Uniprot_aapos_Polyphen2|Uniprot_acc_Polyphen2|Uniprot_id_Polyphen2|VEST3_rankscore|VEST3_score|aapos|cds_strand|clinvar_clnsig|clinvar_golden_stars|clinvar_rs|clinvar_trait|codon_degeneracy|codonpos|fathmm-MKL_coding_group|fathmm-MKL_coding_pred|fathmm-MKL_coding_rankscore|fathmm-MKL_coding_score|genename|gnomAD_exomes_AC|gnomAD_exomes_AF|gnomAD_exomes_AFR_AC|gnomAD_exomes_AFR_AF|gnomAD_exomes_AFR_AN|gnomAD_exomes_AMR_AC|gnomAD_exomes_AMR_AF|gnomAD_exomes_AMR_AN|gnomAD_exomes_AN|gnomAD_exomes_ASJ_AC|gnomAD_exomes_ASJ_AF|gnomAD_exomes_ASJ_AN|gnomAD_exomes_EAS_AC|gnomAD_exomes_EAS_AF|gnomAD_exomes_EAS_AN|gnomAD_exomes_FIN_AC|gnomAD_exomes_FIN_AF|gnomAD_exomes_FIN_AN|gnomAD_exomes_NFE_AC|gnomAD_exomes_NFE_AF|gnomAD_exomes_NFE_AN|gnomAD_exomes_OTH_AC|gnomAD_exomes_OTH_AF|gnomAD_exomes_OTH_AN|gnomAD_exomes_SAS_AC|gnomAD_exomes_SAS_AF|gnomAD_exomes_SAS_AN|gnomAD_genomes_AC|gnomAD_genomes_AF|gnomAD_genomes_AFR_AC|gnomAD_genomes_AFR_AF|gnomAD_genomes_AFR_AN|gnomAD_genomes_AMR_AC|gnomAD_genomes_AMR_AF|gnomAD_genomes_AMR_AN|gnomAD_genomes_AN|gnomAD_genomes_ASJ_AC|gnomAD_genomes_ASJ_AF|gnomAD_genomes_ASJ_AN|gnomAD_genomes_EAS_AC|gnomAD_genomes_EAS_AF|gnomAD_genomes_EAS_AN|gnomAD_genomes_FIN_AC|gnomAD_genomes_FIN_AF|gnomAD_genomes_FIN_AN|gnomAD_genomes_NFE_AC|gnomAD_genomes_NFE_AF|gnomAD_genomes_NFE_AN|gnomAD_genomes_OTH_AC|gnomAD_genomes_OTH_AF|gnomAD_genomes_OTH_AN|integrated_confidence_value|integrated_fitCons_score|integrated_fitCons_score_rankscore|phastCons100way_vertebrate|phastCons100way_vertebrate_rankscore|phastCons20way_mammalian|phastCons20way_mammalian_rankscore|phyloP100way_vertebrate|phyloP100way_vertebrate_rankscore|phyloP20way_mammalian|phyloP20way_mammalian_rankscore|refcodon'.split('|')
# print(len(vep_tags))
snpeff_tags = 'Allele|Annotation|Annotation_Impact|Gene_Name|Gene_ID|Feature_Type|Feature_ID|Transcript_BioType|Rank|HGVS.c|HGVS.p|cDNA.pos/cDNA.length|CDS.pos/CDS.length|AA.pos/AA.length|Distance|ERRORS/WARNINGS/INFO'.split('|')

#Get all annotation tags from a VCF File reading all file (lazy mode!)
def get_all_info_tags(vcffile):
    tempfile = open(vcffile, 'r')
    annotation_tags = set()
    for line in tempfile:
        if not line.startswith('#'):
            variant = line.split('\t')
            string = variant[7].split(';')
            for element in string:
                element =  element.split('=')
                tag = element[0]        
                if tag not in annotation_tags:
                    annotation_tags.add(tag)
    tempfile.close()
    for item in vep_tags:
        annotation_tags.add('vep_'+item)    
    for item in snpeff_tags:
        annotation_tags.add('snpeff_'+item)    
    
    annotation_tags = sorted(annotation_tags)
    
    return annotation_tags
    
    
def parse_info_tag(string, annotation_tags):
    string = string.split(';')
    information = {}
    for element in string:
        element =  element.split('=',1)
        tag = element[0]
        if len(element) > 1:
            

            if tag == 'vep_csq':
                vep_info = element[1].split('|')
                # print(len(vep_info), vep_info)
                for i, vep_tag in enumerate(vep_tags):
                    # print(i,vep_tag)
                    information['vep_'+vep_tag] = vep_info[i]
            elif tag == 'snpeff_eff':
                snpeff_infos = element[1].split(',')
                # for snpeff_info in snpeff_infos:
                snpeff_info = snpeff_infos[0].split('|')
                for i, snpeff_tag in enumerate(snpeff_tags):
                    information['snpeff_'+snpeff_tag] = snpeff_info[i]

            else:
                information[tag] = element[1]

        else:
            information[tag] = 'Yes'
    information_list = []
    for tag in annotation_tags:
        if tag in information:
            information_list.append(str(information[tag]))
        else:
            information_list.append('')
    return information_list

def Get_vcfheader(filepath):
    vcffile = open(filepath, 'r')
    for line in vcffile:
        #print line
        if line.startswith("#CHROM"):
            header_tags = line.strip().split('\t')
            break
        #if not line.startswith("#"):
            
    vcffile.close()
    return header_tags

vcf_header = Get_vcfheader(vcffile)

annotation_tags = get_all_info_tags(vcffile)

vcf_header = vcf_header[:7] +  annotation_tags + vcf_header[8:]

csvfilename = ".".join(os.path.basename(vcffile).split('.')[:-1])+'.csv'
csvfilepath = os.path.join(os.path.dirname(vcffile), csvfilename)

readfile = open(vcffile, 'r')
f = open(csvfilepath, "w")
csvfile = csv.writer(f, quoting=csv.QUOTE_ALL)
csvfile.writerow(vcf_header)
for line in readfile:
    if line.startswith('#CHROM'):
        vcf_header_original = line.strip().split('\t')
        vcf_header_original = vcf_header_original[:7] + list(annotation_tags) + vcf_header_original[8:]
    if not line.startswith('#'):
        variant = line.strip().split('\t')
        information = parse_info_tag(variant[7], annotation_tags)
        variant = variant[:7] + information + variant[8:]
        csvfile.writerow(variant)
        
        #new_variant = []
        ##hack to old times
        
        #print vcf_header
        #print information
        #die()
        #for tag in vcf_header:
            #tag_index = vcf_header_original.index(tag)
            #new_variant.append(variant[tag_index])
        
f.close()
