from setuptools import setup

setup(
      name='pynnotator',
      version='3.0',
      description='A Python Annotation Framework for VCFs using VEP and modern annotation databases.',
      url='http://github.com/raonyguimaraes/pynnotator',
      author='Raony Guimaraes',
      author_email='raony@torchmed.com',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
      keywords='genome exome annotation rare diseases vep variant effect predictor',
      license='BSD-3',
      packages=['pynnotator', 'pynnotator.helpers', 'pynnotator.tests'],
      install_requires=[
          'wheel',
          'cyvcf2',
          'pysam',
          'pyyaml',
          'distro',
      ],
      extras_require={
          'export': ['pandas', 'pyarrow'],
          'dev': ['pytest'],
      },
      entry_points={
              'console_scripts': [
                  'pynnotator=pynnotator.main:main',
              ],
      },
      include_package_data=True,
      zip_safe=False)
