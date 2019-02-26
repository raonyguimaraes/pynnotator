#Gemini wrapper
import argparse
from subprocess import run
from pynnotator import settings
import os

class GnomAD:
    def __init__(self, vcf, cores):
        self.data = []

    def install():
        print('Install gnomAD')

        os.chdir(settings.data_dir)

        
        if not os.path.exists('gnomad'):
            os.makedirs('gnomad')
        os.chdir('gnomad')

        filepath = 'gnomad.genomes.r2.1.sites.vcf.bgz'
        if not os.path.isfile(filepath):
            command = 'wget -c https://storage.googleapis.com/gnomad-public/release/2.1/vcf/genomes/{}'.format(filepath)
            run(command, shell=True)
        filepath = 'gnomad.genomes.r2.1.sites.vcf.bgz.tbi'
        if not os.path.isfile(filepath):
            command = 'wget -c https://storage.googleapis.com/gnomad-public/release/2.1/vcf/genomes/{}'.format(filepath)
            run(command, shell=True)
        
        filepath = 'gnomad.exomes.r2.1.sites.vcf.bgz'
        if not os.path.isfile(filepath):
            command = 'wget -c https://storage.googleapis.com/gnomad-public/release/2.1/vcf/exomes/{}'.format(filepath)
            run(command, shell=True)
        filepath = 'gnomad.exomes.r2.1.sites.vcf.bgz.tbi'
        if not os.path.isfile(filepath):
            command = 'wget -c https://storage.googleapis.com/gnomad-public/release/2.1/vcf/exomes/{}'.format(filepath)
            run(command, shell=True)

    def main(self):
        #command = '
        print('Annotate GnomAD')
        command = ''



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Annotate a VCF File with GnomAD.')

    parser.add_argument('options', help='install test', nargs='?')
    parser.add_argument('-i', dest='vcf_file', required=False, metavar='example.vcf', help='a VCF file to be annotated')
    parser.add_argument('-n', dest='cores', required=False, metavar='4', help='number of cores to use')

    args = parser.parse_args()
    gnomead = GnomAD(args.vcf_file, args.cores)
    if args.options == 'install':
        gnomead.install()
    else:
        gnomead.main()
