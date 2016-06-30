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
