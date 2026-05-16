import os
import subprocess
from subprocess import call

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

    def install_requirements(self):
        print('Installing Dependencies...')
        installer = Installer()
        installer.install_requirements()

    def annotate(self, args):
        print("Annotating VCF... %s %s" % (args.build, args.vcf_file))
        pynnotator = Annotator(args)
        pynnotator.run()

    def test(self, args):
        path = '%s/tests' % (os.path.dirname(__file__))
        args.vcf_file = 'sample.70.vcf.gz'
        args.build = 'hg19'
        print('Testing Annotation... ', args.build, args.vcf_file)

        os.chdir(path)
        pynnotator = Annotator(args)
        pynnotator.run()
        os.chdir(path)

        args.vcf_file = 'sample.70.hg38.vcf.gz'
        args.build = 'hg38'
        print('Testing Annotation... ', args.build, args.vcf_file)
        pynnotator = Annotator(args)
        pynnotator.run()
        os.chdir(path)

        # Clean up
        call('rm -rf ann_sample.10*', shell=True)
