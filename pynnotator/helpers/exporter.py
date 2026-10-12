import argparse
import csv
import os
import re

import cyvcf2

# VEP annotation columns to extract from the CSQ field
VEP_FIELDS = [
    'Consequence', 'IMPACT', 'SYMBOL', 'Gene', 'Feature', 'BIOTYPE',
    'EXON', 'INTRON', 'HGVSc', 'HGVSp', 'cDNA_position', 'CDS_position',
    'Protein_position', 'Amino_acids', 'Codons', 'Existing_variation',
    'SIFT', 'PolyPhen', 'HGNC_ID',
    'CANONICAL', 'gnomADg_AF', 'gnomADe_AF',
    'clinvar_CLNSIG', 'clinvar_CLNDN', 'clinvar_CLNREVSTAT',
]


def _parse_csq_format(reader):
    """Extract CSQ field order from the VCF header. Returns list of field names or []."""
    for h in reader.header_iter():
        try:
            d = h.info()
            if d and d.get('ID') == 'CSQ':
                desc = d.get('Description', '')
                m = re.search(r'Format:\s*(.+?)(?:"|$)', desc)
                if m:
                    return m.group(1).strip().split('|')
        except Exception:
            pass
    return []


def _csq_to_dict(csq_value, csq_format):
    """Parse the first CSQ transcript into a flat dict using csq_format."""
    if not csq_value or not csq_format:
        return {}
    first = csq_value.split(',')[0] if isinstance(csq_value, str) else csq_value[0]
    parts = first.split('|')
    result = {}
    for i, field in enumerate(csq_format):
        if field in VEP_FIELDS:
            result[field] = parts[i] if i < len(parts) else ''
    return result


def to_csv(vcf_path, csv_path=None):
    if csv_path is None:
        csv_path = vcf_path.rsplit('.', 1)[0] + '.csv'

    reader = cyvcf2.VCF(vcf_path)
    csq_format = _parse_csq_format(reader)
    info_ids = []
    for h in reader.header_iter():
        try:
            d = h.info()
            if d and 'ID' in d and d['ID'] != 'CSQ':
                info_ids.append(d['ID'])
        except Exception:
            pass

    vep_cols = [f for f in VEP_FIELDS if f in csq_format]
    with open(csv_path, 'w', newline='') as f:
        fieldnames = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER'] + vep_cols + info_ids
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for variant in reader:
            row = {
                'CHROM': variant.CHROM,
                'POS': variant.POS,
                'ID': variant.ID or '.',
                'REF': variant.REF,
                'ALT': ','.join(variant.ALT),
                'QUAL': variant.QUAL,
                'FILTER': variant.FILTER or 'PASS',
            }
            csq_raw = variant.INFO.get('CSQ')
            if csq_raw is not None:
                row.update(_csq_to_dict(csq_raw, csq_format))
            for key in info_ids:
                val = variant.INFO.get(key)
                if val is not None:
                    row[key] = str(val)
            writer.writerow(row)

    reader.close()
    return csv_path


def to_parquet(vcf_path, parquet_path=None, batch_size=50000):
    """Write a Parquet file in row batches with a fixed schema.

    Columns: CHROM, POS (int64), ID, REF, ALT, QUAL, FILTER, the VEP fields
    present in the CSQ header, then every INFO field declared in the header.
    All columns except POS are strings. Building one DataFrame from per-row
    dicts used several GB for array-sized VCFs (600k+ records).
    """
    import pyarrow as pa
    import pyarrow.parquet as pq

    if parquet_path is None:
        parquet_path = vcf_path.rsplit('.', 1)[0] + '.parquet'

    reader = cyvcf2.VCF(vcf_path)
    csq_format = _parse_csq_format(reader)
    info_ids = []
    for h in reader.header_iter():
        try:
            d = h.info()
            if d and 'ID' in d and d['ID'] != 'CSQ' and d['ID'] not in info_ids:
                info_ids.append(d['ID'])
        except Exception:
            pass
    vep_cols = [f for f in VEP_FIELDS if f in csq_format]
    base = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER']
    columns = base + vep_cols + [c for c in info_ids if c not in base and c not in vep_cols]
    schema = pa.schema([(c, pa.int64() if c == 'POS' else pa.string()) for c in columns])

    def _text(val):
        if val is None:
            return None
        if isinstance(val, (list, tuple)):
            return ','.join(str(v) for v in val)
        return str(val)

    writer = pq.ParquetWriter(parquet_path, schema)
    buffer = {c: [] for c in columns}
    rows = 0
    try:
        for variant in reader:
            row = {
                'CHROM': variant.CHROM,
                'POS': variant.POS,
                'ID': variant.ID or '.',
                'REF': variant.REF,
                'ALT': ','.join(variant.ALT),
                'QUAL': _text(variant.QUAL),
                'FILTER': variant.FILTER or 'PASS',
            }
            csq_raw = variant.INFO.get('CSQ')
            if csq_raw is not None:
                row.update(_csq_to_dict(csq_raw, csq_format))
            for key in info_ids:
                if key not in row:
                    row[key] = _text(variant.INFO.get(key))
            for c in columns:
                value = row.get(c)
                buffer[c].append(value if c == 'POS' or value is None else str(value))
            rows += 1
            if rows % batch_size == 0:
                writer.write_table(pa.table(buffer, schema=schema))
                buffer = {c: [] for c in columns}
        if buffer['CHROM']:
            writer.write_table(pa.table(buffer, schema=schema))
    finally:
        writer.close()
        reader.close()
    return parquet_path


def export_all(vcf_path, formats=None):
    if formats is None:
        formats = ['csv', 'parquet']
    results = {}
    for fmt in formats:
        if fmt == 'csv':
            results['csv'] = to_csv(vcf_path)
        elif fmt == 'parquet':
            results['parquet'] = to_parquet(vcf_path)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export annotated VCF to CSV and/or Parquet.')
    parser.add_argument('-i', dest='vcf', required=True, help='Input VCF file')
    parser.add_argument('-f', dest='formats', nargs='+', default=['csv', 'parquet'], help='Output formats (csv, parquet)')
    args = parser.parse_args()
    export_all(args.vcf, args.formats)
