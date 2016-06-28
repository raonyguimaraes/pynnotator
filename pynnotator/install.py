#!/usr/bin/python2

import os
import subprocess
from subprocess import call
import platform

# base_dir = os.path.dirname(os.path.realpath(__file__))
# scripts_dir = base_dir+'/scripts'
# libdir = base_dir+'/libs'
# datadir = base_dir+'/data'
# import sys
# sys.path.insert(0, scripts_dir)
#
# from settings import *

import sys

BASE_DIR = os.path.dirname(__file__)


class Installer(object):
    """A class to annotate VCFs

    Attributes:
        vcf_file: a VCF file to be annotated
    """

    def __init__(self):
        """Return a Pynnotator Installer object """

        # self.install_requirements()

        libs_dir = os.path.join(BASE_DIR, 'libs')
        if not os.path.isdir(libs_dir):
            os.system('mkdir %s' % (libs_dir))

        # self.install_libs()

        # self.download_data()
        # self.download_data()

    def install_requirements(self):
        """Install Ubuntu Requirements"""
        print('Install Ubuntu requirements')
        if platform.dist()[0] in ['Ubuntu', 'LinuxMint']:
            command = 'sudo apt-get install python3-dev python3-pip python3-setuptools vcftools samtools tabix zlib1g-dev libpq-dev build-essential zlib1g-dev liblocal-lib-perl cpanminus curl unzip'  # lamp-server^
            sts = call(command, shell=True)

            try:
                subprocess.call(['java', '-version'])
            except:
                os.system('''
    	               sudo apt install software-properties-common
    	               sudo add-apt-repository ppa:webupd8team/java
    	               sudo apt-get update
    	               sudo apt-get install oracle-java8-installer
    	               ''')


            # requirements for perl
            os.system(
                '''sudo cpanm DBI File::Copy::Recursive Archive::Extract Archive::Zip LWP::Simple Bio::Root::Version LWP::Protocol::https Bio::DB::Fasta''')


    def build_datasets(self):
        print("Building Datasets")


def install():

    #install dependencies
    requirements()

    # create folders
    if not os.path.isdir('libs'):
        os.system('mkdir libs')
    if not os.path.isdir('data'):
        os.system('mkdir data')

    os.chdir('libs')

    # install_java()
    install_tabix()
    install_vcftools()
    install_snpeff()

    install_vep()


    die()


    os.chdir(base_dir)

    # #download data

    os.chdir('data')

    # download_1000genomes()

    # download_dbsnp()

    # download_esp()

    download_dbnsfp()

def requirements():

    print('installing dependencies...')
    if platform.dist()[0] in ['Ubuntu', 'LinuxMint']:

        # os.system('sudo apt-get install python-dev python-pip vcftools samtools tabix zlib1g-dev libpq-dev build-essential zlib1g-dev libmemcached-dev tasksel postgresql liblocal-lib-perl cpanminus curl lamp-server^')
        command = 'sudo apt-get install python3-dev python3-pip python3-setuptools vcftools samtools tabix zlib1g-dev libpq-dev build-essential zlib1g-dev libmemcached-dev tasksel postgresql liblocal-lib-perl cpanminus curl unzip vim screen less git htop' #lamp-server^
        sts = call(command, shell=True)

        try:
            subprocess.call(['java', '-version'])
        except:
            os.system('''
               sudo apt install software-properties-common
               sudo add-apt-repository ppa:webupd8team/java
               sudo apt-get update
               sudo apt-get install oracle-java8-installer
               ''')


        # requirements for perl
        os.system('''sudo cpanm DBI File::Copy::Recursive Archive::Extract Archive::Zip LWP::Simple Bio::Root::Version LWP::Protocol::https Bio::DB::Fasta''')

    #install java
    os.system('pip install virtualenvwrapper cython')
    os.system('pip install -r requirements.txt')


def install_java():
    if not os.path.isdir('java'):
        os.system('mkdir java')
    os.chdir('java')

    #check if file exists
    # if not os.path.isfile(java_file):
    #     os.system('wget -c %s -O %s' % (java_source, java_file))
    #     os.system('tar -zxvf %s' % (java_file))
    # os.chdir(libdir)

