import os

import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
libs_dir = os.path.join(BASE_DIR, 'libs')
data_dir = os.path.join(BASE_DIR, 'data')

def _load(path):
    if os.path.exists(path):
        with open(path) as f:
            return yaml.safe_load(f) or {}
    return {}


def _merge(base, override):
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _merge(base[key], value)
        else:
            base[key] = value
    return base


config_path = os.path.join(BASE_DIR, 'config.yaml')
# Machine-specific paths (cache, databases) go in config.local.yaml, which is
# gitignored, so a server can follow master without a local commit.
local_config_path = os.path.join(BASE_DIR, 'config.local.yaml')
_cfg = _merge(_load(config_path), _load(local_config_path))

BUILD = _cfg.get('build', 'hg38')

vep_release = str(_cfg.get('vep', {}).get('release', '115'))
vep_cores = str(_cfg.get('vep', {}).get('cores', 4))
vep_cache_dir = _cfg.get('vep', {}).get('cache_dir')
_vep_in_path = next((os.path.dirname(os.path.realpath(p)) for p in os.environ.get('PATH', '').split(':') if os.path.exists(os.path.join(p, 'vep'))), None)
vep_dir = _vep_in_path or os.path.join(libs_dir, 'vep', 'src', 'ensembl-vep')
vep_source = 'https://github.com/Ensembl/ensembl-vep/archive/release/%s.zip' % vep_release
vep_plugins = _cfg.get('vep', {}).get('plugins', [])
# 'local' (default): local vep binary with an offline cache, nothing leaves the machine.
# 'rest': Ensembl REST API; sends variants to rest.ensembl.org, so it must be chosen explicitly.
vep_mode = str(_cfg.get('vep', {}).get('mode') or 'local').lower()
if vep_mode not in ('local', 'rest'):
    raise ValueError("vep.mode must be 'local' or 'rest', not %r" % vep_mode)

OUTPUT_FORMATS = _cfg.get('output', {}).get('formats', ['vcf.gz', 'csv', 'parquet'])

gnomad_file = _cfg.get('databases', {}).get('gnomad')
clinvar_file = _cfg.get('databases', {}).get('clinvar')

java_memory = _cfg.get('resources', {}).get('java_memory', '8G')
