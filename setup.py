from setuptools import setup

setup(name='pynnotator',
      version='0.1.1',
      description='A Python Annotation Framework for VCFs using multiple tools (Ex. VEP, SnpEff and SnpSift) and databases (Ex. 1000genomes, dbSNP and dbnfsp) .',
      url='http://github.com/raonyguimaraes/pynnotator',
      author='Raony Guimaraes',
      author_email='raony@torchmed.com',
      license='MIT',
      packages=['pynnotator'],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/pynnotator'],
      include_package_data=True,
      zip_safe=False)