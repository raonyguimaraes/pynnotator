from setuptools import setup

setup(
      name='pynnotator',
      version='1.9.2',
      description='A Python Annotation Framework for VCFs using multiple tools (Ex. VEP, SnpEff and SnpSift) and databases (Ex. 1000genomes, dbSNP and dbnfsp) .',
      url='http://github.com/raonyguimaraes/pynnotator',
      author='Raony Guimaraes',
      author_email='raony@torchmed.com',
      classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: BSD License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
      keywords='genome exome annotation rare diseases',
      license='BSD-3',
      packages=['pynnotator', 'pynnotator.helpers', 'pynnotator.tests'],
      install_requires=[
          'wheel',
          'pysam',
          'cython',
          'distro',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      #scripts=['bin/pynnotator'],
      entry_points={  # Optional
              'console_scripts': [
                  'pynnotator=pynnotator.main:main',
              ],
      },
      include_package_data=True,
      zip_safe=False)
