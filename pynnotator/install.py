#!/usr/bin/python

import os
import platform
import subprocess
from subprocess import call
import distro
from . import settings

BASE_DIR = os.path.dirname(__file__)
libs_dir = os.path.join(BASE_DIR, 'libs')
data_dir = os.path.join(BASE_DIR, 'data')


class Installer(object):
    """A class to annotate VCFs
  
    Attributes:
        vcf_file: a VCF file to be annotated
    """

    def __init__(self):
        """Return a Pynnotator Installer object """

    def install(self):

        self.install_requirements()        
        #self.download_libs()
        self.download_data()
        self.install_libs()
        self.build_datasets()

    def install_requirements(self):
        """Install Ubuntu Requirements"""
        print('Installing Requirements')
        print(distro.linux_distribution())
        linux_dist = distro.linux_distribution()

        if linux_dist[0] in ['Ubuntu', 'LinuxMint']:
            command = 'sudo apt-get install -y gcc git python3-dev zlib1g-dev make zip libssl-dev libbz2-dev liblzma-dev libcurl4-openssl-dev build-essential libxml2-dev apache2 zlib1g-dev bcftools build-essential cpanminus curl git libbz2-dev libcurl4-openssl-dev liblocal-lib-perl liblzma-dev libmysqlclient-dev libpng-dev libpq-dev libssl-dev manpages mysql-client openssl perl perl-base pkg-config python3-dev python3-pip python3-setuptools sed tabix unzip vcftools vim wget zlib1g-dev apache2 build-essential cpanminus curl git libmysqlclient-dev libpng-dev libssl-dev locales manpages mysql-client openssl perl perl-base unzip vim wget libgd-dev'  # lamp-server^
            sts = call(command, shell=True)

            try:
                subprocess.call(['java', '-version'])
            except:

                command = """sudo apt install -y openjdk-8-jdk"""
                sts = call(command, shell=True)
        elif linux_dist[0] in ['debian']:
            command = 'sudo apt-get update'
            sts = call(command, shell=True)

            command = 'sudo apt-get install -y libmodule-install-perl apache2 bcftools build-essential cpanminus curl git libbz2-dev libcurl4-openssl-dev liblocal-lib-perl liblzma-dev default-libmysqlclient-dev libpng-dev libpq-dev libssl-dev manpages mysql-client openssl perl perl-base pkg-config python3-dev python3-pip python3-setuptools sed tabix unzip vcftools vim wget zlib1g-dev apache2 build-essential cpanminus curl git libpng-dev libssl-dev locales manpages mysql-client openssl perl perl-base unzip vim wget libgd-dev libxml-libxml-perl libgd-dev'  # lamp-server^
            sts = call(command, shell=True)
            command = 'sudo apt-get install -y default-jre default-jdk'
            sts = call(command, shell=True)
        
        elif linux_dist[0] in ['redhat', 'centos']:

            command = 'sudo yum install libcurl-devel sed vcftools bcftools tabix zlib-devel postgresql96-libs perl-local-lib perl-App-cpanminus curl unzip wget'
            sts = call(command, shell=True)
            command = """sudo yum groupinstall 'Development Tools'"""
            sts = call(command, shell=True)
            command = """sudo yum install gcc gcc-c++ make openssl-devel"""
            sts = call(command, shell=True)

            try:
                subprocess.call(['java', '-version'])
            except:
                command = "sudo yum install -y java-1.8.0-openjdk"
                sts = call(command, shell=True)
        # Perl Requirements
        command = "sudo cpanm DBI DBD::mysql File::Copy::Recursive Archive::Extract Archive::Zip LWP::Simple Bio::Root::Version LWP::Protocol::https Bio::DB::Fasta CGI Test::utf8 Test::File inc::Module::Install XML::DOM::XPath XML::LibXML"
        sts = call(command, shell=True)
        command = "sudo cpanm --local-lib=~/perl5 local::lib && eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)"
        sts = call(command, shell=True)
    def install_libs(self):

        if not os.path.exists(libs_dir):
            os.makedirs(libs_dir)
        os.chdir(libs_dir)

        # self.install_java()

        self.install_htslib()
        self.install_vcftools()
        self.install_snpeff()
        self.install_gemini()
        self.install_vep()
        self.install_vcf_anno()

    def build_datasets(self):
        print("Building Datasets")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        os.chdir(data_dir)

        self.download_snpeff_data()
        self.download_vep_data()

        self.download_decipher()
        self.download_ensembl()
        self.download_1000genomes()
        self.download_dbsnp()
        self.download_esp()
        self.download_dbnsfp()

    def download_data(self):
        print("Downloading Data")

        os.chdir(settings.BASE_DIR)

        if not os.path.exists(settings.data_dir):
            command = "wget %s -O %s" % (settings.data_source, settings.data_file)
            call(command, shell=True)

            print("Extracting Data...")
            command = "tar -xvf %s" % (settings.data_file)
            call(command, shell=True)

            print("Deleting Compressed File...")
            command = "rm %s" % (settings.data_file)
            call(command, shell=True)

    def download_libs(self):
        print("Downloading Libs")

        os.chdir(settings.BASE_DIR)

        if not os.path.exists(settings.libs_dir):
            command = "wget %s -O %s" % (settings.libs_source, settings.libs_file)
            call(command, shell=True)

            print("Extracting Data...")
            command = "tar -zxvf %s" % (settings.libs_file)
            call(command, shell=True)

            print("Deleting Compressed File...")
            command = "rm %s" % (settings.libs_file)
            # call(command, shell=True)

    def install_java(self):
        if not os.path.isdir('java'):
            call('mkdir java', shell=True)
        os.chdir('java')

        # check if file exists
        if not os.path.isfile(java_file):
            command = """
            wget -c %s -O %s
            tar -zxvf %s
            """ % (settings.java_source, settings.java_file, settings.java_file)
            call(command, shell=True)

        os.chdir(libs_dir)

    def install_htslib(self):
        if not os.path.isdir('htslib'):
            call('mkdir htslib', shell=True)

        os.chdir('htslib')
        # check if file exists
        if not os.path.isfile(settings.htslib_file):
            command = """
            wget -c %s
            tar -jxvf %s
            cd htslib-%s; ./configure; make
            """ % (settings.htslib_source, settings.htslib_file, settings.htslib_version)

            call(command, shell=True)

        os.chdir(libs_dir)

    def install_vcftools(self):
        if not os.path.isdir('vcftools'):
            call('mkdir vcftools', shell=True)
        os.chdir('vcftools')
        # check if file exists
        if not os.path.isfile(settings.vcftools_file):
            command = """
            wget -c %s
            tar -zxvf %s
            cd vcftools-%s
            ./configure; make
            """ % (settings.vcftools_source, settings.vcftools_file, settings.vcftools_version)
            call(command, shell=True)

        os.chdir(libs_dir)

    def install_snpeff(self):
        if not os.path.isdir('snpeff'):
            call('mkdir snpeff', shell=True)
        os.chdir('snpeff')
        # check if file exists
        if not os.path.isfile('%s.zip' % (settings.snpeff_version)):
            command = """
            wget -c %s
            unzip %s.zip
            """ % (settings.snpeff_source, settings.snpeff_version)
            call(command, shell=True)

            # change data_dir
            # from ./data/ to data.dir = ../../../data/snpeff_data
            command = """
            sed -i 's/\.\/data\//\.\.\/\.\.\/\.\.\/data\/snpeff_data/g' snpEff/snpEff.config"""
            call(command, shell=True)

        os.chdir(libs_dir)

    def install_gemini(self):
        if not os.path.isdir('gemini'):
            call('mkdir gemini', shell=True)
        os.chdir('gemini')
        # check if file exists
        if not os.path.isfile(settings.gemini_file):
            command = 'wget -c %s -O %s' % (settings.gemini_source, settings.gemini_file)
            call(command, shell=True)

        os.chdir(libs_dir)

    def install_vep(self):

        os.chdir(libs_dir)
        if not os.path.exists('vep'):
            os.makedirs('vep')
            os.chdir('vep')
            command = 'bash {}/scripts/install_vep.sh'.format(settings.BASE_DIR)
            call(command, shell=True)
    def install_vcf_anno(self):

        os.chdir(libs_dir)
        if not os.path.exists('vcfanno'):
            os.makedirs('vcfanno')
            os.chdir('vcfanno')
            command = 'wget https://github.com/brentp/vcfanno/releases/download/v0.2.9/vcfanno_linux64'
            call(command, shell=True)
            command = 'chmod +x vcfanno_linux64'
            call(command, shell=True)
        
        # if not os.path.isfile('%s.zip' % (settings.vep_release)):
        #     command = """
        #     wget %s -O %s.zip
        #     unzip %s.zip
        #     """ % (settings.vep_source, settings.vep_release, settings.vep_release)
        #     call(command, shell=True)
        #
        #     os.chdir(settings.vep_dir)
            # download vep cache
            # command = """perl INSTALL.pl -a a --NO_TEST"""

        os.chdir(libs_dir)

    def download_snpeff_data(self):

        # download snpeff data
        if not os.path.isdir(os.path.join(settings.snpeff_data_dir, settings.snpeff_database)):
            command = "java -jar %s/snpEff.jar download -c %s/snpEff.config -v %s" % (
                settings.snpeff_dir, settings.snpeff_dir, settings.snpeff_database)
            call(command, shell=True)

    def download_vep_data(self):

        if not os.path.isdir(settings.vep_dir):
            command = 'mkdir -p {}'.format(settings.vep_dir)
            call(command, shell=True)

        os.chdir(settings.vep_dir)
        # download vep cache
        if not os.path.isdir(settings.vep_cache_dir):
            command = """perl ./INSTALL.pl -a acf -s homo_sapiens -c %s --ASSEMBLY GRCh37 --NO_TEST
            """ % (settings.vep_cache_dir)
            call(command, shell=True)

        if not os.path.isdir('{}/Plugins'.format(settings.vep_cache_dir)):
            command = 'mkdir -p {}/Plugins'.format(settings.vep_cache_dir)
            call(command, shell=True)
        if not os.path.isfile('{}/Plugins/dbNSFP.pm'.format(settings.vep_cache_dir)):
            command = 'wget -O {}/Plugins/dbNSFP.pm https://github.com/Ensembl/VEP_plugins/raw/release/92/dbNSFP.pm'.format(settings.vep_cache_dir)
            call(command, shell=True)
            # test
            #     # os.system('perl variant_effect_predictor.pl -i example_GRCh37.vcf --cache --offline --dir_cache vep_cache --fasta vep_cache/homo_sapiens/77_GRCh37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa')

            # #download plugins
            # os.chdir(vep_cache_dir)
            # if not os.path.isdir('Plugins'):
            #     os.system('git clone %s Plugins' % (vep_plugins_source))

            # #install condel
            # os.chdir('Plugins/config/Condel/config')
            # condel_config = "condel.dir=\\'%s/Plugins/config/Condel\\'" % (vep_cache_dir)
            # os.system('echo %s >> condel_SP.conf' % (condel_config))

    def download_decipher(self):
        os.chdir(data_dir)
        if not os.path.exists('decipher'):
            os.makedirs('decipher')
        os.chdir('decipher')

        if not os.path.isfile(settings.hi_predictions_file):
            command = 'wget -c %s -O %s' % (settings.hi_predictions_source, settings.hi_predictions_file)
            call(command, shell=True)
            # extract
            command = 'gunzip -d %s' % (settings.hi_predictions_file)
            call(command, shell=True)

            file_without_extension = settings.hi_predictions_file.replace('.gz', '')
            # remove first line
            command = 'tail -n +2 "%s" > hi_predictions.unsorted.bed' % (file_without_extension)
            call(command, shell=True)

            command = 'sort -k 1,1 -k2,2n hi_predictions.unsorted.bed > hi_predictions.chr.bed'
            call(command, shell=True)

            # remove chr
            command = "cat hi_predictions.chr.bed | sed 's/^chr//' > hi_predictions.bed"
            call(command, shell=True)

            # compress
            command = 'bgzip hi_predictions.bed'
            call(command, shell=True)
            # rename
            command = 'mv hi_predictions.bed.gz %s' % (settings.hi_predictions_file)
            call(command, shell=True)

            command = 'tabix -p vcf %s' % (settings.hi_predictions_file)
            call(command, shell=True)

            command = 'rm hi_predictions.unsorted.bed %s hi_predictions.chr.bed' % (file_without_extension)
            call(command, shell=True)

        if not os.path.isfile(settings.population_cnv_file):
            command = 'wget -c %s -O %s' % (settings.population_cnv_source, settings.population_cnv_file)
            call(command, shell=True)

        if not os.path.isfile(settings.ddg2p_file):
            command = 'wget -c %s -O %s' % (settings.ddg2p_source, settings.ddg2p_file)
            call(command, shell=True)

    def download_ensembl(self):
        os.chdir(data_dir)
        # download hi_score
        if not os.path.exists('ensembl'):
            os.makedirs('ensembl')
        os.chdir('ensembl')
        if not os.path.isfile(settings.ensembl_phenotype_file):
            command = 'wget -c %s -O %s' % (settings.ensembl_phenotype_source, settings.ensembl_phenotype_file)
            call(command, shell=True)
            command = 'tabix -p vcf %s' % (settings.ensembl_phenotype_file)
            call(command, shell=True)

        if not os.path.isfile(settings.ensembl_clinically_file):
            command = 'wget -c %s -O %s' % (settings.ensembl_clinically_source, settings.ensembl_clinically_file)
            call(command, shell=True)
            command = 'tabix -p vcf %s' % (settings.ensembl_clinically_file)
            call(command, shell=True)

    def download_1000genomes(self):

        os.chdir(data_dir)
        # download 1000genomes
        if not os.path.exists('1000genomes'):
            os.makedirs('1000genomes')
        os.chdir('1000genomes')

        if not os.path.isfile(settings.genomes1k_file):
            command = 'wget -c %s' % (settings.genomes1k_source)
            call(command, shell=True)
            # why do you need to extract ? God only knows ... :P (snpsift merge ?)
            # command = 'gunzip -c %s > %s' % (settings.genomes1k_file, settings.genomes1k_vcf)
            # call(command, shell=True)

        if not os.path.isfile("%s.tbi" % (settings.genomes1k_file)):
            command = 'tabix -p vcf %s' % (settings.genomes1k_file)
            call(command, shell=True)

    def download_dbsnp(self):

        os.chdir(data_dir)

        if not os.path.exists('dbsnp'):
            os.makedirs('dbsnp')
        os.chdir('dbsnp')

        # download
        if not os.path.isfile(settings.dbsnp_file):
            command = 'wget -c %s' % (settings.dbsnp_source)
            call(command, shell=True)

        if not os.path.isfile("%s.tbi" % (settings.dbsnp_file)):
            command = 'wget -c %s.tbi' % (settings.dbsnp_source)
            call(command, shell=True)

        if not os.path.isfile(settings.clinvar_file):
            command = 'wget -c %s' % (settings.clinvar_source)
            call(command, shell=True)

        if not os.path.isfile("%s.tbi" % (settings.clinvar_file)):
            command = 'wget -c %s.tbi' % (settings.clinvar_source)
            call(command, shell=True)

    def download_esp(self):

        os.chdir(data_dir)

        if not os.path.exists('esp6500'):
            os.makedirs('esp6500')

        os.chdir('esp6500')

        if not os.path.isfile(settings.esp_final_file):
            command = 'wget -c %s' % (settings.esp_source)
            call(command, shell=True)

        chroms = list(range(1, 23)) + ['X', 'Y']
        # run prepare_data.sh
        if not os.path.isfile(settings.esp_final_file):
            command = 'tar -zxvf %s' % (settings.esp_file)
            call(command, shell=True)
            vcfs = []
            for chr in chroms:
                command = 'bgzip %s.chr%s.snps_indels.vcf' % (settings.esp_basename, chr)
                call(command, shell=True)
                command = 'tabix -p vcf %s.chr%s.snps_indels.vcf.gz' % (settings.esp_basename, chr)
                call(command, shell=True)
                vcfs.append('%s.chr%s.snps_indels.vcf.gz' % (settings.esp_basename, chr))
            command = 'vcf-concat %s | bgzip -c > esp6500si.vcf.gz' % (" ".join(vcfs))
            call(command, shell=True)
            command = 'tabix -p vcf esp6500si.vcf.gz'
            call(command, shell=True)
            command = 'rm %s* -f' % (settings.esp_basename)
            call(command, shell=True)

    def download_dbnsfp(self):
        os.chdir(data_dir)
        # download dbnsfp

        if not os.path.exists('dbnsfp'):
            os.makedirs('dbnsfp')
        os.chdir('dbnsfp')

        if not os.path.isfile(settings.dbnsfp_file):
            # --user=Anonymous --password=raonyguimaraes@gmail.com
            command = "wget -c %s -O dbNSFPv%s.zip" % (settings.dbnsfp_link, settings.dbnsfp_version)
            call(command, shell=True)

            # Uncompress
            command = 'unzip dbNSFPv%s.zip' % (settings.dbnsfp_version)
            call(command, shell=True)

            # deal with header
            command = """head -n 1 dbNSFP*_variant.chr1 > header.txt """
            call(command, shell=True)

            command = """cat dbNSFP*_variant.chr* | grep -v "^#" > dbNSFP%s.unordered.txt""" % (settings.dbnsfp_version)

            call(command, shell=True)
            # die()

            #use sort -k1,1V -k2,2n for hg38 
            command = """
            mkdir tmp
            sort -k8,8V -k9,9n dbNSFP*.unordered.txt -T tmp/ > dbNSFP%s.ordered.txt
            cat header.txt > dbNSFP%s.txt
            cat dbNSFP*.ordered.txt >> dbNSFP%s.txt
            """ % (settings.dbnsfp_version, settings.dbnsfp_version, settings.dbnsfp_version)
            call(command, shell=True)

            # Compress using block-gzip algorithm

            command = 'bgzip dbNSFP%s.txt' % (settings.dbnsfp_version)
            call(command, shell=True)

            # Create tabix index
            # http://genome.sph.umich.edu/wiki/RareMETALS
            # NOTE: Tabix 1.X does not seem to support the indexing for generic tab-delimited files. To index the file, please use tabix 0.2.5 or earlier versions.
            # use tabix -s 1 -b 2 -e 2 for hg38 and 
            command = 'tabix -s 8 -b 9 -e 9 dbNSFP%s.txt.gz' % (settings.dbnsfp_version)
            call(command, shell=True)

            # clean files
            command = "rm -rf tmp dbNSFP*_variant* dbNSFP*_gene* *ordered.txt *.class *.in *.txt LICENSE.txt try.vcf search_dbNSFP* *.zip"
            # call(command, shell=True)

            # keep original file dbNSFPv3.2a.zip
            # call(command, shell=True)

        if not os.path.isfile(settings.dbscsnv_file):
            command = 'wget %s' % (settings.dbscsnv_source)
            call(command, shell=True)
            command = 'unzip dbscSNV%s.zip' % (settings.dbscsnv_version)
            call(command, shell=True)
            command = 'head -n1 dbscSNV%s.chr1 > h' % (settings.dbscsnv_version)
            call(command, shell=True)
            command = 'cat dbscSNV%s.chr* | grep -v ^chr | cat h - | bgzip -c > dbscSNV%s.txt.gz' % (
                settings.dbscsnv_version, settings.dbscsnv_version)
            call(command, shell=True)
            command = 'tabix -s 1 -b 2 -e 2 -c c dbscSNV%s.txt.gz' % (settings.dbscsnv_version)
            call(command, shell=True)

            command = "rm dbscSNV1.1.zip h *chr*"
            call(command, shell=True)
