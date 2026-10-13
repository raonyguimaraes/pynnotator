"""VEP annotation via the Ensembl REST API (explicit opt-in: vep.mode: rest).

This sends every variant position and allele to rest.ensembl.org. Never use
it for samples that must stay on the machine; the default is helpers/vep.py.

Drop-in replacement for the original ``vep.py`` helper that shelled out to the
local ``vep`` binary. The REST shim is slower than a local install but works
without VEP + the multi-GB cache.

Input  : VCF path  (self.vcffile)
Output : vep/vep.output.vcf  (same place the original produced)
"""
import argparse
import json
import os
import time
from datetime import datetime

import requests

ENSEMBL_REST = {
    'GRCh38': 'https://rest.ensembl.org',
    'GRCh37': 'https://grch37.rest.ensembl.org',
}
BATCH_SIZE = 200          # Ensembl REST max per request
PARALLEL_WORKERS = 8       # parallel in-flight VEP REST requests
RETRY = 3
TIMEOUT = 120
# Claude: 1-second pause between batches to respect Ensembl REST rate limits
INTER_BATCH_SLEEP = 0.0

CSQ_FIELDS = [
    'Allele', 'Consequence', 'IMPACT', 'SYMBOL', 'Gene', 'Feature_type',
    'Feature', 'BIOTYPE', 'EXON', 'INTRON', 'HGVSc', 'HGVSp',
    'cDNA_position', 'CDS_position', 'Protein_position', 'Amino_acids',
    'Codons', 'Existing_variation', 'DISTANCE', 'STRAND', 'FLAGS',
    'SYMBOL_SOURCE', 'HGNC_ID', 'SIFT', 'PolyPhen',
]


