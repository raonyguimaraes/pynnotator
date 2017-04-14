#!/usr/bin/env python
# -*- coding: utf-8 -*-
#parallel https://code.google.com/p/pysam/issues/detail?id=105


# import pp

import multiprocessing as mp

import pysam
import argparse

from datetime import datetime
import os, shutil
# import shlex, subprocess
from pynnotator import settings

dbnfsp_header = '''##INFO=<ID=SIFT_score,Number=A,Type=String,Description="SIFT score (SIFTori). Scores range from 0 to 1. The smaller the score the more likely the SNP has damaging effect.  Multiple scores separated by ";", corresponding to Ensembl_proteinid.">
##INFO=<ID=SIFT_converted_rankscore,Number=A,Type=String,Description="SIFTori scores were first converted to SIFTnew=1-SIFTori, then ranked among all SIFTnew scores in dbNSFP. The rankscore is the ratio of  the rank the SIFTnew score over the total number of SIFTnew scores in dbNSFP.  If there are multiple scores, only the most damaging (largest) rankscore is presented. The rankscores range from 0.00963 to 0.91219.">
##INFO=<ID=SIFT_pred,Number=A,Type=String,Description="If SIFTori is smaller than 0.05 (rankscore>0.395) the corresponding nsSNV is predicted as \"D(amaging)\"; otherwise it is predicted as "T(olerated)".  Multiple predictions separated by \";\" 
##INFO=<ID=SIFT_pred,Number=A,Type=String,Description="Uniprot_acc_Polyphen2: Uniprot accession number provided by Polyphen2. Multiple entries separated by \";\".">
##INFO=<ID=Uniprot_id_Polyphen2,Number=A,Type=String,Description="Uniprot ID numbers corresponding to Uniprot_acc_Polyphen2. Multiple entries separated by \";\".">
##INFO=<ID=Uniprot_aapos_Polyphen2,Number=A,Type=String,Description="amino acid position as to Uniprot_acc_Polyphen2. Multiple entries separated by \";\".">
##INFO=<ID=Polyphen2_HDIV_score,Number=A,Type=String,Description="Polyphen2 score based on HumDiv, i.e. hdiv_prob. The score ranges from 0 to 1.  Multiple entries separated by ";", corresponding to Uniprot_acc_Polyphen2.">
##INFO=<ID=Polyphen2_HDIV_rankscore,Number=A,Type=String,Description="Polyphen2 HDIV scores were first ranked among all HDIV scores in dbNSFP. The rankscore is the ratio of the rank the score over the total number of  the scores in dbNSFP. If there are multiple scores, only the most damaging (largest)  rankscore is presented. The scores range from 0.02634 to 0.89865.">
##INFO=<ID=Polyphen2_HDIV_pred,Number=A,Type=String,Description="Polyphen2 prediction based on HumDiv, "D" ("probably damaging", HDIV score in [0.957,1] or rankscore in [0.52844,0.89865]), "P" ("possibly damaging",  HDIV score in [0.453,0.956] or rankscore in [0.34282,0.52689]) and "B" ("benign",  HDIV score in [0,0.452] or rankscore in [0.02634,0.34268]). Score cutoff for binary  classification is 0.5 for HDIV score or 0.3528 for rankscore, i.e. the prediction is  "neutral" if the HDIV score is smaller than 0.5 (rankscore is smaller than 0.3528),  and "deleterious" if the HDIV score is larger than 0.5 (rankscore is larger than  0.3528). Multiple entries are separated by ";".">
##INFO=<ID=Polyphen2_HVAR_score,Number=A,Type=String,Description="Polyphen2 score based on HumVar, i.e. hvar_prob. The score ranges from 0 to 1.  Multiple entries separated by ";", corresponding to Uniprot_acc_Polyphen2.">
##INFO=<ID=Polyphen2_HVAR_rankscore,Number=A,Type=String,Description="Polyphen2 HVAR scores were first ranked among all HVAR scores in dbNSFP. The rankscore is the ratio of the rank the score over the total number of  the scores in dbNSFP. If there are multiple scores, only the most damaging (largest)  rankscore is presented. The scores range from 0.01257 to 0.97092.">
##INFO=<ID=Polyphen2_HVAR_pred,Number=A,Type=String,Description="Polyphen2 prediction based on HumVar, "D" ("probably damaging", HVAR score in [0.909,1] or rankscore in [0.62797,0.97092]), "P" ("possibly damaging",  HVAR in [0.447,0.908] or rankscore in [0.44195,0.62727]) and "B" ("benign", HVAR  score in [0,0.446] or rankscore in [0.01257,0.44151]). Score cutoff for binary  classification is 0.5 for HVAR score or 0.45833 for rankscore, i.e. the prediction  is "neutral" if the HVAR score is smaller than 0.5 (rankscore is smaller than  0.45833), and "deleterious" if the HVAR score is larger than 0.5 (rankscore is larger  than 0.45833). Multiple entries are separated by ";". LRT_score: The original LRT two-sided p-value (LRTori), ranges from 0 to 1.">
##INFO=<ID=LRT_converted_rankscore,Number=A,Type=String,Description="LRTori scores were first converted as LRTnew=1-LRTori*0.5 if Omega<1, or LRTnew=LRTori*0.5 if Omega>=1. Then LRTnew scores were ranked among all  LRTnew scores in dbNSFP. The rankscore is the ratio of the rank over the total number  of the scores in dbNSFP. The scores range from 0.00162 to 0.84324.">
##INFO=<ID=LRT_pred,Number=A,Type=String,Description="LRT prediction, D(eleterious), N(eutral) or U(nknown), which is not solely determined by the score.  LRT_Omega: estimated nonsynonymous-to-synonymous-rate ratio (Omega, reported by LRT)">
##INFO=<ID=MutationTaster_score,Number=A,Type=String,Description="MutationTaster p-value (MTori), ranges from 0 to 1.  Multiple scores are separated by ";". Information on corresponding transcript(s) can  be found by querying http://www.mutationtaster.org/ChrPos.html">
##INFO=<ID=MutationTaster_converted_rankscore,Number=A,Type=String,Description="The MTori scores were first converted: if the prediction is "A" or "D" MTnew=MTori; if the prediction is "N" or "P", MTnew=1-MTori. Then MTnew  scores were ranked among all MTnew scores in dbNSFP. If there are multiple scores of a  SNV, only the largest MTnew was used in ranking. The rankscore is the ratio of the rank of the score over the total number of MTnew scores in dbNSFP. The scores range from 0.08979 to 0.81033.">
##INFO=<ID=MutationTaster_pred,Number=A,Type=String,Description="MutationTaster prediction, "A" ("disease_causing_automatic"), "D" ("disease_causing"), "N" ("polymorphism") or "P" ("polymorphism_automatic"). The  score cutoff between "D" and "N" is 0.5 for MTnew and 0.31713 for the rankscore. MutationTaster_model: MutationTaster prediction models. MutationTaster_AAE: MutationTaster predicted amino acid change. MutationAssessor_UniprotID: Uniprot ID number provided by MutationAssessor. MutationAssessor_variant: AA variant as to MutationAssessor_UniprotID.">
##INFO=<ID=MutationAssessor_score,Number=A,Type=String,Description="MutationAssessor functional impact combined score (MAori). The score ranges from -5.135 to 6.49 in dbNSFP. ">
##INFO=<ID=MutationAssessor_rankscore,Number=A,Type=String,Description="MAori scores were ranked among all MAori scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of MAori  scores in dbNSFP. The scores range from 0 to 1.">
##INFO=<ID=MutationAssessor_pred,Number=A,Type=String,Description="MutationAssessor's functional impact of a variant : predicted functional, i.e. high ("H") or medium ("M"), or predicted non-functional, i.e. low ("L") or neutral ("N"). The MAori score cutoffs between "H" and "M",  "M" and "L", and "L" and "N", are 3.5, 1.935 and 0.8, respectively. The rankscore cutoffs  between "H" and "M", "M" and "L", and "L" and "N", are 0.92922, 0.51944 and 0.19719,  respectively.">
##INFO=<ID=FATHMM_score,Number=A,Type=String,Description="FATHMM default score (weighted for human inherited-disease mutations with Disease Ontology) (FATHMMori). Scores range from -16.13 to 10.64. The smaller the score  the more likely the SNP has damaging effect. Multiple scores separated by ";", corresponding to Ensembl_proteinid.">
##INFO=<ID=FATHMM_converted_rankscore,Number=A,Type=String,Description="FATHMMori scores were first converted to FATHMMnew=1-(FATHMMori+16.13)/26.77, then ranked among all FATHMMnew scores in dbNSFP.  The rankscore is the ratio of the rank of the score over the total number of FATHMMnew  scores in dbNSFP. If there are multiple scores, only the most damaging (largest)  rankscore is presented. The scores range from 0 to 1.">
##INFO=<ID=FATHMM_pred,Number=A,Type=String,Description="If a FATHMMori score is <=-1.5 (or rankscore >=0.81332) the corresponding nsSNV is predicted as "D(AMAGING)"; otherwise it is predicted as "T(OLERATED)". Multiple predictions separated by ";", corresponding to Ensembl_proteinid.">
##INFO=<ID=PROVEAN_score,Number=A,Type=String,Description="PROVEAN score (PROVEANori). Scores range from -14 to 14. The smaller the score the more likely the SNP has damaging effect.  Multiple scores separated by ";", corresponding to Ensembl_proteinid.">
##INFO=<ID=PROVEAN_converted_rankscore,Number=A,Type=String,Description="PROVEANori were first converted to PROVEANnew=1-(PROVEANori+14)/28, then ranked among all PROVEANnew scores in dbNSFP. The rankscore is the ratio of  the rank the PROVEANnew score over the total number of PROVEANnew scores in dbNSFP.  If there are multiple scores, only the most damaging (largest) rankscore is presented. The scores range from 0 to 1.">
##INFO=<ID=PROVEAN_pred,Number=A,Type=String,Description="If PROVEANori <= -2.5 (rankscore>=0.543) the corresponding nsSNV is predicted as "D(amaging)"; otherwise it is predicted as "N(eutral)".  Multiple predictions separated by ";", corresponding to Ensembl_proteinid. Transcript_id_VEST3: Transcript id provided by VEST3. Transcript_var_VEST3: amino acid change as to Transcript_id_VEST3.">
##INFO=<ID=VEST3_score,Number=A,Type=String,Description="VEST 3.0 score. Score ranges from 0 to 1. The larger the score the more likely the mutation may cause functional change.  Multiple scores separated by ";", corresponding to Transcript_id_VEST3. Please note this score is free for non-commercial use. For more details please refer to  http://wiki.chasmsoftware.org/index.php/SoftwareLicense. Commercial users should contact  the Johns Hopkins Technology Transfer office.">
##INFO=<ID=VEST3_rankscore,Number=A,Type=String,Description="VEST3 scores were ranked among all VEST3 scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of VEST3  scores in dbNSFP. In case there are multiple scores for the same variant, the largest  score (most damaging) is presented. The scores range from 0 to 1.  Please note VEST score is free for non-commercial use. For more details please refer to  http://wiki.chasmsoftware.org/index.php/SoftwareLicense. Commercial users should contact  the Johns Hopkins Technology Transfer office.">
##INFO=<ID=MetaSVM_score,Number=A,Type=String,Description="Our support vector machine (SVM) based ensemble prediction score, which incorporated 10 scores (SIFT, PolyPhen-2 HDIV, PolyPhen-2 HVAR, GERP++, MutationTaster,  Mutation Assessor, FATHMM, LRT, SiPhy, PhyloP) and the maximum frequency observed in  the 1000 genomes populations. Larger value means the SNV is more likely to be damaging.  Scores range from -2 to 3 in dbNSFP.">
##INFO=<ID=MetaSVM_rankscore,Number=A,Type=String,Description="MetaSVM scores were ranked among all MetaSVM scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of MetaSVM  scores in dbNSFP. The scores range from 0 to 1.">
##INFO=<ID=MetaSVM_pred,Number=A,Type=String,Description="Prediction of our SVM based ensemble prediction score,"T(olerated)" or "D(amaging)". The score cutoff between "D" and "T" is 0. The rankscore cutoff between "D" and "T" is 0.82268.">
##INFO=<ID=MetaLR_score,Number=A,Type=String,Description="Our logistic regression (LR) based ensemble prediction score, which incorporated 10 scores (SIFT, PolyPhen-2 HDIV, PolyPhen-2 HVAR, GERP++, MutationTaster,  Mutation Assessor, FATHMM, LRT, SiPhy, PhyloP) and the maximum frequency observed in  the 1000 genomes populations. Larger value means the SNV is more likely to be damaging.  Scores range from 0 to 1.">
##INFO=<ID=MetaLR_rankscore,Number=A,Type=String,Description="MetaLR scores were ranked among all MetaLR scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of MetaLR scores in dbNSFP.  The scores range from 0 to 1.">
##INFO=<ID=MetaLR_pred,Number=A,Type=String,Description="Prediction of our MetaLR based ensemble prediction score,"T(olerated)" or "D(amaging)". The score cutoff between "D" and "T" is 0.5. The rankscore cutoff between  "D" and "T" is 0.81113.">
##INFO=<ID=Reliability_index,Number=A,Type=String,Description="Number of observed component scores (except the maximum frequency in the 1000 genomes populations) for MetaSVM and MetaLR. Ranges from 1 to 10. As MetaSVM  and MetaLR scores are calculated based on imputed data, the less missing component  scores, the higher the reliability of the scores and predictions. ">
##INFO=<ID=M,Number=A,Type=String,Description="AP_score: M-CAP score (details in DOI: 10.1038/ng.3703). Scores range from 0 to 1. The larger the score the more likely the SNP has damaging effect. ">
##INFO=<ID=M,Number=A,Type=String,Description="AP_rankscore: M-CAP scores were ranked among all M-CAP scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of M-CAP scores in dbNSFP.">
##INFO=<ID=M,Number=A,Type=String,Description="AP_pred: Prediction of M-CAP score based on the authors' recommendation, "T(olerated)" or "D(amaging)". The score cutoff between "D" and "T" is 0.025.">
##INFO=<ID=REVEL_score,Number=A,Type=String,Description="REVEL is an ensemble score based on 13 individual scores for predicting the pathogenicity of missense variants. Scores range from 0 to 1. The larger the score the more  likely the SNP has damaging effect. "REVEL scores are freely available for non-commercial use.   For other uses, please contact Weiva Sieh" (weiva.sieh@mssm.edu)">
##INFO=<ID=REVEL_rankscore,Number=A,Type=String,Description="REVEL scores were ranked among all REVEL scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of REVEL scores in dbNSFP.">
##INFO=<ID=MutPred_score,Number=A,Type=String,Description="General MutPred score. Scores range from 0 to 1. The larger the score the more likely the SNP has damaging effect.">
##INFO=<ID=MutPred_rankscore,Number=A,Type=String,Description="MutPred scores were ranked among all MutPred scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of MutPred scores in dbNSFP. MutPred_protID: UniProt accession or Ensembl transcript ID used for MutPred_score calculation. MutPred_AAchange: Amino acid change used for MutPred_score calculation.">
##INFO=<ID=MutPred_Top5features,Number=A,Type=String,Description="Top 5 features (molecular mechanisms of disease) as predicted by MutPred with p values. MutPred_score > 0.5 and p < 0.05 are referred to as actionable hypotheses. MutPred_score > 0.75 and p < 0.05 are referred to as confident hypotheses. MutPred_score > 0.75 and p < 0.01 are referred to as very confident hypotheses.">
##INFO=<ID=CADD_raw,Number=A,Type=String,Description="CADD raw score for functional prediction of a SNP. Please refer to Kircher et al. (2014) Nature Genetics 46(3):310-5 for details. The larger the score the more likely the SNP has damaging effect. Scores range from -7.535037 to 35.788538 in dbNSFP.  Please note the following copyright statement for CADD:  "CADD scores (http://cadd.gs.washington.edu/) are Copyright 2013 University of  Washington and Hudson-Alpha Institute for Biotechnology (all rights reserved) but are  freely available for all academic, non-commercial applications. For commercial  licensing information contact Jennifer McCullar (mccullaj@uw.edu)."">
##INFO=<ID=CADD_raw_rankscore,Number=A,Type=String,Description="CADD raw scores were ranked among all CADD raw scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of CADD  raw scores in dbNSFP. Please note the following copyright statement for CADD: "CADD  scores (http://cadd.gs.washington.edu/) are Copyright 2013 University of Washington  and Hudson-Alpha Institute for Biotechnology (all rights reserved) but are freely  available for all academic, non-commercial applications. For commercial licensing  information contact Jennifer McCullar (mccullaj@uw.edu)."">
##INFO=<ID=CADD_phred,Number=A,Type=String,Description="CADD phred-like score. This is phred-like rank score based on whole genome CADD raw scores. Please refer to Kircher et al. (2014) Nature Genetics 46(3):310-5  for details. The larger the score the more likely the SNP has damaging effect.  Please note the following copyright statement for CADD: "CADD scores  (http://cadd.gs.washington.edu/) are Copyright 2013 University of Washington and  Hudson-Alpha Institute for Biotechnology (all rights reserved) but are freely  available for all academic, non-commercial applications. For commercial licensing  information contact Jennifer McCullar (mccullaj@uw.edu)."">
##INFO=<ID=DANN_score,Number=A,Type=String,Description="DANN is a functional prediction score retrained based on the training data of CADD using deep neural network. Scores range from 0 to 1. A larger number indicate  a higher probability to be damaging. More information of this score can be found in doi: 10.1093/bioinformatics/btu703. For commercial application of DANN, please contact  Daniel Quang (dxquang@uci.edu)">
##INFO=<ID=DANN_rankscore,Number=A,Type=String,Description="DANN scores were ranked among all DANN scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number of DANN scores in dbNSFP.">
##INFO=<ID=fathmm,Number=A,Type=String,Description="KL_coding_score: fathmm-MKL p-values. Scores range from 0 to 1. SNVs with scores >0.5 are predicted to be deleterious, and those <0.5 are predicted to be neutral or benign.  Scores close to 0 or 1 are with the highest-confidence. Coding scores are trained using 10 groups of features. More details of the score can be found in  doi: 10.1093/bioinformatics/btv009.">
##INFO=<ID=fathmm,Number=A,Type=String,Description="KL_coding_rankscore: fathmm-MKL coding scores were ranked among all fathmm-MKL coding scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number  of fathmm-MKL coding scores in dbNSFP.">
##INFO=<ID=fathmm,Number=A,Type=String,Description="KL_coding_pred: If a fathmm-MKL_coding_score is >0.5 (or rankscore >0.28317)  the corresponding nsSNV is predicted as "D(AMAGING)"; otherwise it is predicted as "N(EUTRAL)".">
##INFO=<ID=fathmm,Number=A,Type=String,Description="KL_coding_group: the groups of features (labeled A-J) used to obtained the score. More details can be found in doi: 10.1093/bioinformatics/btv009.">
##INFO=<ID=Eigen_coding_or_noncoding,Number=A,Type=String,Description="Whether Eigen-raw and Eigen-phred scores are based on coding model or noncoding model.">
##INFO=<ID=Eigen,Number=A,Type=String,Description="aw: Eigen score for coding SNVs. A functional prediction score based on conservation, allele frequencies, and deleteriousness prediction using an unsupervised learning method  (doi: 10.1038/ng.3477).  Eigen-phred: Eigen score in phred scale.">
##INFO=<ID=Eigen,Number=A,Type=String,Description="C-raw: Eigen PC score for genome-wide SNVs. A functional prediction score based on conservation, allele frequencies, deleteriousness prediction (for missense SNVs) and epigenomic signals (for synonymous and non-coding SNVs) using an unsupervised learning  method (doi: 10.1038/ng.3477).  Eigen-PC-phred: Eigen PC score in phred scale.">
##INFO=<ID=Eigen,Number=A,Type=String,Description="C-raw_rankscore: Eigen-PC-raw scores were ranked among all Eigen-PC-raw scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number  of Eigen-PC-raw scores in dbNSFP.">
##INFO=<ID=GenoCanyon_score,Number=A,Type=String,Description="A functional prediction score based on conservation and biochemical annotations using an unsupervised statistical learning. (doi:10.1038/srep10576)">
##INFO=<ID=GenoCanyon_score_rankscore,Number=A,Type=String,Description="GenoCanyon_score scores were ranked among all integrated fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number  of GenoCanyon_score scores in dbNSFP.">
##INFO=<ID=integrated_fitCons_score,Number=A,Type=String,Description="fitCons score predicts the fraction of genomic positions belonging to a specific function class (defined by epigenomic "fingerprint") that are under selective  pressure. Scores range from 0 to 1, with a larger score indicating a higher proportion of  nucleic sites of the functional class the genomic position belong to are under selective  pressure, therefore more likely to be functional important. Integrated (i6) scores are integrated across three cell types (GM12878, H1-hESC and HUVEC). More details can be found in doi:10.1038/ng.3196.">
##INFO=<ID=integrated_fitCons_rankscore,Number=A,Type=String,Description="integrated fitCons scores were ranked among all integrated fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number  of integrated fitCons scores in dbNSFP.">
##INFO=<ID=integrated_confidence_value,Number=A,Type=String,Description="0 - highly significant scores (approx. p<.003); 1 - significant scores (approx. p<.05); 2 - informative scores (approx. p<.25); 3 - other scores (approx. p>=.25).">
##INFO=<ID=GM12878_fitCons_score,Number=A,Type=String,Description="fitCons score predicts the fraction of genomic positions belonging to a specific function class (defined by epigenomic "fingerprint") that are under selective  pressure. Scores range from 0 to 1, with a larger score indicating a higher proportion of  nucleic sites of the functional class the genomic position belong to are under selective  pressure, therefore more likely to be functional important. GM12878 fitCons scores are based on cell type GM12878. More details can be found in doi:10.1038/ng.3196.">
##INFO=<ID=GM12878_fitCons_rankscore,Number=A,Type=String,Description="GM12878 fitCons scores were ranked among all GM12878 fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number  of GM12878 fitCons scores in dbNSFP.">
##INFO=<ID=GM12878_confidence_value,Number=A,Type=String,Description="0 - highly significant scores (approx. p<.003); 1 - significant scores (approx. p<.05); 2 - informative scores (approx. p<.25); 3 - other scores (approx. p>=.25).">
##INFO=<ID=H1,Number=A,Type=String,Description="ESC_fitCons_score: fitCons score predicts the fraction of genomic positions belonging to a specific function class (defined by epigenomic "fingerprint") that are under selective  pressure. Scores range from 0 to 1, with a larger score indicating a higher proportion of  nucleic sites of the functional class the genomic position belong to are under selective  pressure, therefore more likely to be functional important. GM12878 fitCons scores are based on cell type H1-hESC. More details can be found in doi:10.1038/ng.3196.">
##INFO=<ID=H1,Number=A,Type=String,Description="ESC_fitCons_rankscore: H1-hESC fitCons scores were ranked among all H1-hESC fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number  of H1-hESC fitCons scores in dbNSFP.">
##INFO=<ID=H1,Number=A,Type=String,Description="ESC_confidence_value: 0 - highly significant scores (approx. p<.003); 1 - significant scores (approx. p<.05); 2 - informative scores (approx. p<.25); 3 - other scores (approx. p>=.25).">
##INFO=<ID=HUVEC_fitCons_score,Number=A,Type=String,Description="fitCons score predicts the fraction of genomic positions belonging to a specific function class (defined by epigenomic "fingerprint") that are under selective  pressure. Scores range from 0 to 1, with a larger score indicating a higher proportion of  nucleic sites of the functional class the genomic position belong to are under selective  pressure, therefore more likely to be functional important. GM12878 fitCons scores are based on cell type HUVEC. More details can be found in doi:10.1038/ng.3196.">
##INFO=<ID=HUVEC_fitCons_rankscore,Number=A,Type=String,Description="HUVEC fitCons scores were ranked among all HUVEC fitCons scores in dbNSFP. The rankscore is the ratio of the rank of the score over the total number  of HUVEC fitCons scores in dbNSFP.">
##INFO=<ID=HUVEC_confidence_value,Number=A,Type=String,Description="0 - highly significant scores (approx. p<.003); 1 - significant scores (approx. p<.05); 2 - informative scores (approx. p<.25); 3 - other scores (approx. p>=.25).">
##INFO=<ID=clinvar_rs,Number=A,Type=String,Description="rs number from the clinvar data set">
##INFO=<ID=clinvar_clnsig,Number=A,Type=String,Description="clinical significance as to the clinvar data set. 0 - unknown, 1 - untested, 2 - Benign, 3 - Likely benign, 4 - Likely pathogenic, 5 - Pathogenic, 6 - drug response, 7 - histocompatibility. A negative score means the the score is for the ref allele">
##INFO=<ID=clinvar_trait,Number=A,Type=String,Description="the trait/disease the clinvar_clnsig referring to">
##INFO=<ID=clinvar_golden_stars,Number=A,Type=String,Description="ClinVar Review Status summary. 0 - no assertion criteria provided, 1 - criteria provided, single submitter, 2 - criteria provided, multiple submitters, no conflicts, 3 - reviewed by expert panel, 4 - practice guideline">
'''

