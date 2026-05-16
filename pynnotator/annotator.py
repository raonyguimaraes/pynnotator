import argparse
import os
import shutil
import subprocess
from datetime import datetime

from . import settings
from .helpers import sanity_check, vep
from .helpers import var_type as var_type_mod
from .helpers import exporter

import logging


class Annotator(object):

    def __init__(self, args=None):

        self.args = args
        self.build = getattr(args, 'build', None) or settings.BUILD

        self.vcf_file = os.path.abspath(str(args.vcf_file))

        self.filename = os.path.splitext(os.path.basename(self.vcf_file))[0]
        self.filename = self.filename.replace('.vcf.gz', '').replace('.vcf', '')

        logging.basicConfig(filename='%s.log' % self.filename, level=logging.DEBUG)

        self.ann_name = 'ann_%s' % self.filename

        if os.path.exists(self.ann_name):
            shutil.rmtree(self.ann_name)

        os.makedirs(self.ann_name)
        os.chdir(self.ann_name)

    def run(self):

        tstart = datetime.now()

        if self.vcf_file.endswith('.vcf.gz'):
            path = os.path.dirname(self.vcf_file)
            new_name = '%s/%s/%s.vcf' % (path, self.ann_name, self.filename)
            subprocess.check_call(
                'gunzip -c %s > %s' % (self.vcf_file, new_name), shell=True)
            self.vcf_file = new_name
        else:
            path = os.path.dirname(self.vcf_file)
            new_name = '%s/%s/%s.vcf' % (path, self.ann_name, self.filename)
            shutil.copy(self.vcf_file, new_name)
            self.vcf_file = new_name

        sanitycheck = sanity_check.Sanity_check(self.vcf_file)
        sanitycheck.run()
        self.args.vcf_file = 'sanity_check/sorted.vcf'

        vep_obj = vep.Vep(self.args)
        vep_out = vep_obj.run()

        merged_vcf = vep_out if vep_out and os.path.exists(vep_out) and os.path.getsize(vep_out) > 0 else 'sanity_check/sorted.vcf'

        var_type_mod.annotate(merged_vcf, 'annotation.final.vcf')

        self.vcf2csv()
        self.export_parquet()

        tend = datetime.now()
        print(tend, 'Finished Annotation, it took %s' % (tend - tstart))

        output = """
A       A G       T G       A       A G       T G       A
| C   C | | C   C | | A   C | C   C | | C   C | | A   C |
| | T | | | | A | | | | G | | | T | | | | A | | | | G | |
| G   G | | G   G | | T   G | G   G | | G   G | | T   G |
T       T C       A C       T       T C       A C       T
"""
        print(output)

    def vcf2csv(self):
        tstart = datetime.now()
        print(tstart, 'Convert VCF to CSV...')
        vcf_path = 'annotation.final.vcf'
        if os.path.exists(vcf_path) and os.path.getsize(vcf_path) > 0:
            exporter.to_csv(vcf_path)
        tend = datetime.now()
        print(tend, 'CSV export took %s' % (tend - tstart))

    def export_parquet(self):
        tstart = datetime.now()
        print(tstart, 'Export to Parquet...')
        vcf_path = 'annotation.final.vcf'
        if os.path.exists(vcf_path) and os.path.getsize(vcf_path) > 0:
            try:
                exporter.to_parquet(vcf_path)
            except ImportError:
                print('pandas/pyarrow not available, skipping Parquet export')
        tend = datetime.now()
        print(tend, 'Parquet export took %s' % (tend - tstart))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Annotate a VCF File with Annotator.')
    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')
    parser.add_argument('-b', dest='build', required=False, default='hg38', metavar='hg19 or hg38', help='The genome build you want to use')
    args = parser.parse_args()

    a = Annotator(args)
    a.run()
