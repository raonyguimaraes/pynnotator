from subprocess import run

# test snpeff annotation
path = '../libs/htslib/htslib-1.5'
command = '%s/bgzip sample.1000.vcf -c > sample.1000.vcf.gz' % (path)
run(command, shell=True)
command = '%s/tabix -p vcf sample.1000.vcf.gz' % (path)
run(command, shell=True)
