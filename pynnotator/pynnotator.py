import os
import subprocess
from subprocess import call, check_output

from .annotator import Annotator
from .install import Installer


class Pynnotator(object):
    """A class to annotate VCFs

    Attributes:
        vcf_file: a VCF file to be annotated
    """

    def __init__(self, args=False):
        """Return a Pynnotator object with a defined VCF file to be annotated."""
        self.args = args

    def install(self):
        print('Starting Installation...')
        installer = Installer()
        installer.install()

        print("Installation Finished with success!! \nNow try testing with the command: pynnotator test")

    def build(self):
        print('Building Databasets...')
        installer = Installer()
        installer.build_datasets()

    def install_libs(self):
        print('Installing Libs...')
        installer = Installer()
        installer.install_libs()

    def install_requirements(self):
        print('Installing Libs...')
        installer = Installer()
        installer.install_requirements()

    def annotate(self, args):
        print("Annotating VCF... %s %s" % (args.build, args.vcf_file))
        pynnotator = Annotator(args)
        pynnotator.run()

    def test(self,args):
        print('Testing Annotation...')
        path = '%s/tests' % (os.path.dirname(__file__))
        args.vcf_file = 'sample.70.vcf.gz'
        args.build = 'hg19'

        os.chdir(path)
        pynnotator = Annotator(args)
        pynnotator.run()
        os.chdir(path)

        # args.vcf_file = 'sample.100.hg38.vcf.gz'
        # args.build = 'hg38'
        # pynnotator = Annotator(args)
        # pynnotator.run()
        # os.chdir(path)


        # command = 'grep -v "^#" ann_sample.1000/annotation.final.vcf > result.vcf'
        # call(command, shell=True)

        # compare result with reference
        # try:
        #     command = "zdiff annotation.validated.vcf.gz ann_sample.1000/annotation.final.vcf"
        #     diff = check_output(command, shell=True)
        # except subprocess.CalledProcessError as e:
        #     diff = '1'

        # if diff == b'':
        #     print('Congratulations, The Python Annotation Framework is working as expected, Happy Annotation!!!\n\n')

        #delete files after test
        command = 'rm -rf ann_sample.10*'
        call(command, shell=True)
