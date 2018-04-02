import os
from subprocess import run
from pynnotator import settings
import shutil

shutil.rmtree(settings.vcf_validator_dir)
os.makedirs(settings.vcf_validator_dir)
os.chdir(settings.vcf_validator_dir)

command = 'wget https://github.com/EBIvariation/vcf-validator/releases/download/v0.7/vcf_validator'
run(command,shell=True)
command = 'chmod +x vcf_validator'
run(command,shell=True)