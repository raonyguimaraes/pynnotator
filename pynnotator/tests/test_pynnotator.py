import os
import shutil
import subprocess
import tempfile

import pytest

from pynnotator.helpers import var_type, exporter


def test_var_type_snp():
    result = var_type.classify('A', 'G')
    assert result == 'SNP'


def test_var_type_mnp():
    result = var_type.classify('AT', 'GC')
    assert result == 'MNP'


def test_var_type_ins():
    result = var_type.classify('A', 'AT')
    assert result == 'INS'


def test_var_type_del():
    result = var_type.classify('AT', 'A')
    assert result == 'DEL'


def test_var_type_mixed():
    result = var_type.classify('AT', 'G')
    assert result == 'DEL'


@pytest.fixture
def mini_vcf():
    content = """##fileformat=VCFv4.2
##FILTER=<ID=PASS,Description="All filters passed">
##contig=<ID=1>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA00001
1	100	.	A	G	30	PASS	.	GT	0/1
1	200	.	T	C	30	PASS	.	GT	1/1
1	300	.	AT	A	30	PASS	.	GT	0/1
"""
    tmpdir = tempfile.mkdtemp()
    vcf_path = os.path.join(tmpdir, 'test.vcf')
    with open(vcf_path, 'w') as f:
        f.write(content)
    yield vcf_path
    shutil.rmtree(tmpdir)


def test_var_type_annotate_vcf(mini_vcf):
    output = var_type.annotate(mini_vcf)
    assert os.path.exists(output)
    with open(output) as f:
        header_lines = [l for l in f if l.startswith('##INFO')]
    assert any('VARTYPE' in l for l in header_lines)
    found = {}
    with open(output) as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            pos = fields[1]
            info = fields[7]
            found[pos] = info
    assert 'VARTYPE=SNP' in found['100']
    assert 'VARTYPE=SNP' in found['200']
    assert 'VARTYPE=DEL' in found['300']
    os.remove(output)


def test_csv_export(mini_vcf):
    csv_path = exporter.to_csv(mini_vcf)
    assert os.path.exists(csv_path)
    with open(csv_path) as f:
        header = f.readline().strip()
        assert 'CHROM' in header
        assert 'POS' in header
        assert 'REF' in header
        assert 'ALT' in header
    os.remove(csv_path)


def test_parquet_export(mini_vcf):
    pytest.importorskip('pandas')
    pytest.importorskip('pyarrow')
    parquet_path = exporter.to_parquet(mini_vcf)
    assert os.path.exists(parquet_path)
    import pandas as pd
    df = pd.read_parquet(parquet_path)
    assert len(df) > 0
    os.remove(parquet_path)


# --- VEP mode: local and offline unless REST is chosen explicitly ----------

def _vep_args(tmp_path):
    import argparse
    vcf = tmp_path / 'in.vcf'
    vcf.write_text('##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n')
    return argparse.Namespace(vcf_file=str(vcf), build='hg38')


def test_default_vep_mode_is_local():
    from pynnotator import settings
    assert settings.vep_mode == 'local'


def test_local_vep_never_falls_back_to_ensembl_database(tmp_path, monkeypatch):
    from pynnotator import settings
    from pynnotator.helpers import vep
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(settings, 'vep_cache_dir', str(tmp_path / 'missing-cache'))
    calls = []
    monkeypatch.setattr(vep.subprocess, 'call', lambda *a, **k: calls.append(a) or 0)
    with pytest.raises(RuntimeError, match='VEP cache not found'):
        vep.Vep(_vep_args(tmp_path)).run()
    assert calls == []


def test_local_vep_runs_offline_and_fails_loudly(tmp_path, monkeypatch):
    from pynnotator import settings
    from pynnotator.helpers import vep
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'cache').mkdir()
    monkeypatch.setattr(settings, 'vep_cache_dir', str(tmp_path / 'cache'))
    seen = {}

    def fake_call(cmd, **kwargs):
        seen['cmd'] = cmd
        return 2
    monkeypatch.setattr(vep.subprocess, 'call', fake_call)
    with pytest.raises(RuntimeError, match='VEP exited with code 2'):
        vep.Vep(_vep_args(tmp_path)).run()
    assert '--offline' in seen['cmd'] and '--database' not in seen['cmd']


@pytest.mark.parametrize('mode, expected', [('local', 'pynnotator.helpers.vep'),
                                            ('rest', 'pynnotator.helpers.vep_rest')])
def test_annotator_picks_vep_by_mode(tmp_path, monkeypatch, mode, expected):
    from pynnotator import annotator, settings
    from pynnotator.helpers import vep, vep_rest
    monkeypatch.setattr(settings, 'vep_mode', mode)
    used = []

    class Stop(Exception):
        pass

    def fake_init(self, args):
        used.append(type(self).__module__)
        raise Stop()
    monkeypatch.setattr(vep.Vep, '__init__', fake_init)
    monkeypatch.setattr(vep_rest.Vep, '__init__', fake_init)
    monkeypatch.setattr(annotator.sanity_check.Sanity_check, 'run', lambda self: None)
    monkeypatch.chdir(tmp_path)
    src = tmp_path / 'sample.vcf'
    src.write_text('##fileformat=VCFv4.2\n')
    import argparse
    with pytest.raises(Stop):
        annotator.Annotator(argparse.Namespace(vcf_file=str(src), build='hg38')).run()
    assert used == [expected]


def test_config_local_overrides(tmp_path):
    from pynnotator import settings
    base = {'vep': {'mode': 'local', 'cores': 2}, 'databases': {'clinvar': None}}
    over = {'vep': {'cache_dir': '/data/vep'}, 'databases': {'clinvar': '/data/clinvar.vcf.gz'}}
    merged = settings._merge(base, over)
    assert merged['vep'] == {'mode': 'local', 'cores': 2, 'cache_dir': '/data/vep'}
    assert merged['databases']['clinvar'] == '/data/clinvar.vcf.gz'
