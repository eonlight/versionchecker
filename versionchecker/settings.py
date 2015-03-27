from sys import path, stderr
from datetime import datetime
import os

version = '0.2.0'

tools_name = 'versionchecker'
tools_folder = '%s/.config/audits' % os.getenv("HOME")
output_folder = '%s/output' % tools_folder

# if only module name is set, it will search for a function with the name of the software
versions_info = {
    'apache':    {
        'url': 'http://httpd.apache.org/',
        'module': 'versionchecker.software_functions',
        'function': 'apache',
        'cve-search': 'http://www.cvedetails.com/version-list/45/66/1/Apache-Http-Server.html',
    },
    'nginx':     {
        'url': 'http://nginx.org/en/CHANGES',
        'module': 'versionchecker.software_functions',
        'function': 'nginx',
        'cve-search': 'http://www.cvedetails.com/version-list/10048/17956/1/Nginx-Nginx.html',
    },
    'microsoft-iis':       {
        'url': 'http://www.iis.net/learn',
        'module': 'versionchecker.software_functions',
        'function': 'iis',
        'cve-search': 'http://www.cvedetails.com/version-list/26/3436/1/Microsoft-IIS.html',
    },
    'joomla':    {
        'url': 'http://www.joomla.org/download.html',
        'module': 'versionchecker.software_functions',
        'function': 'joomla',
        'cve-search': 'http://www.cvedetails.com/version-list/3496/6129/1/Joomla-Joomla.html',
    },
    'wordpress': {
        'url': 'http://wordpress.org/download/',
        'module': 'versionchecker.software_functions',
        'function': 'wordpress',
        'cve-search': 'http://www.cvedetails.com/version-list/2337/4096/1/Wordpress-Wordpress.html',
    },
    'php':       {
        'url': 'http://www.php.net/',
        'module': 'versionchecker.software_functions',
        'function': 'php',
        'cve-search': 'http://www.cvedetails.com/version-list/74/128/1/PHP-PHP.html',
    },
    'openssl':   {
        'url': 'http://www.openssl.org/source/',
        'module': 'versionchecker.software_functions',
        'function': 'openssl',
        'cve-search': 'http://www.cvedetails.com/version-list/217/383/1/Openssl-Openssl.html',
    },
    'liferay':   {
        'url': 'http://www.liferay.com/community/releases',
        'module': 'versionchecker.software_functions',
        'function': 'liferay',
        'cve-search': 'http://www.cvedetails.com/version-list/2114/18625/1/Liferay-Liferay-Portal.html',
    },
    'ipboard':   {
        'url': 'http://en.wikipedia.org/wiki/Invision_Power_Board',
        'module': 'versionchecker.software_functions',
        'function': 'ipboard',
        'cve-search': 'http://www.cvedetails.com/version-list/10268/18333/1/Invisionpower-Invision-Power-Board.html',
    },
    'vbulletin': {
        'url': 'http://www.vbulletin.com/forum/external?type=rss2&nodeid=28',
        'module': 'versionchecker.software_functions',
        'function': 'vbulletin',
        'cve-search': 'http://www.cvedetails.com/version-list/8142/14110/1/Vbulletin-Vbulletin.html',
    },
    'mysql':     {
        'url': 'http://dev.mysql.com/downloads/',
        'module': 'versionchecker.software_functions',
        'function': 'mysql',
        'cve-search': 'http://www.cvedetails.com/version-list/185/316/1/Mysql-Mysql.html',
    },
    'lighttpd':  {
        'url': 'http://www.lighttpd.net/download/',
        'module': 'versionchecker.software_functions',
        'function': 'lighttpd',
        'cve-search': 'http://www.cvedetails.com/version-list/2713/4762/1/Lighttpd-Lighttpd.html',
    },
    'postgre':   {
        'url': 'http://www.postgresql.org/',
        'module': 'versionchecker.software_functions',
        'function': 'postgre',
        'cve-search': 'http://www.cvedetails.com/version-list/336/575/1/Postgresql-Postgresql.html',
    },
    'drupal':    {
        'url': 'https://www.drupal.org/download',
        'module': 'versionchecker.software_functions',
        'function': 'drupal',
        'cve-search': 'http://www.cvedetails.com/version-list/1367/2387/1/Drupal-Drupal.html',
    },
    'tomcat':    {
        'url': 'http://tomcat.apache.org/',
        'module': 'versionchecker.software_functions',
        'function': 'tomcat',
        'cve-search': 'http://www.cvedetails.com/version-list/45/887/1/Apache-Tomcat.html',
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