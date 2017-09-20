from subprocess import run
import os
os.chdir('/projects/pynnotator/pynnotator/data/dbnsfp/')
#test snpeff annotation
vcf_file = '/projects/pynnotator/pynnotator/tests/examples/NA12878.recessive.vcf.gz'
# vcf_file = '/projects/pynnotator/pynnotator/tests/sample.1000.vcf'
#dbnfsp
command = 'java -Xmx5g search_dbNSFP35a -i %s -v hg19 -o dbnfsp.out' % (vcf_file)
print(command)
run(command, shell=True)
#snpeff
command = 'java -Xmx5g -jar /projects/pynnotator/pynnotator/libs/snpeff/snpEff/SnpSift.jar dbnsfp -v -db /projects/pynnotator/pynnotator/data/dbnsfp/dbNSFP3.5a.txt.gz %s > dbnfsp.snpeff.out.vcf' % (vcf_file)
# run(command, shell=True)
#custom
# command = ''
# run(command, shell=True)
