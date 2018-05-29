# Pynnotator

This is a Python Annotation Framework developed with the goal of annotating VCF files (Exomes or Genomes) from patients with Mendelian Disorders.

It was built using state-of-the-art tools and databases for human genome annotation.

Tools
=====

- htslib (1.5)
- vcftools (0.1.15)
- snpeff (SnpEff 4.3r)
- vep (version 91.1)

Databases
=========

- 1000Genomes (Phase 3) - ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf
- dbSNP (including clinvar) - (human_9606_b150_GRCh37p13)
- Exome Sequencing Project - ESP6500SI-V2-SSA137.GRCh38-liftover
- dbNFSP 3.5a (including dbscSNV 1.1)
- Ensembl 90 (phenotype and clinically associated variants)
- Decipher (HI_Predictions_Version3 and DDG2P)

Features
========

- Annotate an exome in only 10 minutes.
- Supports .VCF and .VCF.GZ files.
- 20 min installation.
- Multithread efficient!
- Annotate a VCF file using multiple VCFs as a reference.
- Combine the best tools and databases currently available for vcf annotation.

Files
=====


    .
    ├── 1000genomes
    │   ├── ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz
    │   └── ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.vcf.gz.tbi
    ├── dbnsfp
    │   ├── dbNSFP3.4a.txt.gz
    │   ├── dbNSFP3.4a.txt.gz.tbi
    │   ├── dbscSNV1.1.txt.gz
    │   └── dbscSNV1.1.txt.gz.tbi
    ├── dbsnp
    │   ├── All_20170403.vcf.gz
    │   ├── All_20170403.vcf.gz.tbi
    │   ├── clinvar.vcf.gz
    │   └── clinvar.vcf.gz.tbi
    ├── decipher
    │   ├── DDG2P.csv.gz
    │   ├── HI_Predictions_Version3.bed.gz
    │   ├── HI_Predictions_Version3.bed.gz.tbi
    │   └── population_cnv.txt.gz
    ├── ensembl
    │   ├── Homo_sapiens_clinically_associated.vcf.gz
    │   ├── Homo_sapiens_clinically_associated.vcf.gz.tbi
    │   ├── Homo_sapiens_phenotype_associated.vcf.gz
    │   └── Homo_sapiens_phenotype_associated.vcf.gz.tbi
    ├── esp6500
    │   ├── esp6500si.vcf.gz
    │   └── esp6500si.vcf.gz.tbi
    ├── snpeff_data
    │   └── GRCh37.75
    └── vep_cache
        └── homo_sapiens
            └── 88_GRCh37

705 directories, 11839 files

Examples of VCFs from patients with Mendelian Disorders
==================================================

    .
    ├── annotation.validated.vcf.gz
    ├── examples
    │   ├── miller.vcf.gz
    │   ├── NA12878.compound_heterozygous.vcf.gz
    │   ├── NA12878.dominant.vcf.gz
    │   ├── NA12878.recessive.vcf.gz
    │   ├── NA12878.xlinked.vcf.gz
    │   └── schinzel_giedion.vcf.gz
    └── sample.1000.vcf


Requirements
============
- Docker Compose
or
- Ubuntu 16.04 LTS or Red Hat/CentOS 7
- Python 2 or 3

How to run it?
==============

Requires at least 65GB of disk space during installation and 35GB after installed.

1º Method::

    docker-compose run pynnotator -i pynnotator/tests/sample.1000.vcf
    or
    docker-compose run pynnotator -i sample.vcf.gz


2º Method::

    # Using Ubuntu 16.04 LTS

    sudo apt-get install gcc git python3-dev zlib1g-dev make zip libssl-dev libbz2-dev liblzma-dev libcurl4-openssl-dev build-essential
    python3 -m venv mendelmdenv
    source mendelmdenv/bin/activate
    pip install pynnotator
    pynnotator install

    #And them finally:
    pynnotator -i sample.vcf
    #or
    pynnotator -i sample.vcf.gz


Options
=======

You can change settings of memory usage and number of cores in settings.py

Test
====

    pynnotator test


