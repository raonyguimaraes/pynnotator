#!/usr/bin/python2

import os
import subprocess
from subprocess import call
import platform

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
        self.install_libs()
        self.download_data()
        self.build_datasets()
        

    def install_requirements(self):
        """Install Ubuntu Requirements"""
        print('Installing Ubuntu requirements')
        if platform.dist()[0] in ['Ubuntu', 'LinuxMint']:
            command = 'sudo apt-get install python3-dev python3-pip python3-setuptools vcftools samtools tabix zlib1g-dev libpq-dev build-essential zlib1g-dev liblocal-lib-perl cpanminus curl unzip wget'  # lamp-server^
            sts = call(command, shell=True)

            try:
                subprocess.call(['java', '-version'])
            except:

                command = """sudo apt install software-properties-common
                       sudo add-apt-repository -y ppa:webupd8team/java
                       sudo apt-get update
                       echo "oracle-java8-installer shared/accepted-oracle-license-v1-1 select true" | sudo debconf-set-selections
                       sudo apt-get -y install oracle-java8-installer"""

                sts = call(command, shell=True)

            # Perl Requirements
            command = "sudo cpanm DBI File::Copy::Recursive Archive::Extract Archive::Zip LWP::Simple Bio::Root::Version LWP::Protocol::https Bio::DB::Fasta CGI"
            sts = call(command, shell=True)


    def install_libs(self):
        
        if not os.path.exists(libs_dir):
            os.makedirs(libs_dir)
        os.chdir(libs_dir)
        
        # self.install_java()

        self.install_htslib()
        self.install_vcftools()
        self.install_snpeff()
        self.install_vep()


    def build_datasets(self):
        print("Building Datasets")

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        os.chdir(data_dir)

        self.download_snpeff_data()
        self.download_vep_data()

        self.download_hi_score()
        self.download_ensembl()        
        self.download_1000genomes()
        self.download_dbsnp()
        self.download_esp()
        self.download_dbnsfp()

    def download_data(self):
        print("Downloading Data")

        os.chdir(settings.BASE_DIR)

        if not os.path.exists(settings.data_dir):
            command = "wget %s -O %s" %(settings.data_source, settings.data_file)
            call(command, shell=True)

            print("Extracting Data...")
            command = "tar -zxvf %s" % (settings.data_file)
            call(command, shell=True)


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
        #check if file exists
        if not os.path.isfile(settings.htslib_file):
            command = """
            wget -c %s 
            tar -jxvf %s
            cd %s; ./configure; make
            """ % (settings.htslib_source, settings.htslib_file, settings.htslib_version)

            call(command, shell=True)

        os.chdir(libs_dir)


    def install_vcftools(self):
        if not os.path.isdir('vcftools'):
            call('mkdir vcftools', shell=True)
        os.chdir('vcftools')
        #check if file exists
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
        #check if file exists
        if not os.path.isfile('%s.zip' % (settings.snpeff_version)):
            command = """
            wget -c %s
            unzip %s.zip
            """ % (settings.snpeff_source, settings.snpeff_version)
            call(command, shell=True)

            #change data_dir
            #from ./data/ to data.dir = ../../../data/snpeff_data
            command = """
            sed -i 's/\.\/data\//\.\.\/\.\.\/\.\.\/data\/snpeff_data/g' snpEff/snpEff.config"""
            call(command, shell=True)

        os.chdir(libs_dir)

    def install_vep(self):

        if not os.path.isdir('vep'):
            call('mkdir vep', shell=True)
        os.chdir('vep')

        if not os.path.isfile('%s.zip' % (settings.vep_release)):
            command = """
            wget %s -O %s.zip
            unzip %s.zip
            """ % (settings.vep_source, settings.vep_release, settings.vep_release)
            call(command, shell=True)

        os.chdir(settings.vep_dir)
        # download vep cache
        command = """perl INSTALL.pl -a a"""
        call(command, shell=True)


        os.chdir(libs_dir)
        

    def download_snpeff_data(self):

        #download snpeff data
        if not os.path.isdir(os.path.join(settings.snpeff_data_dir, settings.snpeff_database)):
            command = "java -jar %s/snpEff.jar download -c %s/snpEff.config -v %s" % (settings.snpeff_dir, settings.snpeff_dir, settings.snpeff_database)
            call(command, shell=True)

    def download_vep_data(self):

        os.chdir(settings.vep_dir)
        # download vep cache
        if not os.path.isdir(settings.vep_cache_dir):
            command = """perl INSTALL.pl -a acf -s homo_sapiens -c %s --ASSEMBLY GRCh37
            """ % (settings.vep_cache_dir)
            call(command, shell=True)

        #test
        #     # os.system('perl variant_effect_predictor.pl -i example_GRCh37.vcf --cache --offline --dir_cache vep_cache --fasta vep_cache/homo_sapiens/77_GRCh37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa')

        # #download plugins
        # os.chdir(vep_cache_dir)
        # if not os.path.isdir('Plugins'):
        #     os.system('git clone %s Plugins' % (vep_plugins_source))

        # #install condel
        # os.chdir('Plugins/config/Condel/config')
        # condel_config = "condel.dir=\\'%s/Plugins/config/Condel\\'" % (vep_cache_dir)
        # os.system('echo %s >> condel_SP.conf' % (condel_config))

    def download_hi_score(self):
        os.chdir(data_dir)
        # download hi_score
        if not os.path.exists('hi_score'):
            os.makedirs('hi_score')
        os.chdir('hi_score')
        if not os.path.isfile(settings.hi_score_file):
            command = 'wget -c %s -O %s' % (settings.hi_score_source, settings.hi_score_file)
            call(command, shell=True)
            command = 'tabix -p vcf %s' % (settings.hi_score_file)
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
            #why do you need to extract ? God only knows ... :P (snpsift merge ?)
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
        
        #download
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

        chroms = list(range(1,23))+['X', 'Y']
        #run prepare_data.sh
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
            command  = 'vcf-concat %s | bgzip -c > esp6500si.vcf.gz' % (" ".join(vcfs))
            call(command, shell=True)
            command  = 'tabix -p vcf esp6500si.vcf.gz'
            call(command, shell=True)
            command = 'rm %s* -f' % (settings.esp_basename)
            call(command, shell=True)


    def download_dbnsfp(self):
        os.chdir(data_dir)
        #download dbnsfp

        if not os.path.exists('dbnsfp'):
            os.makedirs('dbnsfp')
        os.chdir('dbnsfp')

        if not os.path.isfile(settings.dbnsfp_file):

            # --user=Anonymous --password=raonyguimaraes@gmail.com
            command = "wget -c %s -O dbNSFPv%s.zip" % (settings.dbnsfp_link, settings.dbnsfp_version)
            # call(command, shell=True)


            # Uncompress
            command = 'unzip dbNSFPv%s.zip' % (settings.dbnsfp_version)
            call(command, shell=True)

            #deal with header
            command = """head -n 1 dbNSFP%s_variant.chr1 > header.txt """ % (settings.dbnsfp_version)
            call(command, shell=True)

            command = """cat dbNSFP%s_variant.chr* | grep -v "^#" > dbNSFP%s.unordered.txt""" % (settings.dbnsfp_version, settings.dbnsfp_version)
            call(command, shell=True)

            command = """
            sort -k1,1V -k2,2n dbNSFP%s.unordered.txt > dbNSFP%s.ordered.txt
            cat header.txt > dbNSFP%s.txt
            cat dbNSFP%s.ordered.txt >> dbNSFP%s.txt
            """ % (settings.dbnsfp_version, settings.dbnsfp_version, settings.dbnsfp_version, settings.dbnsfp_version, settings.dbnsfp_version)

            call(command, shell=True)
            
            # Compress using block-gzip algorithm
            
            command = 'bgzip dbNSFP%s.txt' % (settings.dbnsfp_version)
            call(command, shell=True)
            
            # Create tabix index
            # http://genome.sph.umich.edu/wiki/RareMETALS
            # NOTE: Tabix 1.X does not seem to support the indexing for generic tab-delimited files. To index the file, please use tabix 0.2.5 or earlier versions.

            command = 'tabix -f -s 1 -b 2 -e 2 dbNSFP%s.txt.gz' % (settings.dbnsfp_version)
            call(command, shell=True)

            #clean files
            command = "rm dbNSFP*_variant* dbNSFP*_gene* *ordered.txt *.class *.in header.txt LICENSE.txt try.vcf search_dbNSFP32a.java search_dbNSFP32a.readme.pdf "
            call(command, shell=True)

            #keep original file dbNSFPv3.2a.zip
            # call(command, shell=True)

        if not os.path.isfile(settings.dbscsnv_file):
            command = 'wget %s' % (settings.dbscsnv_source)
            call(command, shell=True)
            command = 'unzip dbscSNV%s.zip' % (settings.dbscsnv_version)
            call(command, shell=True)
            command = 'head -n1 dbscSNV%s.chr1 > h' % (settings.dbscsnv_version)
            call(command, shell=True)
            command = 'cat dbscSNV%s.chr* | grep -v ^chr | cat h - | bgzip -c > dbscSNV%s.txt.gz' % (settings.dbscsnv_version, settings.dbscsnv_version)
            call(command, shell=True)
            command = 'tabix -s 1 -b 2 -e 2 -c c dbscSNV%s.txt.gz' % (settings.dbscsnv_version)
            call(command, shell=True)

            command = "rm dbscSNV1.1.zip h *chr*"
            call(command, shell=True)
