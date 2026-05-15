import argparse
import csv
import os

import cyvcf2


def to_csv(vcf_path, csv_path=None):
    if csv_path is None:
        csv_path = vcf_path.rsplit('.', 1)[0] + '.csv'

    reader = cyvcf2.VCF(vcf_path)
    info_ids = []
    for h in reader.header_iter():
        try:
            d = h.info()
            if d and 'ID' in d:
                info_ids.append(d['ID'])
        except Exception:
            pass

    with open(csv_path, 'w', newline='') as f:
        fieldnames = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER'] + info_ids
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
            for key in info_ids:
                val = variant.INFO.get(key)
                if val is not None:
                    row[key] = str(val)
            writer.writerow(row)

    reader.close()
    return csv_path


def to_parquet(vcf_path, parquet_path=None):
    import pandas as pd

    if parquet_path is None:
        parquet_path = vcf_path.rsplit('.', 1)[0] + '.parquet'

    reader = cyvcf2.VCF(vcf_path)
    records = []
    for variant in reader:
        d = {
            'CHROM': variant.CHROM,
            'POS': variant.POS,
            'ID': variant.ID or '.',
            'REF': variant.REF,
            'ALT': ','.join(variant.ALT),
            'QUAL': variant.QUAL,
            'FILTER': variant.FILTER or 'PASS',
        }
        for key, val in dict(variant.INFO).items():
            if isinstance(val, (list, tuple)):
                d[key] = ','.join(str(v) for v in val)
            elif val is None:
                d[key] = None
            else:
                d[key] = str(val)
        records.append(d)
    reader.close()

    df = pd.DataFrame(records)
    df.to_parquet(parquet_path, index=False)
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
