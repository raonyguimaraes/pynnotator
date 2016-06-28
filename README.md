# Pynnotator

A Python Annotation Framework for VCF files (Exome or Genome) from Humans using multiple tools and databases.

Features
========
- Multithread Efficient
- Annotate a VCF file using multiple VCF as a reference

Requirements
============

- Ubuntu 16.04 (probably also works on 14.04)
- Python 3.4+

Installation 
============

1º Method
    pip install pynnotator
    pynnotator install

2º Method
    docker-compose up

Libraries
=========

- htslib
- vcftools
- snpeff
- vep

Databases
=========

- 1000Genomes (Phase 3) - ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf 
- dbSNP (including clinvar) - (human_9606_b147_GRCh37p13) 
- Exome Sequencing Project - ESP6500SI-V2-SSA137.GRCh38-liftover
- dbNFSP (including dbscSNV) - 

