from .install import Installer

from .helpers.validator import Validator 

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

    def build_datasets(self):
        installer = Installer()
        # installer.build_datasets()

    def annotate(self, vcf_file):
        print("Annotating VCF... %s" % (vcf_file))


    def validate(self, vcf_file):

        print("Validating VCF... %s" % (vcf_file))

    # def withdraw(self, amount):
    #     """Return the balance remaining after withdrawing *amount*
    #     dollars."""
    #     if amount > self.balance:
    #         raise RuntimeError('Amount greater than available balance.')
    #     self.balance -= amount
    #     return self.balance
    #
    # def deposit(self, amount):
    #     """Return the balance remaining after depositing *amount*
    #     dollars."""
    #     self.balance += amount
    #     return self.balance
