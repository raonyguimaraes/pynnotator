import argparse
import os

import cyvcf2


def classify(ref, alt):
    if len(ref) == 1 and len(alt) == 1:
        return 'SNP'
    if len(ref) > 1 and len(alt) > 1 and len(ref) == len(alt):
        return 'MNP'
    if len(ref) < len(alt):
        return 'INS'
    if len(ref) > len(alt):
        return 'DEL'
    return 'MIXED'


def annotate(in_vcf, out_vcf=None):
    if out_vcf is None:
        base, ext = os.path.splitext(in_vcf)
        if ext == '.gz':
            base, _ = os.path.splitext(base)
        out_vcf = base + '.vartype.vcf'

    reader = cyvcf2.VCF(in_vcf)
    reader.add_info_to_header({'ID': 'VARTYPE', 'Description': 'Variant type (SNP/MNP/INS/DEL/MIXED)', 'Type': 'String', 'Number': '1'})
    reader.add_info_to_header({'ID': 'HET', 'Description': 'Heterozygous', 'Type': 'Flag', 'Number': '0'})
    reader.add_info_to_header({'ID': 'HOM', 'Description': 'Homozygous', 'Type': 'Flag', 'Number': '0'})

    writer = cyvcf2.Writer(out_vcf, reader)

    for variant in reader:
        variant.INFO['VARTYPE'] = classify(variant.REF, variant.ALT[0])
        gt_types = variant.gt_types
        if 1 in gt_types:
            variant.INFO['HET'] = True
        if 2 in gt_types:
            variant.INFO['HOM'] = True
        writer.write_record(variant)

    writer.close()
    reader.close()
    return out_vcf


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate VCF with variant types (SNP/MNP/INS/DEL/MIXED).')
    parser.add_argument('-i', dest='vcf', required=True, help='Input VCF file')
    parser.add_argument('-o', dest='output', default=None, help='Output VCF file')
    args = parser.parse_args()
    annotate(args.vcf, args.output)