Others
======

    pynnotator install
    #this will download and install all libraries and data needed.
    pynnotator build
    #this will rebuild the whole dataset required from scratch (this will take about 8h hours and requires a lot of memory)

Development
===========

     git clone https://github.com/raonyguimaraes/pynnotator
     python setup.py develop
     # And have fun!

Annotations you can get from dbnfsp
===================================

Major sources:

        Variant determination:
                Gencode release 22/Ensembl 79, released March, 2015 (hg38)
        Functional predictions:
                SIFT ensembl 66, released Jan, 2015 http://provean.jcvi.org/index.php
                PROVEAN 1.1 ensembl 66, released Jan, 2015 http://provean.jcvi.org/index.php
                Polyphen-2 v2.2.2, released Feb, 2012 http://genetics.bwh.harvard.edu/pph2/
                LRT, released November, 2009 http://www.genetics.wustl.edu/jflab/lrt_query.html
                MutationTaster 2, data retrieved in 2015 http://www.mutationtaster.org/
                MutationAssessor, release 3 http://mutationassessor.org/
                FATHMM, v2.3 http://fathmm.biocompute.org.uk
                fathmm-MKL, http://fathmm.biocompute.org.uk/fathmmMKL.htm
                CADD, v1.3 http://cadd.gs.washington.edu/
                VEST, v3.0 http://karchinlab.org/apps/appVest.html
                fitCons, v1.01 http://compgen.bscb.cornell.edu/fitCons/
                DANN, https://cbcl.ics.uci.edu/public_data/DANN/
                MetaSVM and MetaLR, doi: 10.1093/hmg/ddu733
                GenoCanyon, v1.0.3 http://genocanyon.med.yale.edu/index.html
                Eigen & Eigen PC， v1.1 http://www.columbia.edu/~ii2135/eigen.html
                M-CAP, v1.0 http://bejerano.stanford.edu/MCAP/
                REVEL, https://sites.google.com/site/revelgenomics/
                MutPred, v1.2 http://mutpred.mutdb.org/
        Conservation scores:
                phyloP100way_vertebrate (hg38) http://hgdownload.soe.ucsc.edu/goldenPath/hg38/phyloP100way/
                phyloP20way_mammalian (hg38) http://hgdownload.soe.ucsc.edu/goldenPath/hg38/phyloP20way/
                phastCons100way_vertebrate (hg38) http://hgdownload.soe.ucsc.edu/goldenPath/hg38/phastCons100way/
                phastCons20way_mammalian (hg38) http://hgdownload.soe.ucsc.edu/goldenPath/hg38/phastCons20way/
                GERP++ http://mendel.stanford.edu/SidowLab/downloads/gerp/
                SiPhy http://www.broadinstitute.org/mammals/2x/siphy_hg19/
        Other variant annotation sources:
                Interpro v56 http://www.ebi.ac.uk/interpro/
                1000 Genomes project http://www.1000genomes.org/
                ESP http://evs.gs.washington.edu/EVS/
                dbSNP 147 (hg38) ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b147_GRCh38p2/VCF/All_20160527.vcf.gz
                clinvar 20161101 (hg38) ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar_20161101.vcf.gz
                ExAC v0.3 http://exac.broadinstitute.org/
                UK10K COHORT http://www.uk10k.org/studies/cohorts.html
                Ancestral alleles (hg38) ftp://ftp.ensembl.org/pub/release-84/fasta/ancestral_alleles
                Altai Neanderthal genotypes: http://cdna.eva.mpg.de/neandertal/altai/AltaiNeandertal/VCF/
                Denisova genotypes: http://www.eva.mpg.de/denisova
                RSRS http://dx.doi.org/10.1016/j.ajhg.2012.03.002
                GTEx v6 http://www.gtexportal.org/static/datasets/gtex_analysis_v6/single_tissue_eqtl_data/
        Other gene annotation sources:
                HGNC, downloaded on March 15, 2016
                Uniprot, released 2016_2
                IntAct, downloaded on March 15, 2016
                GWAS catalog, downloaded on March 15, 2015
                egenetics and GNF/Atlas expression data, downloaded from BioMart on Oct. 1, 2013
                BioGRID, version 3.4.134
                Haploinsufficiency probability data, from doi:10.1371/journal.pgen.1001154
                Recessive probability data, from DOI:10.1126/science.1215040
                Residual Variation Intolerance Score (RVIS), from http://genic-intolerance.org/
                GO, downloaded on March 15, 2016
                ConsensusPathDB, Release 31
                Essential genes, based on doi:10.1371/journal.pgen.1003484
                Mouse genes, from ftp://ftp.informatics.jax.org/pub/reports/index.html on March 15, 2016
                Zebra fish genes, from http://zfin.org/downloads/pheno.txt on March 15, 2016
                KEGG pathway, from http://www.openbioinformatics.org/gengen/tutorial_calculate_gsea.html
                BioCarta pathway, from http://www.openbioinformatics.org/gengen/tutorial_calculate_gsea.html
                GTEx v6 http://www.gtexportal.org/static/datasets/gtex_analysis_v6/rna_seq_data/
                GDI doi: 10.1073/pnas.1518646112
                LoFtool: joao.fadista@med.lu.se
                SORVA: doi: 10.1101/103218


