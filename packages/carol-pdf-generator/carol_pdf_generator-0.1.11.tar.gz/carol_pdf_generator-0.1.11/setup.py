#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'python-datauri==0.2.9',
    'reportbro-fpdf==1.7.10',
    'opencv-contrib-python-headless',
    'scikit-image',
    'numpy',
    'imutils',
    'pypdf2'
]

setup_requirements = []

test_requirements = []

setup(
    author="Giovani Zamboni",
    author_email='giovani.zamboni@totvs.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A library to create PDF Files from a set of "
                "image files/base64 data",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='carol_pdf_generator',
    name='carol_pdf_generator',
    packages=find_packages(
        include=[
            'carol_pdf_generator',
            'carol_pdf_generator.*'
        ]
    ),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gzamboni/carol_pdf_generator',
    version='0.1.11',
    zip_safe=False,
)
