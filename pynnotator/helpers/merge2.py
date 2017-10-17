from subprocess import run
#options
#use vcfanno
#use gatk
#benchmark ?
command = 'java -Xmx15g -jar dist/GenomeAnalysisTK.jar \
-T CombineVariants \
-R /home/raony/dev/pynnotator/pynnotator/data/vep_cache/homo_sapiens/90_GRCh37/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.gz \
'

command = '/home/raony/dev/pynnotator/pynnotator/libs/gatk/gatk/gatk-launch MergeVcfs \
-I /home/raony/dev/pynnotator/pynnotator/tests/merge/snpeff.output.vcf \
-I /home/raony/dev/pynnotator/pynnotator/tests/merge/vep.output.sorted.vcf \
-O union.vcf'

run(command, shell=True)

#https://gatkforums.broadinstitute.org/gatk/discussion/7515/simple-question-about-combinevariants
# $GATK -T CombineVariants \
# -R $REFERENCE_HG38 \
# --variant:strelka vcf-strelka.vcf \
# --variant:mutect2 vcf-mutect2.vcf \
# -o vcf-combine.vcf \
# -genotypeMergeOptions PRIORITIZE \
# -priority mutect2,strelka \
# --disable_auto_index_creation_and_locking_when_reading_rods

#https://gatkforums.broadinstitute.org/gatk/discussion/53/combining-variants-from-different-files-into-one
#java -Xmx2g -jar dist/GenomeAnalysisTK.jar -T CombineVariants -R bundle/b37/human_g1k_v37.fasta -L 1:1-1,000,000 -V:omni bundle/b37/1000G_omni2.5.b37.sites.vcf -V:hm3 bundle/b37/hapmap_3.3.b37.sites.vcf -o union.vcf
