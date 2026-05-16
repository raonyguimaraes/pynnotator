import argparse
import os
import shlex
from datetime import datetime
from subprocess import call


toolname = 'sanity_check'


class Sanity_check(object):
    def __init__(self, vcf_file=None):

        self.vcf_file = vcf_file
        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]

        if not os.path.exists('sanity_check'):
            os.makedirs('sanity_check')

    def run(self):

        tstart = datetime.now()
        print(tstart, 'Starting sanity_check: ', self.vcf_file)
        self.check()
        tend = datetime.now()
        print(tend, 'Finished sanity_check, it took: ', tend - tstart)

    def check(self):
        out = 'sanity_check/sorted.vcf'
        call('vcf-sort %s > %s' % (shlex.quote(self.vcf_file), out), shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sanity Check a VCf File')
    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')
    args = parser.parse_args()
    sanity_check = Sanity_check(args.vcf_file)
    sanity_check.run()
