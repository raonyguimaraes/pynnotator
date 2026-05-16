import os

import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
libs_dir = os.path.join(BASE_DIR, 'libs')
data_dir = os.path.join(BASE_DIR, 'data')

config_path = os.path.join(BASE_DIR, 'config.yaml')
if os.path.exists(config_path):
    with open(config_path) as f:
        _cfg = yaml.safe_load(f)
else:
    _cfg = {}

BUILD = _cfg.get('build', 'hg38')

vep_release = str(_cfg.get('vep', {}).get('release', '115'))
vep_cores = str(_cfg.get('vep', {}).get('cores', 4))
vep_cache_dir = _cfg.get('vep', {}).get('cache_dir')
_vep_in_path = next((os.path.dirname(os.path.realpath(p)) for p in os.environ.get('PATH', '').split(':') if os.path.exists(os.path.join(p, 'vep'))), None)
vep_dir = _vep_in_path or os.path.join(libs_dir, 'vep', 'src', 'ensembl-vep')
vep_source = 'https://github.com/Ensembl/ensembl-vep/archive/release/%s.zip' % vep_release
vep_plugins = _cfg.get('vep', {}).get('plugins', [])

OUTPUT_FORMATS = _cfg.get('output', {}).get('formats', ['vcf.gz', 'csv', 'parquet'])

gnomad_file = _cfg.get('databases', {}).get('gnomad')
clinvar_file = _cfg.get('databases', {}).get('clinvar')

java_memory = _cfg.get('resources', {}).get('java_memory', '8G')
