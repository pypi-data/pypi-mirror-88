# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2019-12-28 19:26
from os.path import abspath, join, dirname
from setuptools import find_packages, setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='unofficial_stog',
    version='0.0.8',
    description='Unofficial Package of AMR Parsing as Sequence-to-Graph Transduction',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sheng-z/stog',
    license='MIT',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        "Development Status :: 3 - Alpha",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        "Topic :: Text Processing :: Linguistic"
    ],
    keywords='corpus,machine-learning,NLU,NLP',
    packages=find_packages(exclude=['params', 'tests*', 'scripts']),
    include_package_data=True,
    install_requires=[
        'networkx',
        'penman==0.6.2',
        'word2number',
        'ftfy',
        'pytorch_pretrained_bert',
        'editdistance'
    ],
    python_requires='>=3.6',
)
