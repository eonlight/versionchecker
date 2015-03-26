#! /usr/bin/env python
from setuptools import setup, find_packages
from sys import argv
import os

version = '0.0.1'
home = os.getenv('HOME')
file_path = os.path.realpath(__file__).rsplit('/', 1)[0]

class bcolors:
    FAIL = '\033[91m'
    ENF  = '\033[1m'
    OK  = '\033[92m'
    ENDC = '\033[0m'

tools_folder = '%s/.config/audits' % home
settings_filename = '%s/versionchecker_settings.py' % tools_folder

if 'install' in argv or 'develop' in argv:
    if not os.path.exists(tools_folder):
        try:
            os.mkdir(tools_folder)
        except OSError:
            print '%sNo permission to create %s.%s' % (bcolors.FAIL, tools_folder, bcolors.ENDC)
            exit(0)

    #copy template to place
    if os.path.exists(settings_filename):
        try:
            os.rename(settings_filename, '%s/versionchecker_settings-old.py' % tools_folder)
            print '%s%s moved to %s/versionchecker_settings-old.py .%s' % (bcolors.OK, settings_filename, tools_folder, bcolors.ENDC)
        except OSError:
            print '%sCould not move old settings file.%s' % (bcolors.FAIL, bcolors.ENDC)
            exit(0)



    with open('%s/versionchecker/versionchecker_settings.template.py' % file_path) as f:
        lines = f.readlines()
        with open(settings_filename, 'w') as w:
            for line in lines:
                w.write(line.replace('{{ home }}', home).replace('{{ version }}', version))
        print '%s%s created.%s' % (bcolors.OK, settings_filename, bcolors.ENDC)

setup(
    name="versionchecker",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyquery>=1.2.8',
        'requests>=2.3.0',
        'parsers>=0.0.1'
    ],
    entry_points={
        'console_scripts': [
            'versionchecker = versionchecker:main'
        ]
    },
    dependency_links=[
        "git+ssh://git@github.com:eonlight/parsers.git",
    ],
    author='Ruben de Campos',
    author_email='rcadima@gmail.com',
    description='Version Checker',
    keywords=['version', 'identifiers', 'audits'],
    long_description=""" Tool that checks a url for software and software versions and compares it to the most recent versions. """
)

print '%srun \'versionchecker --update\' to fetch the most current versions before running%s' % (bcolors.ENF, bcolors.ENDC)