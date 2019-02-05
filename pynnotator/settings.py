import os

###MAIN SETTINGS

snpEff_memory = "4G"
snpsift_memory = "4G"
snpsift_merge_memory = "4G"
vep_cores = 4
vcf_annotator_cores = 4
dbnsfp_cores = 4
vcfanno_cores = 4

# LIBS SETTINGS
BASE_DIR = os.path.dirname(__file__)
libs_dir = os.path.join(BASE_DIR, 'libs')
data_dir = os.path.join(BASE_DIR, 'data')

###LIBS

# htslib (tabix)
htslib_version = '1.9'
htslib_file = 'htslib-%s.tar.bz2' % (htslib_version)
htslib_source = 'https://github.com/samtools/htslib/releases/download/%s/%s' % (htslib_version, htslib_file)
htslib_dir = '%s/htslib/htslib-%s' % (libs_dir, htslib_version)

vcfanno_dir = '%s/vcfanno/' % (libs_dir)

# vcftools
vcftools_version = '0.1.16'
vcftools_file = 'vcftools-%s.tar.gz' % (vcftools_version)
vcftools_source = 'https://github.com/vcftools/vcftools/releases/download/v%s/vcftools-%s.tar.gz' % (
    vcftools_version, vcftools_version)
# validation
vcftools_dir = "%s/vcftools/vcftools-%s/src/cpp" % (libs_dir, vcftools_version)
vcftools_dir_perl = "%s/vcftools/vcftools-%s/src/perl" % (libs_dir, vcftools_version)
vcf_validator_dir = "%s/vcf-validator" % (libs_dir)

# snpeff
snpeff_database = 'GRCh37.75'  # this is the last build from GRCh37
snpeff_version = 'snpEff_latest_core'
snpeff_version = 'snpEff_v4_3t_core'  # need to test version 4.3
snpeff_source = 'http://sourceforge.net/projects/snpeff/files/%s.zip' % (snpeff_version)

snpeff_dir = os.path.join(libs_dir, 'snpeff', 'snpEff')
snpeff_data_dir = os.path.join(data_dir, 'snpeff_data')

# vep
vep_release = '95.1'
vep_source = 'https://github.com/Ensembl/ensembl-vep/archive/release/%s.zip' % (vep_release)
vep_cache_dir = os.path.join(data_dir, 'vep_data')
vep_dir = '%s/vep/src/ensembl-vep/' % (libs_dir)

# gemini
gemini_file = 'gemini_install.py'
gemini_source = 'https://github.com/arq5x/gemini/raw/master/gemini/scripts/%s' % (gemini_file)

###Datasets

# Decipher
hi_predictions_file = 'HI_Predictions_Version3.bed.gz'
hi_predictions_source = 'https://decipher.sanger.ac.uk/files/downloads/%s' % (hi_predictions_file)
hi_predictions = '%s/decipher/%s' % (data_dir, hi_predictions_file)

population_cnv_file = 'population_cnv.txt.gz'
population_cnv_source = 'https://decipher.sanger.ac.uk/files/downloads/%s' % (population_cnv_file)

ddg2p_file = 'DDG2P.csv.gz'
ddg2p_source = 'http://www.ebi.ac.uk/gene2phenotype/downloads/%s' % (ddg2p_file)

# ensembl #HGMD PUBLIC
vep_major_release = '95'
ensembl_phenotype_file = 'homo_sapiens_phenotype_associated.vcf.gz'
ensembl_phenotype_source = 'ftp://ftp.ensembl.org/pub/grch37/release-%s/variation/vcf/homo_sapiens/%s' % (
    vep_major_release, ensembl_phenotype_file)

ensembl_clinically_file = 'homo_sapiens_clinically_associated.vcf.gz'
ensembl_clinically_source = 'ftp://ftp.ensembl.org/pub/grch37/release-%s/variation/vcf/homo_sapiens/%s' % (
    vep_major_release, ensembl_clinically_file)

# 1000genomes
genomes1k_vcf = 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf'
genomes1k_file = '%s.gz' % (genomes1k_vcf)
genomes1k_source = 'ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/%s' % (genomes1k_file)

# dbsnp
dbsnp_file = 'All_20180423.vcf.gz'
dbsnp_source = 'ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/%s' % (dbsnp_file)
dbsnp = '%s/dbsnp/%s' % (data_dir, dbsnp_file)

clinvar_file = 'clinvar.vcf.gz'
clinvar_source = 'ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/%s' % (clinvar_file)

# ESP
esp_basename = 'ESP6500SI-V2-SSA137.GRCh38-liftover'
esp_file = '%s.snps_indels.vcf.tar.gz' % (esp_basename)
esp_source = 'http://evs.gs.washington.edu/evs_bulk_data/%s' % (esp_file)
esp_final_file = 'esp6500si.vcf.gz'

# dbnsfp
dbnsfp_version = '3.5a'
dbnsfp_file = 'dbNSFP%s.txt.gz' % (dbnsfp_version)
dbnsfp_link = 'ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFPv%s.zip' % (dbnsfp_version)
dbnsfp = '%s/dbnsfp/dbNSFP%s.txt.gz' % (data_dir, dbnsfp_version)

# dbscsnv
dbscsnv_version = '1.1'
dbscsnv_file = 'dbscSNV%s.txt.gz' % (dbscsnv_version)
dbscsnv_source = 'ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbscSNV%s.zip' % (dbscsnv_version)
dbscsnv = '%s/dbnsfp/dbscSNV%s.txt.gz' % (data_dir, dbscsnv_version)

data_file = "pynnotator-data.latest.tar"
data_source = "https://mendelmd.org/%s" % (data_file)

libs_file = "pynnotator-libs.latest.tar.gz"
libs_source = "https://mendelmd.org/%s" % (libs_file)

