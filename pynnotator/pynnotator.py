import os
from subprocess import call, check_output, check_call
import subprocess

from .install import Installer
from .annotator import Annotator


class Pynnotator(object):
    """A class to annotate VCFs

    Attributes:
        vcf_file: a VCF file to be annotated
    """

    def __init__(self, vcf_file=False):
        """Return a Pynnotator object with a defined VCF file to be annotated."""
        self.vcf_file= vcf_file

    def install(self):
        print('Starting Installation...')
        installer = Installer()
        installer.install()
        
        print("Installation Finished with success!! \nNow try testing with the command: pynnotator test")
        
    def install_libs(self):
        print('Installing Libs...')
        installer = Installer()
        installer.install_libs()
    def install_requirements(self):
        print('Installing Libs...')
        installer = Installer()
        installer.install_requirements()
    def build(self):
        print('Building Databasets...')
        installer = Installer()
        installer.build_datasets()
    def annotate(self, vcf_file):
        print("Annotating VCF... %s" % (vcf_file))
        pynnotator = Annotator(vcf_file)
        pynnotator.run()

    def test(self):
        print('Testing Annotation...')
        path = '%s/tests' % (os.path.dirname(__file__))
        vcf_file = 'sample.1000.vcf'
        os.chdir(path)
        pynnotator = Annotator(vcf_file)
        pynnotator.run()
        os.chdir(path)

        command = 'grep -v "^#" ann_sample.1000/annotation.final.vcf > result.vcf'
        call(command, shell=True)

        # compare result with reference
        try:
            command = "zdiff annotation.vcf.gz result.vcf"
            diff_1 = check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            diff_1 = '1'

        try:    
            command = "zdiff annotation.v2.vcf.gz result.vcf"
            diff_2 = check_output(command, shell=True)#check_output
        except subprocess.CalledProcessError as e:
            diff_2 = '1'

        # print(diff_1, diff_2)
        if diff_1 == b'' or diff_2 == b'':
            print('Congratulations, The Python Annotation Framework is working as expected, Happy Annotation!!!')
 

        command = 'rm -rf ann_sample.1000 result.vcf'
        call(command, shell=True)