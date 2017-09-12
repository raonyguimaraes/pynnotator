from subprocess import run

# test snpeff annotation
command = 'python ../helpers/snpeff.py -i sample.1000.vcf'
run(command, shell=True)
