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
