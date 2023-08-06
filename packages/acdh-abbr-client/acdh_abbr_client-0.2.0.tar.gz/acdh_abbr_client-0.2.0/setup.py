#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'requests==2.25.0',
]

setup_requirements = []

test_requirements = []

setup(
    author="Peter Andorfer",
    author_email='peter.andorfer@oeaw.ac.at',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="A python client to interact with abbr.acdh.oeaw.ac.at",
    entry_points={
        'console_scripts': [
            'acdh_abbr_client=acdh_abbr_client.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='acdh_abbr_client',
    name='acdh_abbr_client',
    packages=find_packages(include=['acdh_abbr_client', 'acdh_abbr_client.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/acdh-oeaw/acdh_abbr_client',
    version='0.2.0',
    zip_safe=False,
)
