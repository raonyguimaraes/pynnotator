import argparse
import logging
import os
import subprocess
from subprocess import check_output

import common

logging.basicConfig(filename='vt.log', level=logging.DEBUG)


class VT():

    def __init__(self, args):
        if args.install:
            self.install()
        self.vt = '{}/vt'.format(common.libs_dir)

    def install(self):
        # change to libs dir

        os.chdir(common.libs_dir)

        if not os.path.exists('vt'):
            command = 'git clone https://github.com/atks/vt'
            output = check_output(command, shell=True)

            logging.info(output)
            os.chdir('vt')
            command = 'make'
            output = check_output(command, shell=True)
            print(output)
            logging.info(output)

    def main(self):
        vt = self.vt
        command = '{}/vt decompose -s {} \
        | {}/vt normalize -r {} - > {}'.format(self.vt, args.input, self.vt, args.reference, args.output)
        output = check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        print(output)
        logging.info(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Decompose and normalize a VCF file.')
    parser.add_argument('--install', dest='install', action='store_true')
    parser.add_argument('--reinstall', dest='reinstall', action='store_true')
    parser.add_argument('-i', dest='input', required=False, metavar='sample.vcf', help='a VCF file to be annotated')
    parser.add_argument('-r', dest='reference', required=False, metavar='reference.fasta', help='a reference fasta')
    parser.add_argument('-o', dest='output', required=False, metavar='reference.fasta', help='a reference fasta')
    args = parser.parse_args()

    vt = VT(args)
    vt.main()
