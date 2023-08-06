# -*- coding: utf-8 -*-

import setuptools


with open('README.md', 'r') as rm:
    long_desc = rm.read()


setuptools.setup(
    name='hipopayflake',
    version='1.1.6',
    author='Qingxu Kuang',
    author_email='asahikuang@gmail.com',
    url='https://hipopay.com',
    description=u'Distributed system ID generator based on snowflake.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ]
)
