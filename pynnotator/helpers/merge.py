
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from settings import *

import argparse
from datetime import datetime
import os, shutil
import shlex, subprocess
import csv

from settings import *

parser = argparse.ArgumentParser(description='MERGE all VCF Files from previous methods.')

parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')

args = parser.parse_args()

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
        print tstart, 'Starting merge: ', self.vcffile
        
        self.merge()

        tend = datetime.now()
        annotation_time =  tend - tstart
        print tend, 'Finished merge, it took: ', annotation_time        

    #merge VCF Files with VariantAnnotator
    def merge(self):

        BASE_DIR = os.getcwd()

        #merge 5 vcfs: snpeff, vep, snpsift, hi_index and hgmd 
        
        #snpeff
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar \
        annotate -info EFF -noId \
        ../snpeff/snpeff.output.vcf \
        ../sanity_check/checked.vcf \
        > snpeff.vcf \
        "% (java_path, snpsift_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)
        # print 'snpeff'

        #vep
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar \
        annotate -info CSQ -noId \
        ../vep/vep.output.sorted.vcf \
        snpeff.vcf \
        > snpeff.vep.vcf \
        "% (java_path, snpsift_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)
        
        #snpsift
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar \
        annotate -info VARTYPE,SNP,MNP,INS,DEL,MIXED,HOM,HET -noId \
        ../snpsift/snpsift.final.vcf \
        snpeff.vep.vcf \
        > snpsift.snpeff.vep.vcf \
        "% (java_path, snpsift_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        
        #hi_index
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar \
        annotate -info HI_INDEX -noId \
        ../hi_index/hi_index.vcf \
        snpsift.snpeff.vep.vcf \
        > hi_index.snpsift.snpeff.vep.vcf \
        "% (java_path, snpsift_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        #hgmd
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar \
        annotate -info HGMD -noId \
        ../hgmd/hgmd.vcf \
        hi_index.snpsift.snpeff.vep.vcf \
        > hgmd.hi_index.snpsift.snpeff.vep.vcf  \
        "% (java_path, snpsift_dir)


        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)
        

        #pynnotator - 1000genomes, dbsnp, clinvar, esp6500
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar \
        annotate -noId \
        ../pynnotator/pynnotator.vcf \
        hgmd.hi_index.snpsift.snpeff.vep.vcf \
        > 1kgenomes.dbsnp.clinvar.esp.hgmd.hi_index.snpsift.snpeff.vep.vcf  \
        " % (java_path, snpsift_dir)

        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        # print   'cadd vest'
        #cadd_vest
        command = "%s/java -Xmx40G -jar \
        %s/SnpSift.jar \
        annotate -noId -info dbNSFP_VEST3_rankscore,dbNSFP_VEST3_score,dbNSFP_CADD_phred,dbNSFP_CADD_raw_rankscore,dbNSFP_CADD_raw \
        ../cadd_vest/cadd_vest.vcf \
        1kgenomes.dbsnp.clinvar.esp.hgmd.hi_index.snpsift.snpeff.vep.vcf \
        > cadd_vest.1kgenomes.dbsnp.clinvar.esp.hgmd.hi_index.snpsift.snpeff.vep.vcf  \
        "% (java_path, snpsift_dir)


        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        #dbsnp
        command = "java -Xmx40G -jar \
        %s/SnpSift.jar \
        annotate -id \
        %s \
        cadd_vest.1kgenomes.dbsnp.clinvar.esp.hgmd.hi_index.snpsift.snpeff.vep.vcf \
        > annotation.final.vcf  \
        "% (snpsift_dir,dbsnp)


        p = subprocess.call(command, 
            cwd=os.getcwd(), 
            shell=True)

        

        # #var type
        # command = "java -Xmx40G -jar \
        # %s/SnpSift.jar \
        # annotate \
        # ../snpsift/snpsift.vartype.vcf \
        # hgmd.hi_index.snpsift.snpeff.vep.vcf \
        # > annotation.final.vcf \
        # "% (snpsift_dir)

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)




        # command = "java -Xmx40G -jar %s/GenomeAnalysisTK.jar \
        # -T VariantAnnotator \
        # -R %s \
        # -A SnpEff \
        # --alwaysAppendDbsnpId \
        # --snpEffFile %s/../snpeff/snpEff_output.vcf \
        # --variant %s/../%s \
        # -L %s/../%s \
        # -o annotation.final.vcf \
        # --dbsnp %s \
        # --log_to_file gatk_merge_report.log \
        # --resource:dbsnpann %s \
        # -E dbsnpann.CAF \
        # -E dbsnpann.dbSNPBuildID \
        # --resource:hi_index ../hi_index/hi_index.vcf \
        # -E hi_index.HI_INDEX \
        # --resource:snpsift ../snpsift/dbnfsp.vcf \
        # -E snpsift.dbnsfpGERP++_RS \
        # -E snpsift.dbnsfp1000Gp1_ASN_AF \
        # -E snpsift.dbnsfpEnsembl_transcriptid \
        # -E snpsift.dbnsfpUniprot_acc \
        # -E snpsift.dbnsfpESP6500_AA_AF \
        # -E snpsift.dbnsfp29way_logOdds \
        # -E snpsift.dbnsfp1000Gp1_AFR_AF \
        # -E snpsift.dbnsfp1000Gp1_EUR_AF \
        # -E snpsift.dbnsfpESP6500_EA_AF \
        # -E snpsift.dbnsfp1000Gp1_AMR_AF \
        # -E snpsift.dbnsfpGERP++_NR \
        # -E snpsift.dbnsfp1000Gp1_AF \
        # -E snpsift.dbnsfpPolyphen2_HVAR_pred \
        # -E snpsift.dbnsfpInterpro_domain \
        # -E snpsift.dbnsfpSIFT_score \
        # --resource:1000genomes %s \
        # -E 1000genomes.AF \
        # --resource:exome_server %s \
        # -E exome_server.MAF \
        # --resource:vep ../vep/output.checked.vcf \
        # -E vep.CSQ \
        # -nt 4 \
        # " % (gatk_dir, reference, BASE_DIR, BASE_DIR, self.vcffile, BASE_DIR, self.vcffile, dbsnp, dbsnp, genomes1k, evs)
        #removed vep to make it fast and free
        # --resource:annovar ../annovar/annovar.vcf \
        # -E annovar.Func_refGene \
        # -E annovar.Gene_refGene \
        # -E annovar.ExonicFunc_refGene \
        # -E annovar.AAChange_refGene \
        # -E annovar.phastConsElements46way \
        # -E annovar.genomicSuperDups \
        # -E annovar.esp6500si_all \
        # -E annovar.1000g2012apr_all \
        # -E annovar.LJB2_SIFT \
        # -E annovar.LJB2_PolyPhen2_HDIV \
        # -E annovar.LJB2_PP2_HDIV_Pred \
        # -E annovar.LJB2_PolyPhen2_HVAR \
        # -E annovar.LJB2_PolyPhen2_HVAR_Pred \
        # -E annovar.LJB2_LRT \
        # -E annovar.LJB2_LRT_Pred \
        # -E annovar.LJB2_MutationTaster \
        # -E annovar.LJB2_MutationTaster_Pred \
        # -E annovar.LJB_MutationAssessor \
        # -E annovar.LJB_MutationAssessor_Pred \
        # -E annovar.LJB2_FATHMM \
        # -E annovar.LJB2_GERP++ \
        # -E annovar.LJB2_PhyloP \
        # -E annovar.LJB2_SiPhy \
        # -E annovar.cosmic65 \
        # -E annovar.avsift \
        
        # 
        #--useAllAnnotations \

        # p = subprocess.call(command, 
        #     cwd=os.getcwd(), 
        #     shell=True)

        if p == 0:
            print 'This vcf was succesfully merged'
        else:
            print 'Sorry this vcf could not be merged'


if  __name__ == '__main__' :
    merge = Merge(args.vcffile)
    merge.run()