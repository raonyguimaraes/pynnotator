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
