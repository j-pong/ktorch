
#!/usr/bin/env python3
from distutils.version import LooseVersion
import os
import pip
from setuptools import find_packages
from setuptools import setup
import sys


if LooseVersion(sys.version) < LooseVersion('3.6'):
    raise RuntimeError(
        'ktorch requires Python>=3.6, '
        'but your Python is {}'.format(sys.version))
if LooseVersion(pip.__version__) < LooseVersion('19'):
    raise RuntimeError(
        'pip>=19.0.0 is required, but your pip is {}. '
        'Try again after "pip install -U pip"'.format(pip.__version__))

requirements = {
    'install': [
        'matplotlib>=2.1.0',
        'scipy>=1.0.0',
        'numpy>=1.14.2',
        'blockdiag>=1.0',
        'setuptools>=38.5.1',
        'librosa>=0.7.0',
        'soundfile>=0.10.2',
        'inflect>=1.0.0',
        'unidecode>=1.0.22',
        'editdistance==0.5.2',
        'h5py==2.9.0',
        'pillow>=6.1.0',
        'kaldiio>=2.13.8',
        'funcsigs>=1.0.2',  # A backport of inspect.signature for python2
        'configargparse==1.1',
        'PyYAML>=5.1.2',
        'sentencepiece>=0.1.82',
    ]}
install_requires = requirements['install']

dirname = os.path.dirname(__file__)
setup(name='ktorch',
      version='0.6.3',
      url='',
      author='jpong',
      author_email='',
      description='',
      long_description=open(os.path.join(dirname, 'README.md'),
                            encoding='utf-8').read(),
      license='Apache Software License',
      packages=find_packages(include=['ktorch*']),
      install_requires=install_requires,
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Science/Research',
          'Operating System :: POSIX :: Linux',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      )