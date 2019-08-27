#!/usr/bin/env python3

import argparse
import pynnotator

from subprocess import call, check_call

parser = argparse.ArgumentParser()
parser.add_argument('options', help='install test', nargs='?')
parser.add_argument('-i', dest='vcf_file', required=False, metavar='example.vcf', help='a VCF file to be annotated')
parser.add_argument('-b', dest='build', required=False, metavar='hg19 or hg38', help='The genome build you want to use')

args = parser.parse_args()

def main():

    if args.options == 'update':
        print('Updating Pynnotator to latest version...')
        output = check_call('pip install -U pynnotator', shell=True)
        if output == 0:
            print('Pynnotator was updated!')
    if args.options == 'install':
        obj = pynnotator.Pynnotator()
        obj.install()
    elif args.options == 'install_libs':
        obj = pynnotator.Pynnotator()
        obj.install_libs()
    elif args.options == 'install_requirements':
        obj = pynnotator.Pynnotator()
        obj.install_requirements()
    elif args.options == 'build':
        obj = pynnotator.Pynnotator()
        obj.build()
    elif args.vcf_file:
        obj = pynnotator.Pynnotator()
        obj.annotate(args.vcf_file)
    elif args.options == 'test':
        obj = pynnotator.Pynnotator()
        obj.test()
    elif args.options == 'vep':
        obj = pynnotator.Pynnotator()
        obj.vep()