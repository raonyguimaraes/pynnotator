#!/usr/bin/python

import os
import subprocess
from subprocess import call

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

    def install_data(self):
        self.install_requirements()
        self.install_libs()

    def install_requirements(self):
        """Install Ubuntu Requirements"""
        print('Installing Requirements')
        print(subprocess.check_output(['lsb_release', '-si']).decode().strip())

        distro_id = subprocess.check_output(['lsb_release', '-si']).decode().strip().lower()

        if distro_id in ['ubuntu', 'linuxmint', 'debian']:
            pkgs = 'gcc git python3-dev python3-pip zlib1g-dev make libssl-dev libbz2-dev liblzma-dev libcurl4-openssl-dev bcftools tabix curl wget unzip'
            call('sudo apt-get update', shell=True)
            call('sudo apt-get install -y %s' % pkgs, shell=True)
        elif distro_id in ['redhat', 'centos']:
            pkgs = 'gcc git python3-devel python3-pip zlib-devel make openssl-devel bzip2-devel xz-devel libcurl-devel bcftools tabix curl wget unzip'
            call('sudo yum install -y %s' % pkgs, shell=True)

    def install_libs(self):
        if not os.path.exists(libs_dir):
            os.makedirs(libs_dir)
        os.chdir(libs_dir)

        if not os.path.exists('vep'):
            self.install_vep()

        os.chdir(settings.BASE_DIR)

    def install_vep(self):
        os.makedirs('vep')
        os.chdir('vep')

        vep_zip = 'release-%s.zip' % settings.vep_release
        if not os.path.exists(vep_zip):
            call('wget %s -O %s' % (settings.vep_source, vep_zip), shell=True)
            call('unzip %s' % vep_zip, shell=True)

        vep_src = os.path.join(os.getcwd(), 'src')
        if not os.path.exists(vep_src):
            os.makedirs(vep_src)
            extracted = [d for d in os.listdir('.') if d.startswith('ensembl-vep')][0]
            os.rename(extracted, os.path.join(vep_src, extracted))

        vep_script_dir = os.path.join(vep_src, 'ensembl-vep-release-%s' % settings.vep_release)
        if os.path.exists(vep_script_dir):
            call('perl %s/INSTALL.pl --NO_TEST' % vep_script_dir, shell=True)

    def build_datasets(self):
        print('Building Datasets')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        os.chdir(data_dir)
        self.download_vep_data()

    def download_vep_data(self):
        if not os.path.exists(settings.vep_cache_dir):
            os.makedirs(settings.vep_cache_dir)

        cache_url = 'https://ftp.ensembl.org/pub/release-%s/variation/indexed_vep_cache/homo_sapiens_vep_%s_%s.tar.gz' % (
            settings.vep_release, settings.vep_release,
            'GRCh38' if settings.BUILD == 'hg38' else 'GRCh37'
        )
        cache_file = 'homo_sapiens_vep_cache.tar.gz'
        if not os.path.exists(os.path.join(settings.vep_cache_dir, 'homo_sapiens')):
            call('wget %s -O %s' % (cache_url, cache_file), shell=True)
            call('tar -xzf %s -C %s' % (cache_file, settings.vep_cache_dir), shell=True)
            os.remove(cache_file)
