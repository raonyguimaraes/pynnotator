import os

#annotator
scripts_dir = os.path.dirname(os.path.realpath(__file__))
ann_dir = scripts_dir.replace('/scripts', '')
data_dir = scripts_dir.replace('/scripts', '/data')

#tabix
tabix_version = '1.2.1'
tabix_base_name = 'htslib-%s' % (tabix_version)
tabix_path = '%s/libs/tabix/%s' % (ann_dir, tabix_base_name)
tabix_source = 'https://github.com/samtools/htslib/archive/%s.zip' % (tabix_version)

#vcftools
vcftools_basename = 'vcftools_0.1.10'
vcftools_file = 'vcftools_0.1.10.tar.gz'
vcftools_source = 'http://downloads.sourceforge.net/project/vcftools/vcftools_0.1.10.tar.gz'

#snpeff_source = 'http://downloads.sourceforge.net/project/snpeff/snpEff_latest_core.zip'
snpeff_version = 'snpEff_v4_0_core'
snpeff_source = 'http://sourceforge.net/projects/snpeff/files/%s.zip' % (snpeff_version)

snpeff_database = 'GRCh37.75'
# snpeff_database = 'GRCh37.64'

vep_release = '77'
vep_source = 'https://github.com/Ensembl/ensembl-tools/archive/release/%s.zip' % (vep_release)

vep_plugins_folder = 'VEP_plugins'
vep_plugins_source = 'https://github.com/ensembl-variation/VEP_plugins.git'


# vep_file = 'homo_sapiens_vep_75.tar.gz'

genomes1k_file = 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5a.20130502.sites.vcf.gz'
genomes1k_source = 'ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/%s' % (genomes1k_file)

dbsnp_file = '00-All.vcf.gz'
dbsnp_source = 'ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b144_GRCh37p13/VCF/%s' % (dbsnp_file)

clinvar_file = 'clinvar.vcf.gz'
clinvar_source = 'ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b144_GRCh37p13/VCF/clinical_vcf_set/%s' % (clinvar_file)

esp_file = 'ESP6500SI-V2-SSA137.protein-hgvs-update.snps_indels.vcf.tar.gz'
esp_source = 'http://evs.gs.washington.edu/evs_bulk_data/%s' % (esp_file)

dbnsfp_version = '2.9'

vcf_tools_path = '%s/libs/vcftools/vcftools_0.1.10' % (ann_dir)

#sanitycheck
#pure python and grep!

#annovar
#annovar_dir = '%s/libs/annovar041113/annovar' % (ann_dir)
# gatk_dir = '%s/libs/gatk' % (ann_dir)

#snpeff
#snpeff_2.0.5d
snpeff_dir = '%s/libs/snpeff/snpEff' % (ann_dir)
#snpsift
snpsift_dir = '%s/libs/snpeff/snpEff' % (ann_dir)

#vep
vep_dir = '%s/libs/vep/ensembl-tools-release-77/scripts/variant_effect_predictor' % (ann_dir)
vep_cache_dir = '%s/libs/vep/ensembl-tools-release-77/scripts/variant_effect_predictor/vep_cache' % (ann_dir)
vep_plugin_dir = '%s/Plugins' % (vep_cache_dir)

# vep_fasta = '%s/homo_sapiens/77_GRCh37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa' % (vep_cache_dir)

condel_plugin = 'Condel,%s/config/Condel/config,b' % (vep_plugin_dir)
#move .vep folder to libs DONE! Find a way to decrease the big space of this folder
#change path in file condel_SP.conf
#Example condel.dir='/projects/www/mendelmd_dev/annotator/libs/ensembl-tools-release-75/.vep/Plugins/config/Condel'


#reference = '%s/b37/human_g1k_v37.fasta' % (data_dir)
genomes1k_vcf = 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5a.20130502.sites.vcf'

genomes1k = '%s/1000genomes/ALL.wgs.phase3_shapeit2_mvncall_integrated_v5a.20130502.sites.vcf.gz' % (data_dir)
dbsnp = '%s/dbsnp/00-All.vcf.gz' % (data_dir)
dbsnp2 = '%s/dbsnp/00-All.vcf' % (data_dir)

clinvar = '%s/dbsnp/clinvar.vcf.gz' % (data_dir)
esp = '%s/esp6500/esp6500si.vcf.gz' % (data_dir)
dbnsfp = '%s/dbnsfp/dbNSFP2.9.txt.gz' % (data_dir)
dbscsnv = '%s/dbnsfp/dbscSNV1.1.txt.gz' % (data_dir)
dbscsnv_plugin = 'dbscSNV,%s' % (dbscsnv)



cadd_vest_cores = 2
pynnotator_cores = 2
vep_cores = 2
snpEff_memory = '4G' #8GB, 6G, 40G

hi_data = '%s/hi_index/hi_index.bed.gz' % (data_dir)
hgmd_data = '%s/hgmd/hgmd.sorted.bed.gz' % (data_dir)


#java Settings
java_file = 'jre-7u75-linux-x64.tar.gz'
java_source= 'http://javadl.sun.com/webapps/download/AutoDL?BundleId=101460'
java_path = '%s/libs/java/jre1.7.0_75/bin' % (ann_dir)
