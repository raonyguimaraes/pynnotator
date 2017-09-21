#Gemini wrapper
import argparse
from subprocess import run
from pynnotator import settings
import os

class Gemini:
    def __init__(self, vcf, cores):
        self.data = []

    def install(self):
        print('Install GEMINI')
        os.chdir('{}/gemini/'.format(settings.libs_dir))
        command = 'wget https://raw.github.com/arq5x/gemini/master/gemini/scripts/gemini_install.py'
        run(command, shell=True)
        if not os.path.exists('gemini'):
            os.makedirs('gemini')
        if not os.path.exists('local'):
            os.makedirs('local')
        command = 'python gemini_install.py local gemini'
        run(command, shell=True)
        command = 'gemini update --dataonly --extra cadd_score'
        run(command, shell=True)
        command = 'gemini update --dataonly --extra gerp_bp'
        run(command, shell=True)
                

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Annotate a VCF File with GEMINI.')

    parser.add_argument('options', help='install test', nargs='?')
    parser.add_argument('-i', dest='vcf_file', required=False, metavar='example.vcf', help='a VCF file to be annotated')
    parser.add_argument('-n', dest='cores', required=False, metavar='4', help='number of cores to use')

    args = parser.parse_args()
    gemini = Gemini(args.vcf_file, args.cores)
    if args.options == 'install':
        gemini.install()
    else:
        gemini.run()