Annotation example
==================

    cd tests
    pynnotator -i miller.vcf.gz
    grep 'Miller' ann_miller/annotation.final.vcf

    16      72050942        rs267606766     G       A       287.41  PASS    AC=1;AF=0.50;AN=2;BaseQRankSum=2.237;DB;DP=13;Dels=0.00;FS=5.119;HRun=0;HaplotypeScore=0.0000;MQ0=0;MQ=60.00;MQRankSum=0.231;QD=22.11;ReadPosRankSum=-0.077;set=variant2;EFF=NON_SYNONYMOUS_CODING(MODERATE|MISSENSE|Ggg/Agg|G152R|395|DHODH|protein_coding|CODING|ENST00000219240|4|A);CSQ=A|missense_variant|MODERATE|DHODH|ENSG00000102967|Transcript|ENST00000219240|protein_coding|4/9||||475/2065|454/1188|152/395|G/R|Ggg/Agg|||1||HGNC|2867|deleterious(0)|probably_damaging(1);SNP;HET;VARTYPE=SNP;HI_PREDICTIONS=DHODH|0.325470662|25.78%;dbsnp.RS=267606766;dbsnp.RSPOS=72050942;dbsnp.dbSNPBuildID=137;dbsnp.SSR=0;dbsnp.SAO=1;dbsnp.VP=0x050268000a05040002110100;dbsnp.GENEINFO=DHODH:1723;dbsnp.WGT=1;dbsnp.VC=SNV;dbsnp.PM;dbsnp.PMC;dbsnp.S3D;dbsnp.NSM;dbsnp.REF;dbsnp.ASP;dbsnp.VLD;dbsnp.LSD;dbsnp.OM;clinvar.RS=267606766;clinvar.RSPOS=72050942;clinvar.dbSNPBuildID=137;clinvar.SSR=0;clinvar.SAO=1;clinvar.VP=0x050268000a05040002110100;clinvar.GENEINFO=DHODH:1723;clinvar.WGT=1;clinvar.VC=SNV;clinvar.PM;clinvar.PMC;clinvar.S3D;clinvar.NSM;clinvar.REF;clinvar.ASP;clinvar.VLD;clinvar.LSD;clinvar.OM;clinvar.CLNALLE=1;clinvar.CLNHGVS=NC_000016.9:g.72050942G>A;clinvar.CLNSRC=OMIM_Allelic_Variant|UniProtKB_(protein);clinvar.CLNORIGIN=1;clinvar.CLNSRCID=126064.0004|Q02127#VAR_062414;clinvar.CLNSIG=5;clinvar.CLNDSDB=MedGen:OMIM:SNOMED_CT;clinvar.CLNDSDBID=C0265257:263750:66038001;clinvar.CLNDBN=Miller_syndrome;clinvar.CLNREVSTAT=no_criteria;clinvar.CLNACC=RCV000018294.28;esp6500.DBSNP=dbSNP_138;esp6500.EA_AC=1,8301;esp6500.AA_AC=0,3878;esp6500.TAC=1,12179;esp6500.MAF=0.012,0.0,0.0082;esp6500.GTS=AA,AG,GG;esp6500.EA_GTC=0,1,4150;esp6500.AA_GTC=0,0,1939;esp6500.GTC=0,1,6089;esp6500.DP=130;esp6500.GL=DHODH;esp6500.CP=0.8;esp6500.CG=5.8;esp6500.AA=G;esp6500.CA=.;esp6500.EXOME_CHIP=no;esp6500.GWAS_PUBMED=.;esp6500.FG=NM_001361.4:missense;esp6500.HGVS_CDNA_VAR=NM_001361.4:c.454G>A;esp6500.HGVS_PROTEIN_VAR=NM_001361.4:p.(G152R);esp6500.CDS_SIZES=NM_001361.4:1188;esp6500.GS=125;esp6500.PH=probably-damaging:1.0;esp6500.EA_AGE=.;esp6500.AA_AGE=.;esp6500.GRCh38_POSITION=16:72017043 GT:AD:DP:GQ:PL  0/1:4,9:13:99:317,0,101
    16      72055110        rs267606767     G       C       287.41  PASS    AC=1;AF=0.50;AN=2;BaseQRankSum=2.237;DB;DP=13;Dels=0.00;FS=5.119;HRun=0;HaplotypeScore=0.0000;MQ0=0;MQ=60.00;MQRankSum=0.231;QD=22.11;ReadPosRankSum=-0.077;set=variant2;EFF=NON_SYNONYMOUS_CODING(MODERATE|MISSENSE|gGc/gCc|G202A|395|DHODH|protein_coding|CODING|ENST00000219240|5|C);CSQ=C|missense_variant|MODERATE|DHODH|ENSG00000102967|Transcript|ENST00000219240|protein_coding|5/9||||626/2065|605/1188|202/395|G/A|gGc/gCc|||1||HGNC|2867|tolerated(0.18)|possibly_damaging(0.893);SNP;HET;VARTYPE=SNP;HI_PREDICTIONS=DHODH|0.325470662|25.78%;dbsnp.RS=267606767;dbsnp.RSPOS=72055110;dbsnp.dbSNPBuildID=137;dbsnp.SSR=0;dbsnp.SAO=1;dbsnp.VP=0x050268000a05040002110100;dbsnp.GENEINFO=DHODH:1723;dbsnp.WGT=1;dbsnp.VC=SNV;dbsnp.PM;dbsnp.PMC;dbsnp.S3D;dbsnp.NSM;dbsnp.REF;dbsnp.ASP;dbsnp.VLD;dbsnp.LSD;dbsnp.OM;dbsnp.TOPMED=0.999828,0.000171715,.;clinvar.RS=267606767;clinvar.RSPOS=72055110;clinvar.dbSNPBuildID=137;clinvar.SSR=0;clinvar.SAO=1;clinvar.VP=0x050268000a05040002110100;clinvar.GENEINFO=DHODH:1723;clinvar.WGT=1;clinvar.VC=SNV;clinvar.PM;clinvar.PMC;clinvar.S3D;clinvar.NSM;clinvar.REF;clinvar.ASP;clinvar.VLD;clinvar.LSD;clinvar.OM;clinvar.CLNALLE=1,2;clinvar.CLNHGVS=NC_000016.9:g.72055110G>A,NC_000016.9:g.72055110G>C;clinvar.CLNSRC=OMIM_Allelic_Variant|UniProtKB_(protein),OMIM_Allelic_Variant|UniProtKB_(protein);clinvar.CLNORIGIN=1,1;clinvar.CLNSRCID=126064.0006|Q02127#VAR_062417,126064.0005|Q02127#VAR_062416;clinvar.CLNSIG=5,5;clinvar.CLNDSDB=MedGen:OMIM:SNOMED_CT,MedGen:OMIM:SNOMED_CT;clinvar.CLNDSDBID=C0265257:263750:66038001,C0265257:263750:66038001;clinvar.CLNDBN=Miller_syndrome,Miller_syndrome;clinvar.CLNREVSTAT=no_criteria,no_criteria;clinvar.CLNACC=RCV000018296.27,RCV000018295.27   GT:AD:DP:GQ:PL       0/1:4,9:13:99:317,0,101

