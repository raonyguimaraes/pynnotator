import os

#LIBS SETTINGS
BASE_DIR = os.path.dirname(__file__)
libs_dir = os.path.join(BASE_DIR, 'libs')
data_dir = os.path.join(BASE_DIR, 'data')

###LIBS

#htslib (tabix)
htslib_version = 'htslib-1.3.1'
htslib_file = '%s.tar.bz2' % (htslib_version)
htslib_source = 'https://github.com/samtools/htslib/releases/download/1.3.1/%s' % (htslib_file)

#vcftools
vcftools_version = '0.1.14'
vcftools_file = 'vcftools-%s.tar.gz' % (vcftools_version)
vcftools_source = 'https://github.com/vcftools/vcftools/releases/download/v%s/vcftools-%s.tar.gz' % (vcftools_version, vcftools_version)

#snpeff
snpeff_database = 'GRCh37.75' # this is the last build from GRCh37
snpeff_version = 'snpEff_latest_core'
snpeff_source = 'http://sourceforge.net/projects/snpeff/files/%s.zip' % (snpeff_version)
snpeff_dir = os.path.join(libs_dir, 'snpeff', 'snpEff')
snpeff_data_dir = os.path.join(data_dir, 'snpeff_data')

#vep
vep_release = '84'
vep_source = 'https://github.com/Ensembl/ensembl-tools/archive/release/%s.zip' % (vep_release)
vep_cache_dir = os.path.join(data_dir, 'vep_cache')
vep_dir = '%s/vep/ensembl-tools-release-%s/scripts/variant_effect_predictor' % (libs_dir, vep_release)

###Datasets

#1000genomes
genomes1k_vcf = 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf'
genomes1k_file = '%s.gz' % (genomes1k_vcf)
genomes1k_source = 'ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/%s' % (genomes1k_file)

#dbsnp
dbsnp_file = 'All_20160408.vcf'
dbsnp_source = 'ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b147_GRCh37p13/VCF/%s.gz' % (dbsnp_file)

clinvar_file = 'clinvar.vcf.gz'
clinvar_source = 'ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/%s' % (clinvar_file)

#ESP
esp_basename = 'ESP6500SI-V2-SSA137.GRCh38-liftover'
esp_file = '%s.snps_indels.vcf.tar.gz' % (esp_basename)
esp_source = 'http://evs.gs.washington.edu/evs_bulk_data/%s' % (esp_file)

#dbnsfp
dbnsfp_version = '3.2a'
dbnsfp_file = 'dbNSFP%s.txt.gz' % (dbnsfp_version)
dbnsfp_link = 'ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbNSFPv%s.zip' % (dbnsfp_version)
