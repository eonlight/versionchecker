from sys import path, stderr
from datetime import datetime
import os

version = '0.1.0'

tools_name = 'versionchecker'
tools_folder = '%s/.config/audits' % os.getenv("HOME")
output_folder = '%s/output' % tools_folder

# if only module name is set, it will search for a function with the name of the software
versions_info = {
    'apache':    {
        'url': 'http://httpd.apache.org/',
        'module': 'versionchecker.software_functions',
        'function': 'apache'
    },
    'nginx':     {
        'url': 'http://nginx.org/en/CHANGES',
        'module': 'versionchecker.software_functions',
        'function': 'nginx'
    },
    'microsoft-iis':       {
        'url': 'http://www.iis.net/learn',
        'module': 'versionchecker.software_functions',
        'function': 'iis'
    },
    'joomla':    {
        'url': 'http://www.joomla.org/download.html',
        'module': 'versionchecker.software_functions',
        'function': 'joomla'
    },
    'wordpress': {
        'url': 'http://wordpress.org/download/',
        'module': 'versionchecker.software_functions',
        'function': 'wordpress'
    },
    'php':       {
        'url': 'http://www.php.net/',
        'module': 'versionchecker.software_functions',
        'function': 'php'
    },
    'openssl':   {
        'url': 'http://www.openssl.org/source/',
        'module': 'versionchecker.software_functions',
        'function': 'openssl'
    },
    'liferay':   {
        'url': 'http://www.liferay.com/community/releases',
        'module': 'versionchecker.software_functions',
        'function': 'liferay'
    },
    'ipboard':   {
        'url': 'http://en.wikipedia.org/wiki/Invision_Power_Board',
        'module': 'versionchecker.software_functions',
        'function': 'ipboard'
    },
    'vbulletin': {
        'url': 'http://www.vbulletin.com/forum/external?type=rss2&nodeid=28',
        'module': 'versionchecker.software_functions',
        'function': 'vbulletin'
    },
    'mysql':     {
        'url': 'http://dev.mysql.com/downloads/',
        'module': 'versionchecker.software_functions',
        'function': 'mysql'
    },
    'lighttpd':  {
        'url': 'http://www.lighttpd.net/download/',
        'module': 'versionchecker.software_functions',
        'function': 'lighttpd'
    },
    'postgre':   {
        'url': 'http://www.postgresql.org/',
        'module': 'versionchecker.software_functions',
        'function': 'postgre'
    },
    'drupal':    {
        'url': 'https://www.drupal.org/download',
        'module': 'versionchecker.software_functions',
        'function': 'drupal'
    },
    'tomcat':    {
        'url': 'http://tomcat.apache.org/',
        'module': 'versionchecker.software_functions',
        'function': 'tomcat'
    },
}

version_checking_tools = {
    'whatweb': {
        'module': 'parsers',
        'class': 'WhatWebParser',
    },
    'nmap': {
        'module': 'parsers',
        'class': 'NMapParser'
    }
}

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0 VersionChecker/%s' % version

DEBUG = False

""" import local settings """
path.append(tools_folder)
try:
    import versionchecker_settings

    if hasattr(versionchecker_settings, 'DEBUG'): DEBUG = versionchecker_settings.DEBUG or DEBUG

    if hasattr(versionchecker_settings, 'tools_name'): tools_name = versionchecker_settings.tools_name or tools_name
    if hasattr(versionchecker_settings, 'tools_folder'): tools_folder = versionchecker_settings.tools_folder or tools_folder
    if hasattr(versionchecker_settings, 'output_folder'): output_folder = versionchecker_settings.output_folder or output_folder

    # other options
    if hasattr(versionchecker_settings, 'user_agent'): user_agent = versionchecker_settings.user_agent or user_agent

    # updates versions parsers functions
    if hasattr(versionchecker_settings, 'versions_info'):
        for key in versionchecker_settings.versions_info:
            versions_info[key] = versionchecker_settings.versions_info[key]

    if hasattr(versionchecker_settings, 'version_checking_tools'): version_checking_tools = versionchecker_settings.version_checking_tools or version_checking_tools

except ImportError:
    stderr.write('%s - settings - versionchecker local settings not found...\n' % str(datetime.now()))

versions_file = '%s/%s.versions' % (tools_folder, tools_name)
try:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print '\033[92mCreated %s\033[0m' % output_folder
    with open('%s/testfile.tmp' % output_folder, 'w'): pass
    with open('%s/testfile.tmp' % tools_folder, 'w'): pass
except OSError:
    print '\033[1mOne of the following errors occured:\033[0m'
    print '\033[91mNo permission to create %s\033[0m' % output_folder
    print '\033[91mNo permission to create a file in %s\033[0m' % output_folder
    print '\033[91mNo permission to create a file in %s\033[0m' % tools_folder
    exit(0)