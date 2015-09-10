#! /usr/bin/env python
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup, find_packages
from sys import argv
import os

version = '0.2.1'
home = os.getenv('HOME')
file_path = os.path.realpath(__file__).rsplit('/', 1)[0]

tools_folder = '%s/.config/audits' % home
settings_filename = '%s/versionchecker_settings.py' % tools_folder

class bcolors:
    FAIL = '\033[91m'
    ENF  = '\033[1m'
    OK  = '\033[92m'
    ENDC = '\033[0m'

def common(debug=False):
    if not os.path.exists(tools_folder):
        try:
            os.makedirs(tools_folder)
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
                w.write(line.replace('{{ home }}', home).replace('{{ version }}', version).replace('{{ debug }}', 'True' if debug else 'False'))
        print '%s%s created.%s' % (bcolors.OK, settings_filename, bcolors.ENDC)

class PreInstall(install):
    def run(self):
        common(False)
        install.run(self)
        print '%srun \'versionchecker --update\' to fetch the most current versions before running%s' % (bcolors.ENF, bcolors.ENDC)

class PreDevelop(develop):
    def run(self):
        common(True)
        develop.run(self)
        print '%srun \'versionchecker --update\' to fetch the most current versions before running%s' % (bcolors.ENF, bcolors.ENDC)

setup(
    name="versionchecker",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyquery>=1.2.8',
        'requests>=2.3.0',
        'parsers>=0.1.0'
    ],
    entry_points={
        'console_scripts': [
            'versionchecker = versionchecker:main'
        ]
    },
    dependency_links=[
        "https://github.com/eonlight/parsers/tarball/master#egg=parsers-v0.1.0",
    ],
    cmdclass={
        'install': PreInstall,
        'develop': PreDevelop,
    },
    author='Ruben de Campos',
    author_email='rcadima@gmail.com',
    description='Version Checker',
    keywords=['version', 'identifiers', 'audits'],
    long_description="""
        Checks a URL for which software the server is running and its versions.
        Gets the latest versions and reports the ones that are outdated.
    """
)