def install_tabix():
    if not os.path.isdir('tabix'):
        os.system('mkdir tabix')
    os.chdir('tabix')
    #check if file exists
    if not os.path.isfile(tabix_file):
        os.system('wget -c %s -O %s' % (tabix_source, tabix_file))
        os.system('unzip %s' % (tabix_file))
        os.system('cd %s; make' % (tabix_path))

    os.chdir(libdir)

def install_vcftools():
    if not os.path.isdir('vcftools'):
        os.system('mkdir vcftools')
    os.chdir('vcftools')
    #check if file exists
    if not os.path.isfile(vcftools_file):
        os.system('wget -c %s' % (vcftools_source))
        os.system('tar -zxvf %s' % (vcftools_file))
        os.chdir(vcftools_basename)
        os.system('make')
    os.chdir(libdir)

def install_snpeff():
    if not os.path.isdir('snpeff'):
        os.system('mkdir snpeff')
    os.chdir('snpeff')
    #check if file exists
    if not os.path.isfile('%s.zip' % (snpeff_version)):
        os.system('wget -c %s' % (snpeff_source))
        os.system('unzip %s.zip' % (snpeff_version))

    os.chdir('snpEff')

    #download data
    if not os.path.isdir('data/%s' % (snpeff_database)):
        os.system('java -jar snpEff.jar download -c snpEff.config -v %s' % (snpeff_database))

    os.chdir(libdir)


def install_vep():

    if not os.path.isdir('vep'):
        os.system('mkdir vep')
    os.chdir('vep')

    #download
    if not os.path.isfile('%s.zip' % (vep_release)):
        os.system('wget %s -O %s.zip' % (vep_source, vep_release))
        os.system('unzip %s.zip' % (vep_release))

    os.chdir('ensembl-tools-release-%s/scripts/variant_effect_predictor' % (vep_release))

    #install cache
    vep_cache_dir = '%s/vep_cache' % (data_dir)
    if not os.path.isdir(vep_cache_dir):
        os.system('mkdir %s' % (vep_cache_dir))
        os.system('perl INSTALL.pl -a acf -s homo_sapiens -c %s --ASSEMBLY GRCh37' % (vep_cache_dir))

        # os.system('perl variant_effect_predictor.pl -i example_GRCh37.vcf --cache --offline --dir_cache vep_cache --fasta vep_cache/homo_sapiens/77_GRCh37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa')

    #download plugins
    os.chdir(vep_cache_dir)
    if not os.path.isdir('Plugins'):
        os.system('git clone %s Plugins' % (vep_plugins_source))

    #install condel
    os.chdir('Plugins/config/Condel/config')
    condel_config = "condel.dir=\\'%s/Plugins/config/Condel\\'" % (vep_cache_dir)
    os.system('echo %s >> condel_SP.conf' % (condel_config))

    os.chdir(libdir)


def download_1000genomes():

    os.chdir(datadir)
    # download 1000genomes

    if not os.path.isdir('1000genomes'):
        os.system('mkdir 1000genomes')

    os.chdir('1000genomes')

    if not os.path.isfile(genomes1k_file):
        command = 'wget -c %s' % (genomes1k_source)
        os.system(command)
        #why do you need to extract ?
        command = 'gunzip -c %s > %s' % (genomes1k_file, genomes1k_vcf)
        os.system(command)
    # command = '%s/tabix -p vcf %s' % (tabix_path, genomes1k_vcf)


    if not os.path.isfile("%s.tbi" % (genomes1k_file)):
        command = 'tabix -p vcf %s' % (genomes1k_file)
        os.system(command)


def download_dbsnp():

    os.chdir(datadir)

    #download dbsnp
    if not os.path.isdir('dbsnp'):
        os.system('mkdir dbsnp')

    os.chdir('dbsnp')
    #download
    if not os.path.isfile(dbsnp_file):
        command = 'wget -c %s' % (dbsnp_source)
        os.system(command)
        #extract and zip with bgzip
        command = 'gunzip -d %s' % (dbsnp_file)
        os.system(command)
        command = 'bgzip %s' % (dbsnp_file)
        os.system(command)

    if not os.path.isfile("%s.tbi" % (dbsnp_file)):
        command = 'tabix -p vcf %s' % (dbsnp_file)
        os.system(command)

    if not os.path.isfile(clinvar_file):
        command = 'wget -c %s' % (clinvar_source)
        os.system(command)

    if not os.path.isfile("%s.tbi" % (clinvar_file)):
        command = 'tabix -p vcf %s' % (clinvar_file)
        os.system(command)