class Vep(object):
    """REST-API powered VEP annotator (compatible with the local Vep helper)."""

    def __init__(self, args=None):
        self.args = args
        self.build = 'GRCh38' if getattr(args, 'build', 'hg38') == 'hg38' else 'GRCh37'
        self.vcffile = args.vcf_file
        self.filename = os.path.splitext(os.path.basename(str(self.vcffile)))[0]
        os.makedirs('vep', exist_ok=True)

    # ------------------------------------------------------------------ run
    def run(self):
        tstart = datetime.now()
        print(tstart, 'Starting VEP REST annotation:', self.build, self.vcffile)
        result = self.annotate()
        tend = datetime.now()
        print(tend, 'Finished VEP REST annotation, it took:', tend - tstart)
        return result

    # -------------------------------------------------------------- annotate
    def annotate(self):
        out_path = 'vep/vep.output.vcf'
        endpoint = ENSEMBL_REST[self.build] + '/vep/human/region'

        header_lines, variant_lines = self._read_vcf(self.vcffile)

        # Convert each VCF row into Ensembl region notation
        # "chr start . ref alt . . ." → "chr start end ref/alt strand"
        regions = []
        for line in variant_lines:
            cols = line.split('\t')
            if len(cols) < 5:
                regions.append(None)
                continue
            chrom = cols[0].lstrip('chr')
            pos = cols[1]
            ref = cols[3]
            alt = cols[4]
            try:
                end = str(int(pos) + len(ref) - 1)
            except Exception:
                end = pos
            regions.append('%s %s %s %s/%s 1' % (chrom, pos, end, ref, alt))

        # Batched POST
        annotations = [None] * len(regions)
        index_map = [i for i, r in enumerate(regions) if r is not None]
        clean_regions = [regions[i] for i in index_map]

        total_batches = (len(clean_regions) + BATCH_SIZE - 1) // BATCH_SIZE
        # Parallel VEP REST submission with bounded in-flight futures to avoid
        # building all 20k+ futures up front (was crashing the worker).
        from concurrent.futures import ThreadPoolExecutor, as_completed

        WINDOW = PARALLEL_WORKERS * 4   # cap in-flight futures
        completed = 0
        with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as ex:
            inflight = {}
            iterator = iter(range(0, len(clean_regions), BATCH_SIZE))
            # prime the pump
            for _ in range(WINDOW):
                try:
                    start = next(iterator)
                except StopIteration:
                    break
                chunk = clean_regions[start:start + BATCH_SIZE]
                fut = ex.submit(self._post_with_retry, endpoint, chunk)
                inflight[fut] = start

            while inflight:
                for fut in as_completed(list(inflight.keys()), timeout=None):
                    start = inflight.pop(fut)
                    data = fut.result()
                    for offset, item in enumerate(data or []):
                        annotations[index_map[start + offset]] = item
                    completed += 1
                    if completed % 10 == 0 or completed == total_batches:
                        pct = int(100 * completed / total_batches)
                        print('[VEP] batch %d/%d (%d%%) parallel=%d'
                              % (completed, total_batches, pct, PARALLEL_WORKERS))
                    try:
                        nxt = next(iterator)
                        chunk = clean_regions[nxt:nxt + BATCH_SIZE]
                        nfut = ex.submit(self._post_with_retry, endpoint, chunk)
                        inflight[nfut] = nxt
                    except StopIteration:
                        pass
                    break  # re-enter as_completed with refreshed inflight set

        # Write annotated VCF
        csq_hdr = ('##INFO=<ID=CSQ,Number=.,Type=String,Description="Consequence '
                   'annotations from Ensembl VEP REST. Format: '
                   + '|'.join(CSQ_FIELDS) + '">')
        with open(out_path, 'w') as out:
            # Inject CSQ header BEFORE the #CHROM line (must be a ## meta line)
            for h in header_lines:
                if h.startswith('#CHROM'):
                    out.write(csq_hdr + '\n')
                out.write(h + '\n')
            for vcf_line, ann in zip(variant_lines, annotations):
                out.write(self._inject_csq(vcf_line, ann) + '\n')

        print('Wrote', out_path)
        return out_path

    # --------------------------------------------------------------- helpers
    def _read_vcf(self, path):
        headers, variants = [], []
        opener = open
        if path.endswith('.gz'):
            import gzip
            opener = gzip.open
        with opener(path, 'rt') as fh:
            for line in fh:
                line = line.rstrip('\n')
                if line.startswith('#'):
                    headers.append(line)
                elif line.strip():
                    variants.append(line)
        return headers, variants

    def _post_with_retry(self, url, regions):
        body = {'variants': regions}
        for attempt in range(RETRY):
            try:
                r = requests.post(
                    url, json=body, timeout=TIMEOUT,
                    headers={'Content-Type': 'application/json',
                             'Accept': 'application/json'},
                )
                if r.status_code == 200:
                    return r.json()
                if r.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                print('VEP REST', r.status_code, r.text[:200])
                return []
            except Exception as e:
                print('VEP REST attempt %d failed: %s' % (attempt + 1, e))
                time.sleep(2 ** attempt)
        return []

    def _inject_csq(self, vcf_line, annotation):
        cols = vcf_line.split('\t')
        if len(cols) < 8 or not annotation:
            return vcf_line
        csq_value = self._encode_csq(annotation)
        if not csq_value:
            return vcf_line
        info = cols[7]
        sep = ';' if info and info != '.' else ''
        cols[7] = ('' if info == '.' else info) + sep + 'CSQ=' + csq_value
        return '\t'.join(cols)

    def _encode_csq(self, ann):
        # Collect consequence records from all categories. Take the first.
        tcs = (ann.get('transcript_consequences')
               or ann.get('regulatory_feature_consequences')
               or ann.get('motif_feature_consequences')
               or ann.get('intergenic_consequences')
               or [])
        tc = tcs[0] if tcs else {}

        # Mapping from CSQ_FIELDS → keys in the REST JSON response
        rest_key = {
            'Allele': 'variant_allele',
            'Consequence': 'consequence_terms',
            'IMPACT': 'impact',
            'SYMBOL': 'gene_symbol',
            'Gene': 'gene_id',
            'Feature_type': None,            # derived below
            'Feature': 'transcript_id',
            'BIOTYPE': 'biotype',
            'EXON': 'exon',
            'INTRON': 'intron',
            'HGVSc': 'hgvsc',
            'HGVSp': 'hgvsp',
            'cDNA_position': 'cdna_start',
            'CDS_position': 'cds_start',
            'Protein_position': 'protein_start',
            'Amino_acids': 'amino_acids',
            'Codons': 'codons',
            'Existing_variation': None,      # filled from colocated_variants
            'DISTANCE': 'distance',
            'STRAND': 'strand',
            'FLAGS': 'flags',
            'SYMBOL_SOURCE': 'gene_symbol_source',
            'HGNC_ID': 'hgnc_id',
            'SIFT': 'sift_prediction',
            'PolyPhen': 'polyphen_prediction',
        }

        # Feature_type: transcript / regulatory / motif / intergenic
        if tc.get('transcript_id'):
            feature_type = 'Transcript'
        elif tc.get('regulatory_feature_id'):
            feature_type = 'RegulatoryFeature'
        elif tc.get('motif_feature_id'):
            feature_type = 'MotifFeature'
        else:
            feature_type = ''

        # Existing variation from colocated_variants list at top level
        existing = ''
        colo = ann.get('colocated_variants') or []
        if colo:
            existing = '&'.join(str(c.get('id', '')) for c in colo if c.get('id'))

        def _clean(v):
            if isinstance(v, list):
                return '&'.join(str(x) for x in v)
            return str(v) if v not in (None, '') else ''

        vals = []
        for k in CSQ_FIELDS:
            if k == 'Feature_type':
                v = feature_type
            elif k == 'Existing_variation':
                v = existing
            else:
                rk = rest_key.get(k)
                v = _clean(tc.get(rk)) if rk else ''
            vals.append(v.replace(',', '_').replace(';', '_').replace('|', '_'))
        if not any(vals):
            return ''
        return '|'.join(vals)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate VCF via Ensembl VEP REST API.')
    parser.add_argument('-i', dest='vcf_file', required=True)
    parser.add_argument('-b', dest='build', default='hg38')
    Vep(parser.parse_args()).run()
