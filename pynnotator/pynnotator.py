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
        #compare result with reference
        try:
            command = "diff annotation.final.vcf ann_sample.1000/annotation.final.vcf"
            diff_1 = check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            diff_1 = '1'
        try:    
            command = "diff annotation.final.v2.vcf ann_sample.1000/annotation.final.vcf"
            diff_2 = check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            diff_2 = '1'            
        # print(diff_1, diff_2)
        if diff_1 == b'' or diff_2 == b'':
            print('Congratulations, The Annotation Framework is working as expected, Happy Annotation!!!') 
        # print(std)
        command = 'rm -rf ann_sample.1000'
        call(command, shell=True)