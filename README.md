# Pynnotator

A modern VEP-centric VCF annotation framework for exomes and genomes.

## Quick Start

```bash
# Install
git clone https://github.com/raonyguimaraes/pynnotator
cd pynnotator
pip install -e .

# Install VEP
conda install -c bioconda ensembl-vep
# Or download cache:
# vep_install -a cf -s homo_sapiens -y GRCh38 -c pynnotator/data/vep_data

# Run
pynnotator -i sample.vcf.gz
```

## Architecture

```
Input VCF → vcf-sort → VEP 115 → Python varType → CSV + Parquet
```

**VEP is the single annotation engine** with configurable plugins (AlphaMissense, SpliceAI, REVEL). No Java dependencies.

## Output

For `sample.vcf.gz`, the pipeline creates `ann_sample/` containing:

| File | Format | Description |
|------|--------|-------------|
| `annotation.final.vcf` | VCF | VEP CSQ + VARTYPE + HET/HOM |
| `annotation.final.csv` | CSV | All INFO fields flattened |
| `annotation.final.parquet` | Parquet | Columnar format for downstream analysis |

## Configuration

Edit `pynnotator/config.yaml`:

```yaml
build: hg38                     # or hg19
vep:
  release: 115
  cores: 4
  plugins: [AlphaMissense, SpliceAI, REVEL]
output:
  formats: [vcf.gz, csv, parquet]
databases:
  gnomad: /path/to/gnomad.vcf.gz
  clinvar: /path/to/clinvar.vcf.gz
```

## Commands

| Command | Description |
|---------|-------------|
| `pynnotator -i sample.vcf` | Annotate a VCF |
| `pynnotator install` | Install dependencies |
| `pynnotator test` | Run test on sample VCFs |
| `pynnotator build` | Build annotation datasets |

## Requirements

- Python 3.8+
- VEP 115 (conda: `conda install -c bioconda ensembl-vep`)
- bcftools, tabix, vcf-sort

## Changes from v2.0

See [CHANGELOG.md](CHANGELOG.md) for the full list of changes. Key highlights:
- **Dropped** SnpEff, SnpSift, vcfanno — VEP handles everything
- **Replaced** Java-based varType with Python (`cyvcf2`)
- **Added** Parquet export, YAML config, VEP plugin support
- **Default** build changed from hg19 to hg38
- **Removed** 22 dead helper files, 35GB data tarball dependency

## Annotation Example

From 15 variants on chr1, VEP 115 annotates with:

```
chr1 69511 A→G  CSQ=missense_variant|MODERATE|OR4F5|tolerated(0.92)|benign(0);VARTYPE=SNP
chr1 881627 G→A  CSQ=missense_variant|MODERATE|OR4F5|deleterious(0.01)|possibly_damaging(0.64);VARTYPE=SNP;HET
```
