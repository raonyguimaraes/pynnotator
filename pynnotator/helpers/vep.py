import argparse
import os
import shlex
import subprocess
from datetime import datetime

from pynnotator import settings

toolname = 'vep'


class Vep(object):
    def __init__(self, args=None):

        self.args = args
        self.build = 'GRCh38' if getattr(args, 'build', 'hg38') == 'hg38' else 'GRCh37'

        self.vcffile = args.vcf_file
        self.filename = os.path.splitext(os.path.basename(str(self.vcffile)))[0]

        vep_bin = os.path.join(settings.vep_dir, 'vep')
        self.vep_cmd = 'vep' if os.path.exists(os.path.join('/usr/bin', 'vep')) or os.path.exists(
            os.path.join('/usr/local/bin', 'vep')) or not os.path.exists(vep_bin) else vep_bin

        if not os.path.exists('vep'):
            os.makedirs('vep')

    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting VEP annotation: ', self.build, self.vcffile)
        result = self.annotate()
        tend = datetime.now()
        print(tend, 'Finished VEP annotation, it took: ', tend - tstart)
        return result

    def annotate(self):
        cmd = [
            self.vep_cmd,
            '-i', self.vcffile,
            '--format', 'vcf',
            '-o', 'vep/vep.output.vcf', '--vcf', '--force_overwrite',
            '--assembly', self.build,
            '--sift', 'b', '--polyphen', 'b',
            '--no_progress',
            '--numbers',
            '--biotype',
            '--total_length',
            '--coding_only',
            '--pick',
            '--symbol',
            '--fork', str(settings.vep_cores),
        ]

        if settings.vep_cache_dir and os.path.exists(settings.vep_cache_dir):
            cmd += ['--cache', '--dir', settings.vep_cache_dir, '--offline']
        else:
            cmd.append('--database')

        for plugin in settings.vep_plugins:
            cmd += ['--plugin', plugin]

        if settings.gnomad_file and os.path.exists(settings.gnomad_file):
            cmd += ['--custom', '%s,gnomad,vcf,exact,0,AF,AF_popmax,AF_male,AF_female' % settings.gnomad_file]

        if settings.clinvar_file and os.path.exists(settings.clinvar_file):
            cmd += ['--custom', '%s,clinvar,vcf,exact,0,CLNSIG,CLNREVSTAT,CLNDN' % settings.clinvar_file]

        print('Running VEP:', ' '.join(shlex.quote(str(c)) for c in cmd))
        vep_base = os.path.join(settings.libs_dir, 'vep')
        perl5_paths = [
            os.path.join(vep_base, 'perl5'),
            os.path.join(settings.vep_dir, 'modules'),
        ]
        env = os.environ.copy()
        existing = env.get('PERL5LIB', '')
        env['PERL5LIB'] = ':'.join(perl5_paths + ([existing] if existing else []))
        with open('vep/vep.log', 'w') as log:
            p = subprocess.call(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)

        if p != 0:
            print('VEP returned non-zero exit code:', p)
            return p

        result = 'vep/vep.output.vcf'
        try:
            subprocess.check_call(['bcftools', 'sort', '-o', 'vep/vep.output.sorted.vcf', result])
            os.remove(result)
            result = 'vep/vep.output.sorted.vcf'
        except (subprocess.CalledProcessError, OSError):
            print('bcftools sort not available, using unsorted VEP output')

        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate a VCF File with VEP.')
    parser.add_argument('-i', dest='vcffile', required=True, metavar='example.vcf', help='a VCF file to be annotated')
    parser.add_argument('-b', dest='build', default='hg38', help='Genome build (hg19 or hg38)')
    args = parser.parse_args()
    vep = Vep(args)
    vep.run()
