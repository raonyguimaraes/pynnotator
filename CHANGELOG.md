# Changelog

## 3.0 — Modern VEP-Centric Architecture

### Architecture Rewrite

**Before (v2.0):** Three parallel annotation engines + merge step
```
Input VCF → snpEff + VEP + SnpSift (parallel) → vcfanno merge → vcf2csv.py
```

**After (v3.0):** Single-pass VEP engine with Python-native post-processing
```
Input VCF → bcftools sort → VEP 115 (with plugins) → varType (Python) → CSV + Parquet
```

### What Changed

| Area | v2.0 | v3.0 |
|------|------|------|
| **Annotation engine** | snpEff + SnpSift + VEP | VEP only |
| **Variant classification** | SnpSift varType (Java) | Python `var_type.py` (cyvcf2) |
| **VEP version** | Release 103 | Release 115 |
| **Default build** | hg19 | hg38 |
| **Intermediate files** | Uncompressed VCF | Handles `.vcf.gz` natively |
| **Sorting** | vcf-sort (vcftools) | Falls back gracefully |
| **Export** | vcf2csv.py only | CSV + Parquet (via pandas/pyarrow) |
| **Configuration** | Hardcoded paths in settings.py | `config.yaml` |
| **VEP plugins** | None | Configurable (AlphaMissense, SpliceAI, REVEL) |
| **Custom annotations** | None | gnomAD + ClinVar via VEP `--custom` |

### Files Removed (22 dead helpers deleted)

- `snpeff.py`, `snpsift.py`, `merge.py` — replaced by VEP
- `dbnsfp.py`, `decipher.py`, `hgmd.py`, `func_pred.py` — unused / superseded
- `gemini.py`, `gnomad.py`, `validator.py`, `vcf_annotator.py`, `vt.py` — never used in pipeline
- 5 pre-existing dead variants (`dbnsfp.*.py`, `merge.*.py`)
- `scripts/` directory, `fabfile.py`, `devlog.txt`

### New Files

- `config.yaml` — externalized configuration
- `helpers/var_type.py` — SnpSift-free variant classification
- `helpers/exporter.py` — CSV + Parquet export
- `tests/test_pynnotator.py` — 8 pytest tests with real output validation

### Dependencies

- **Removed:** Java (no more snpEff/SnpSift), `nose`, Perl vcftools modules
- **Added:** `cyvcf2`, `pyyaml`, `pandas+pyarrow` (optional, for parquet)

### Pipeline Flow

```
Input: sample.vcf.gz
  │
  ├─ 1. vcf-sort → sanity_check/sorted.vcf
  ├─ 2. VEP (database or cache mode)
  │     └── CSQ annotations for all variants
  ├─ 3. Python varType → VARTYPE, HET, HOM
  ├─ 4. CSV export → sample.csv
  └─ 5. Parquet export → sample.parquet
```
