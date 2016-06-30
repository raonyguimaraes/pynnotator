
import os

import unittest

test_dir = os.path.dirname(os.path.realpath(__file__))
scripts_dir = test_dir.replace('/tests', '/scripts')

import sys
sys.path.insert(0, scripts_dir)

from settings import *

# if not os.path.exists('output'):
#     os.makedirs('output')
#     #enter inside folder
# os.chdir('output')

#rm -rf cadd_vest hgmd hi_index merge output pyannotator sanity_check snpeff snpsift validator vep

class TestAnnotator(unittest.TestCase):

    def setUp(self):


        self.tests_dir = os.path.dirname(os.path.realpath(__file__))
        self.scripts_dir = self.tests_dir.replace('tests', 'scripts')

        self.sample_name = 'sample.100.vcf'
        self.sample = self.scripts_dir.replace('scripts', 'samples/sample.100.vcf')#sample_proton.vcf
        
        

    def test_001_validator(self):

        command = 'python %s/validator.py -i %s' % (self.scripts_dir, self.sample)
        print 'command running', command
        os.system(command)
        # now check if it worked!

    def test_002_sanity_check(self):
        command = 'python %s/sanity_check.py -i %s' % (self.scripts_dir, self.sample)
        os.system(command)
        #now check if it worked!
        fname = 'sanity_check/checked.vcf'
        self.assertTrue(os.path.isfile(fname))

    

    def test_003_snpeff(self):
        command = 'python %s/snpeff.py -i %s' % (self.scripts_dir, self.sample)
        os.system(command)
        #now check if it worked!
        fname = 'snpeff/snpeff.output.vcf'
        self.assertTrue(os.path.isfile(fname))

    def test_004_vep(self):
        command = 'python %s/vep.py -i %s' % (self.scripts_dir, self.sample)
        os.system(command)
        #now check if it worked!
        fname = 'vep/vep.output.sorted.vcf'
        self.assertTrue(os.path.isfile(fname))

    def test_005_hi_index(self):
        command = 'python %s/hi_index.py -i %s' % (self.scripts_dir, self.sample)
        os.system(command)
        #now check if it worked!
        fname = 'hi_index/hi_index.vcf'
        self.assertTrue(os.path.isfile(fname))

    def test_006_hgmd(self):
        command = 'python %s/hgmd.py -i %s' % (self.scripts_dir, self.sample)
        os.system(command)
        #now check if it worked!
        fname = 'hgmd/hgmd.vcf'
        self.assertTrue(os.path.isfile(fname))

    def test_007_snpsift(self):
        command = 'python %s/snpsift.py -i %s' % (self.scripts_dir, self.sample)
        os.system(command)
        #now check if it worked!
        fname = 'snpsift/snpsift.final.vcf'
        self.assertTrue(os.path.isfile(fname))

    def test_008_vcf_annotator(self):

        # command = 'python %s/vcf_annotator.py -i %s' % (self.scripts_dir, self.sample)
        command = '''python %s/vcf_annotator_parallel.py \
        -i %s \
        -n %s \
        -r 1000genomes dbsnp clinvar esp6500 \
        -a %s %s %s %s''' % (self.scripts_dir, self.sample, pynnotator_cores, genomes1k, dbsnp, clinvar, esp)

        os.system(command)
        #now check if it worked!
        fname = 'pynnotator/pynnotator.vcf'
        self.assertTrue(os.path.isfile(fname))

    def test_009_cadd_vest(self):

        command = '''python %s/cadd_vest_parallel.py \
        -i %s \
        -n %s''' % (self.scripts_dir, self.sample, cadd_vest_cores)

        os.system(command)
        #now check if it worked!
        fname = 'cadd_vest/cadd_vest.vcf'
        self.assertTrue(os.path.isfile(fname))


    def test_010_merge(self):

    #     command = 'python %s/merge.py \
    #     -i ' % (self.scripts_dir, self.sample)
        command = 'python %s/merge.py -i sanity_check/checked.vcf' % (scripts_dir)
        os.system(command)
    #     #now check if it worked!
    #     fname = 'cadd_vest/cadd_vest.vcf'
    #     self.assertTrue(os.path.isfile(fname))


    # def test_shuffle(self):
    #     # make sure the shuffled sequence does not lose any elements
    #     random.shuffle(self.seq)
    #     self.seq.sort()
    #     self.assertEqual(self.seq, range(10))

    #     # should raise an exception for an immutable sequence
    #     self.assertRaises(TypeError, random.shuffle, (1,2,3))

    # def test_choice(self):
    #     element = random.choice(self.seq)
    #     self.assertTrue(element in self.seq)

    # def test_sample(self):
    #     with self.assertRaises(ValueError):
    #         random.sample(self.seq, 20)
    #     for element in random.sample(self.seq, 5):
    #         self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()