# cores = int(args.cores)
# prefix = 'func_pred'
# if not os.path.exists(prefix):
#     os.makedirs(prefix)

class FUNC_PRED_Annotator(object):

    def __init__(self, vcf_file=None, cores=None):
        
        self.vcf_file = vcf_file

        # print('self.resources', self.resources)
        self.cores = int(cores)

        self.filename = os.path.splitext(os.path.basename(str(vcf_file)))[0]
        #create folder validator if it doesn't exists
        if not os.path.exists('func_pred'):
            os.makedirs('func_pred')

    def run(self):

        tstart = datetime.now()

        print(tstart, 'Starting func pred annotator: ', self.vcf_file)
        
        # std = self.annotator()

        self.splitvcf(self.vcf_file)

        pool = mp.Pool()
        pool.map(self.annotate, range(1,self.cores+1))
        # pool.close()
        # pool.join()

        prefix = 'func_pred'
        # # Define your jobs
        # jobs = []
        final_parts = []
        for n in range(0,self.cores):
            index = n+1
            final_file = 'func_pred/func_pred.%s.vcf' % (index)
            final_parts.append(final_file)
        
        command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/func_pred.vcf' % (prefix)
        std = os.system(command)

        tend = datetime.now()
        annotation_time =  tend - tstart
        print(tend, 'Finished func pred, it took: ', annotation_time)


    def partition(self, lst, n):
            division = len(lst) / float(n)
            return [ lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n) ]

    def splitvcf(self, vcffile):
        # print('split file', vcffile)
        # print 'numero de cores', cores
        prefix = 'func_pred'
        vcf_reader = open('%s' % (vcffile))
        header_writer = open('%s/header.vcf' % (prefix), 'w')
        body_writer = open('%s/body.vcf' % (prefix), 'w')
        
        count_lines = 0
        for line in vcf_reader:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    header_writer.writelines(dbnfsp_header)
                header_writer.writelines(line)
            else:
                body_writer.writelines(line)
        header_writer.close()
        body_writer.close()
        
        vcf_reader = open('%s/body.vcf' % (prefix))

        groups = self.partition(list(vcf_reader.readlines()), self.cores)
        for c, group in enumerate(groups):
            # print 'group', len(group)
            # print 'c', c
            part = c + 1
            part_writer = open('%s/part.%s.vcf' % (prefix, part), 'w')
            for line in group:
                part_writer.writelines(line)
            part_writer.close()

    #convert and annotate the vcf file to snpeff
    def annotate(self, out_prefix):
        #print 'Hello'
        #print self.dbnfsp_reader
        #header is at:
        
        # 24    SIFT_score: SIFT score (SIFTori).
        # 105 HUVEC_confidence_value: 0 - highly significant scores (approx. p<.003); 1 - significant scores

        #188   clinvar_rs: rs number from the clinvar data set
        #191 clinvar_golden_stars: ClinVar Review Status summary.
        
        func_pred_start = 23
        func_pred_end = 105
        
        clinvar_start = 187
        clinvar_end = 191


        # print 'input',vcffile, out_prefix, dbnsfp 
        dbnfsp_reader = pysam.Tabixfile(settings.dbnsfp, 'r')
        
        # print('header')
        for item in dbnfsp_reader.header:
            header = item.decode('utf-8').strip().split('\t')

        # header = dbnfsp_reader.header.next().strip().split('\t')

        vcffile = 'func_pred/part.%s.vcf' % (out_prefix)

        vcf_reader = open('%s' % (vcffile))
        vcf_writer = open('func_pred/func_pred.%s.vcf' % (out_prefix), 'w')
        
        for line in vcf_reader:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    vcf_writer.writelines(dbnfsp_header)
                vcf_writer.writelines(line)
            else:
                variant = line.split('\t')
                variant[0] = variant[0].replace('chr', '')
                index = '%s-%s' % (variant[0], variant[1])
                #print index
                try:
                    records = dbnfsp_reader.fetch(variant[0], int(variant[1])-1, int(variant[1]))
                except:
                    records = []
                    
                for record in records:
                    ann = record.strip().split('\t')

                    ispresent = False
                    if variant[3] == ann[2]:
                        alts = variant[4].split(',')
                        alts_ann = ann[3].split(',')
                        #compare ALT
                        for alt in alts:
                            if alt in alts_ann:
                                ispresent = True

                    if ispresent:
                        new_ann = []
                        
                        for k, item in enumerate(header[func_pred_start:func_pred_end]):
                            idx = k+func_pred_start
                            if ann[idx] != '.':
                                new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|')))

                        for k, item in enumerate(header[clinvar_start:clinvar_end]):
                            idx = k+clinvar_start
                            if ann[idx] != '.':
                                new_ann.append('dbNSFP_%s=%s' % (item, ann[idx].replace(';', '|').replace(' ', '_')))

                        variant[7] = '%s;%s' % (variant[7], ";".join(new_ann))
                vcf_writer.writelines("\t".join(variant))


