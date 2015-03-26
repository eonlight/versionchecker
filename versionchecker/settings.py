from sys import path, stderr
from datetime import datetime
import os

version = '0.0.1'

tools_name = 'versionchecker'
tools_folder = '%s/.config/audits' % os.getenv("HOME")
output_folder = '%s/output' % tools_folder

# if only module name is set, it will search for a function with the name of the software
versions_info = {
    'apache':    {
        'url': 'http://httpd.apache.org/',
        'function': 'versionchecker.software_functions.apache'
    },
    'nginx':     {
        'url': 'http://nginx.org/en/CHANGES',
        'function': 'versionchecker.software_functions.nginx'
    },
    'microsoft-iis':       {
        'url': 'http://www.iis.net/learn',
        'function': 'versionchecker.software_functions.iis'
    },
    'joomla':    {
        'url': 'http://www.joomla.org/download.html',
        'function': 'versionchecker.software_functions.joomla'
    },
    'wordpress': {
        'url': 'http://wordpress.org/download/',
        'function': 'versionchecker.software_functions.wordpress'
    },
    'php':       {
        'url': 'http://www.php.net/',
        'function': 'versionchecker.software_functions.php'
    },
    'openssl':   {
        'url': 'http://www.openssl.org/source/',
        'function': 'versionchecker.software_functions.openssl'
    },
    'liferay':   {
        'url': 'http://www.liferay.com/community/releases',
        'function': 'versionchecker.software_functions.liferay'
    },
    'ipboard':   {
        #'url': 'http://community.invisionpower.com/resources/documentation/versions.html',
        'url': 'http://en.wikipedia.org/wiki/Invision_Power_Board',
        'function': 'versionchecker.software_functions.ipboard'
    },
    'vbulletin': {
        'url': 'http://www.vbulletin.com/forum/external?type=rss2&nodeid=28',
        'function': 'versionchecker.software_functions.vbulletin'
    },
    'mysql':     {
        'url': 'http://dev.mysql.com/downloads/',
        'function': 'versionchecker.software_functions.mysql'
    },
    'lighttpd':  {
        'url': 'http://www.lighttpd.net/download/',
        'function': 'versionchecker.software_functions.lighttpd'
    },
    'postgre':   {
        'url': 'http://www.postgresql.org/',
        'function': 'versionchecker.software_functions.postgre'
    },
    'drupal':    {
        'url': 'https://www.drupal.org/download',
        'function': 'versionchecker.software_functions.drupal'
    },
    'tomcat':    {
        'url': 'http://tomcat.apache.org/',
        'function': 'versionchecker.software_functions.tomcat'
    },
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

    if hasattr(versionchecker_settings, 'joomla_sql_files'): joomla_sql_files = list(set(versionchecker_settings.joomla_sql_files + joomla_sql_files))

except ImportError:
    stderr.write('%s - settings - versionchecker local settings not found...\n' % str(datetime.now()))

versions_file = '%s/%s.versions' % (tools_folder, tools_name)
if not os.path.exists(output_folder):
    try:
        os.mkdir(output_folder)
    except OSError:
        print '\033[91mNo permission to create %s.\033[0m' % output_folder
        exit(0)