def download_esp():

    os.chdir(datadir)

    if not os.path.isdir('esp6500'):
        os.system('mkdir esp6500')

    os.chdir('esp6500')

    if not os.path.isfile(esp_file):
        command = 'wget -c %s' % (esp_source)
        os.system(command)

    chroms = list(range(1,23))+['X', 'Y']
    #run prepare_data.sh
    if not os.path.isfile('esp6500si.vcf.gz'):
        command = 'tar -zxvf %s' % (esp_file)
        os.system(command)
        vcfs = []
        for chr in chroms:
            command = 'bgzip %s.chr%s.snps_indels.vcf' % (esp_basename, chr)
            os.system(command)
            command = 'tabix -p vcf %s.chr%s.snps_indels.vcf.gz' % (esp_basename, chr)
            os.system(command)
            vcfs.append('%s.chr%s.snps_indels.vcf.gz' % (esp_basename, chr))
        command  = 'vcf-concat %s | bgzip -c > esp6500si.vcf.gz' % (" ".join(vcfs))
        os.system(command)
        command  = 'tabix -p vcf esp6500si.vcf.gz'
        os.system(command)
        command = 'rm %s* -f' % (esp_basename)
        os.system(command)



def download_dbnsfp():
    os.chdir(datadir)
    #download esp6500

    if not os.path.isdir('dbnsfp'):
        os.system('mkdir dbnsfp')


    os.chdir('dbnsfp')

    # if not os.path.isfile(dbnsfp):

        #--user=Anonymous --password=raonyguimaraes@gmail.com
        # command = "wget -c %s -O dbNSFPv%s.zip" % (dbnsfp_link, dbnsfp_version)
        # os.system(command)

        # # Uncompress
        # os.system('unzip dbNSFPv%s.zip' % (dbnsfp_version))

        # # Create a single file version
        # os.system('(head -n 1 dbNSFP%s_variant.chr1 ;\
        # cat dbNSFP%s_variant.chr* | grep -v "^#" ) > dbNSFP%s.txt \
        # ' % (dbnsfp_version, dbnsfp_version, dbnsfp_version))


        # os.system('head -n 1 dbNSFP%s_variant.chr1 > dbNSFP%s.txt' % (dbnsfp_version, dbnsfp_version))
        # os.system('tail -n +2 dbNSFP%s_variant.chr* >> dbNSFP%s.txt' % (dbnsfp_version, dbnsfp_version))
        #awk '{if(NR>1)print}'
        #head -n 1 dbNSFP3.2a_variant.chr1 > dbNSFP3.2a.txt


        # # Compress using block-gzip algorithm
        #
        # os.system('bgzip dbNSFP%s.txt' % (dbnsfp_version))

        # # Create tabix index
        #http://genome.sph.umich.edu/wiki/RareMETALS
        #NOTE: Tabix 1.X does not seem to support the indexing for generic tab-delimited files. To index the file, please use tabix 0.2.5 or earlier versions.


        # os.system('tabix -f -s 1 -b 2 -e 2 dbNSFP%s.txt.gz' % (dbnsfp_version))


        #for f in dbNSFP3.2a_variant.chr*; do
        #   cat $f | awk '{if(NR>1)print}' >> dbNSFP3.2a.txt
        # done
        # root@4f5e8725433d:~/annotator/data/dbnsfp# bgzip -c dbNSFP3.2a.txt > dbNSFP3.2a.txt.gz
        # root@4f5e8725433d:~/annotator/data/dbnsfp# tabix -f -s 1 -b 2 -e 2 dbNSFP3.2a.txt.gz


        #
        # command = 'cd ..'
        # os.system(command)

    if not os.path.isfile(dbscsnv):
        command = 'wget ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbscSNV1.1.zip'
        os.system(command)
        command = 'unzip dbscSNV1.1.zip'
        os.system(command)
        command = 'head -n1 dbscSNV1.1.chr1 > h'
        os.system(command)
        command = 'cat dbscSNV1.1.chr* | grep -v ^chr | cat h - | bgzip -c > dbscSNV1.1.txt.gz'
        os.system(command)
        command = 'tabix -s 1 -b 2 -e 2 -c c dbscSNV1.1.txt.gz'
        os.system(command)

# install()