if  __name__ == '__main__' :
    
    
    parser = argparse.ArgumentParser(description='Annotate a VCF File with DbNSFP.')

    parser.add_argument('-i', dest='vcf_file', required=True, metavar='example.vcf', help='a VCF file to be annotated')

    parser.add_argument('-n', dest='cores', required=True, metavar='4', help='number of cores to use')

    args = parser.parse_args()

    func_pred = FUNC_PRED_Annotator(args.vcf_file, args.cores)
    func_pred.run()



# def annotate(vcffile, index, dbnsfp):
#     print 'vcf', vcffile, index
#     # filename = os.path.splitext(os.path.basename(str(vcffile)))[0]
#     dbnfsp_reader = pysam.Tabixfile(dbnsfp)

# splitvcf(args.vcffile)

# # job_server = pp.Server()
# prefix = 'func_pred'
# # Define your jobs
# jobs = []
# final_parts = []
# for n in range(0,cores):
#     index = n+1
#     part = '%s/part.%s.vcf' % (prefix, index)
    
#     job = Process(target=annotate, args=(part, index, args.dbnsfp))
#     final_file = 'func_pred/func_pred.%s.vcf' % (index)
#     final_parts.append(final_file)
#     jobs.append(job)


# for job in jobs:
#     job.start()

# for job in jobs:
#     job.join()

# command = 'cat %s/header.vcf ' % (prefix) + " ".join(final_parts) + '> %s/func_pred.vcf' % (prefix)
# os.system(command)
# #merge all files 
