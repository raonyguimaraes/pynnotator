#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
from datetime import datetime
from subprocess import call

from pynnotator import settings

toolname = 'vep'


class Vep(object):
    def __init__(self, vcffile=None):

        self.vcffile = vcffile

        self.filename = os.path.splitext(os.path.basename(str(vcffile)))[0]

        # create folder vep if it doesn't exists
        if not os.path.exists('vep'):
            os.makedirs('vep')
            # enter inside folder
            # os.chdir('vep')

    def install(self):
        print('install')

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting vep annotation: ', self.vcffile)

        self.annotate()

        tend = datetime.now()
        annotation_time = tend - tstart
        print(tend, 'Finished vep annotation, it took: ', annotation_time)

    # convert and annotate the vcf file to vep
    def annotate(self):

        command = '''perl %s/vep \
        -i %s \
        --cache \
        --dir %s \
        --offline \
        --format vcf \
        -o vep/vep.output.vcf --vcf --force_overwrite \
        --assembly GRCh37 \
        -sift b -polyphen b \
        -plugin dbNSFP,%s,genename,cds_strand,refcodon,codonpos,codon_degeneracy,Ancestral_allele,AltaiNeandertal,Denisova,Ensembl_geneid,Ensembl_transcriptid,Ensembl_proteinid,aapos,SIFT_score,SIFT_converted_rankscore,SIFT_pred,Uniprot_acc_Polyphen2,Uniprot_id_Polyphen2,Uniprot_aapos_Polyphen2,Polyphen2_HDIV_score,Polyphen2_HDIV_rankscore,Polyphen2_HDIV_pred,Polyphen2_HVAR_score,Polyphen2_HVAR_rankscore,Polyphen2_HVAR_pred,LRT_score,LRT_converted_rankscore,LRT_pred,LRT_Omega,MutationTaster_score,MutationTaster_converted_rankscore,MutationTaster_pred,MutationTaster_model,MutationTaster_AAE,MutationAssessor_UniprotID,MutationAssessor_variant,MutationAssessor_score,MutationAssessor_score_rankscore,MutationAssessor_pred,FATHMM_score,FATHMM_converted_rankscore,FATHMM_pred,PROVEAN_score,PROVEAN_converted_rankscore,PROVEAN_pred,Transcript_id_VEST3,Transcript_var_VEST3,VEST3_score,VEST3_rankscore,MetaSVM_score,MetaSVM_rankscore,MetaSVM_pred,MetaLR_score,MetaLR_rankscore,MetaLR_pred,Reliability_index,M-CAP_score,M-CAP_rankscore,M-CAP_pred,REVEL_score,REVEL_rankscore,MutPred_score,MutPred_rankscore,MutPred_protID,MutPred_AAchange,MutPred_Top5features,CADD_raw,CADD_raw_rankscore,CADD_phred,DANN_score,DANN_rankscore,fathmm-MKL_coding_score,fathmm-MKL_coding_rankscore,fathmm-MKL_coding_pred,fathmm-MKL_coding_group,Eigen_coding_or_noncoding,Eigen-raw,Eigen-phred,Eigen-PC-raw,Eigen-PC-phred,Eigen-PC-raw_rankscore,GenoCanyon_score,GenoCanyon_score_rankscore,integrated_fitCons_score,integrated_fitCons_score_rankscore,integrated_confidence_value,GM12878_fitCons_score,GM12878_fitCons_score_rankscore,GM12878_confidence_value,H1-hESC_fitCons_score,H1-hESC_fitCons_score_rankscore,H1-hESC_confidence_value,HUVEC_fitCons_score,HUVEC_fitCons_score_rankscore,HUVEC_confidence_value,GERP++_NR,GERP++_RS,GERP++_RS_rankscore,phyloP100way_vertebrate,phyloP100way_vertebrate_rankscore,phyloP20way_mammalian,phyloP20way_mammalian_rankscore,phastCons100way_vertebrate,phastCons100way_vertebrate_rankscore,phastCons20way_mammalian,phastCons20way_mammalian_rankscore,SiPhy_29way_pi,SiPhy_29way_logOdds,SiPhy_29way_logOdds_rankscore,1000Gp3_AC,1000Gp3_AF,1000Gp3_AFR_AC,1000Gp3_AFR_AF,1000Gp3_EUR_AC,1000Gp3_EUR_AF,1000Gp3_AMR_AC,1000Gp3_AMR_AF,1000Gp3_EAS_AC,1000Gp3_EAS_AF,1000Gp3_SAS_AC,1000Gp3_SAS_AF,TWINSUK_AC,TWINSUK_AF,ALSPAC_AC,ALSPAC_AF,ESP6500_AA_AC,ESP6500_AA_AF,ESP6500_EA_AC,ESP6500_EA_AF,ExAC_AC,ExAC_AF,ExAC_Adj_AC,ExAC_Adj_AF,ExAC_AFR_AC,ExAC_AFR_AF,ExAC_AMR_AC,ExAC_AMR_AF,ExAC_EAS_AC,ExAC_EAS_AF,ExAC_FIN_AC,ExAC_FIN_AF,ExAC_NFE_AC,ExAC_NFE_AF,ExAC_SAS_AC,ExAC_SAS_AF,ExAC_nonTCGA_AC,ExAC_nonTCGA_AF,ExAC_nonTCGA_Adj_AC,ExAC_nonTCGA_Adj_AF,ExAC_nonTCGA_AFR_AC,ExAC_nonTCGA_AFR_AF,ExAC_nonTCGA_AMR_AC,ExAC_nonTCGA_AMR_AF,ExAC_nonTCGA_EAS_AC,ExAC_nonTCGA_EAS_AF,ExAC_nonTCGA_FIN_AC,ExAC_nonTCGA_FIN_AF,ExAC_nonTCGA_NFE_AC,ExAC_nonTCGA_NFE_AF,ExAC_nonTCGA_SAS_AC,ExAC_nonTCGA_SAS_AF,ExAC_nonpsych_AC,ExAC_nonpsych_AF,ExAC_nonpsych_Adj_AC,ExAC_nonpsych_Adj_AF,ExAC_nonpsych_AFR_AC,ExAC_nonpsych_AFR_AF,ExAC_nonpsych_AMR_AC,ExAC_nonpsych_AMR_AF,ExAC_nonpsych_EAS_AC,ExAC_nonpsych_EAS_AF,ExAC_nonpsych_FIN_AC,ExAC_nonpsych_FIN_AF,ExAC_nonpsych_NFE_AC,ExAC_nonpsych_NFE_AF,ExAC_nonpsych_SAS_AC,ExAC_nonpsych_SAS_AF,gnomAD_exomes_AC,gnomAD_exomes_AN,gnomAD_exomes_AF,gnomAD_exomes_AFR_AC,gnomAD_exomes_AFR_AN,gnomAD_exomes_AFR_AF,gnomAD_exomes_AMR_AC,gnomAD_exomes_AMR_AN,gnomAD_exomes_AMR_AF,gnomAD_exomes_ASJ_AC,gnomAD_exomes_ASJ_AN,gnomAD_exomes_ASJ_AF,gnomAD_exomes_EAS_AC,gnomAD_exomes_EAS_AN,gnomAD_exomes_EAS_AF,gnomAD_exomes_FIN_AC,gnomAD_exomes_FIN_AN,gnomAD_exomes_FIN_AF,gnomAD_exomes_NFE_AC,gnomAD_exomes_NFE_AN,gnomAD_exomes_NFE_AF,gnomAD_exomes_SAS_AC,gnomAD_exomes_SAS_AN,gnomAD_exomes_SAS_AF,gnomAD_exomes_OTH_AC,gnomAD_exomes_OTH_AN,gnomAD_exomes_OTH_AF,gnomAD_genomes_AC,gnomAD_genomes_AN,gnomAD_genomes_AF,gnomAD_genomes_AFR_AC,gnomAD_genomes_AFR_AN,gnomAD_genomes_AFR_AF,gnomAD_genomes_AMR_AC,gnomAD_genomes_AMR_AN,gnomAD_genomes_AMR_AF,gnomAD_genomes_ASJ_AC,gnomAD_genomes_ASJ_AN,gnomAD_genomes_ASJ_AF,gnomAD_genomes_EAS_AC,gnomAD_genomes_EAS_AN,gnomAD_genomes_EAS_AF,gnomAD_genomes_FIN_AC,gnomAD_genomes_FIN_AN,gnomAD_genomes_FIN_AF,gnomAD_genomes_NFE_AC,gnomAD_genomes_NFE_AN,gnomAD_genomes_NFE_AF,gnomAD_genomes_OTH_AC,gnomAD_genomes_OTH_AN,gnomAD_genomes_OTH_AF,clinvar_rs,clinvar_clnsig,clinvar_trait,clinvar_golden_stars,Interpro_domain,GTEx_V6p_gene,GTEx_V6p_tissue \
        --no_progress \
        --no_intergenic \
        --numbers \
        --biotype \
        --total_length \
        --coding_only \
        --pick \
        --symbol \
        1>vep/vep.log \
        --fork %s \
        ''' % (settings.vep_dir, self.vcffile, settings.vep_cache_dir, settings.dbnsfp, settings.vep_cores)
        # 1> vepreport.log \
        ##--pick \
        # condel_plugin, dbscsnv_plugin, 
        # -plugin %s \
        # --plugin %s \

        p = subprocess.call(command,
                            cwd=os.getcwd(),
                            shell=True)

        tend = datetime.now()

        # if p == 0:
        #     print(tend, 'This vcf was sucessfully annotated by %s!' % (toolname))
        # else:
        #     print(tend, 'Sorry this vcf could not be annotated by %s' % (toolname))

        # command = '(grep ^# output.vep.vcf; grep -v ^# output.vep.vcf|sort -k1,1N -k2,2n) > output.vep.sorted.vcf'
        # Sort VCF file 


        command = '''grep '^#' vep/vep.output.vcf > vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        command = '''grep -E -v '^X|^Y|^M|^#|^GL' vep/vep.output.vcf | sort -n -k1 -k2 >> vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        command = '''grep -E '^X' vep/vep.output.vcf | sort -k1,1d -k2,2n >> vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        command = '''grep -E '^Y' vep/vep.output.vcf | sort -k1,1d -k2,2n >> vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        command = '''grep -E '^M' vep/vep.output.vcf | sort -k1,1d -k2,2n >> vep/vep.output.sorted.vcf'''
        call(command, shell=True)

        tend = datetime.now()
        # print(tend, 'Finished sorting vep vcf.')

        command = 'rm vep/vep.output.vcf'
        call(command, shell=True)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate a VCF File with VEP.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    args = parser.parse_args()

    vep = Vep(args.vcffile)
    vep.run()
