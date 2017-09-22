from subprocess import run
import os
from datetime import datetime


# code to speed test

os.chdir('../../data/dbnsfp/')
#test snpeff annotation
vcf_file = '../../tests/examples/miller.sorted.vcf'
vcf_file = '../../tests/sample.1000.vcf.gz'
#dbnfsp
tstart = datetime.now()
command = 'java -Xmx5g search_dbNSFP35a -i %s -v hg19 -o dbnfsp.out' % (vcf_file)
# print(command)
# run(command, shell=True)
tend = datetime.now()
execution = tend - tstart
# print(execution)
#snpeff
tstart = datetime.now()
# command = 'java -Xmx5g -jar ../../libs/snpeff/snpEff/SnpSift.jar dbnsfp -v -db ../../data/dbnsfp/dbNSFP3.5a.txt.gz %s > dbnfsp.snpeff.out.vcf' % (vcf_file)
command = 'java -Xmx5g -jar ../../libs/snpeff/snpEff/SnpSift.jar dbnsfp -v -db ../../data/dbnsfp/dbNSFP2.9.txt.gz %s > dbnfsp.snpeff.out.vcf' % (vcf_file)
# run(command, shell=True)
tend = datetime.now()
execution = tend - tstart
# print(execution)
#bcftools
command = 'bcftools '
run(command, shell=True)
