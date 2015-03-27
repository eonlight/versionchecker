from sys import argv, exit, stderr
from datetime import datetime
import traceback

import requests
import re

import settings

from parsers import WhatWebParser
from comparer import compare_versions
from versions_parser import VersionsParser

class bcolors:
    FAIL = '\033[91m'
    ENF  = '\033[1m'
    OK  = '\033[92m'
    END = '\033[0m'

def printhelp():
    print 'Usage: %s %scommand | url%s ' % (argv[0], bcolors.ENF, bcolors.END)
    print 'Available commands:'
    print '  %s--url url%s' % (bcolors.ENF, bcolors.END)
    print '    checks the software versions of the given url'
    print '  %s--json url%s' % (bcolors.ENF, bcolors.END)
    print '    checks the software version of the given url and prints the results in json format'
    print '  %s--update%s' % (bcolors.ENF, bcolors.END)
    print '    updates the latest versions of all software'
    print '  %s--versions%s' % (bcolors.ENF, bcolors.END)
    print '    prints the latest versions of all the software'
    print '  %s--settings%s' % (bcolors.ENF, bcolors.END)
    print '    prints the settings of VersionChecker and its tools'

def merge_results(result, new_result):
    for key in new_result:
        if key not in result:
            result[key] = new_result[key]
        elif 'version' in new_result[key] and new_result[key] != '':
            result[key] = new_result[key]

def test(url=None):
    if not url:
        return None

    versionsparser = VersionsParser()

    stats = {'issues': 0}

    try:
        stats['start'] = datetime.now()
        stats['host'] = url

        detected_versions = {}
        for tool in sorted(settings.version_checking_tools):
            # gets class and module info
            info = settings.version_checking_tools[tool]

            try:
                #imports module and class
                module = __import__(info['module'], fromlist = [info['class']])
                Class = getattr(module, info['class'])

                print 'Running %s...' % tool

                # runs the tool
                obj = Class(tool=settings.tools_name)
                merge_results(detected_versions, obj.execute(url))

            except (AttributeError, Exception) as e:
                if settings.DEBUG:
                    stderr.write(traceback.format_exc())
                stderr.write('%s - versionchecker - test - Import Error: %s\n' % (str(datetime.now()), e.message))
                continue

        result = compare_versions(detected_versions, versionsparser.latest_versions)

        if detected_versions and result:
            for key in result:
                if 'result' in result[key]:
                    stats['issues'] = stats['issues'] + 1 if 'nok' == result[key]['result'] else stats['issues']

        stats['end'] = datetime.now()

        return result
    except (ValueError) as e:
        if settings.DEBUG:
            stderr.write(traceback.format_exc())
    return None

def run(url):
    try:
        scan = 'Scan started at %s' % str(datetime.now())
        print '\n%s %s %s\n' % ( ('-' * ((78 - len(scan))/2)), scan, ('-' * ((78 - len(scan))/2)) )
        result = test(url)
        print '--------------------------------------------------------------------------------'
        print '--------------------------- %sVersionChecker Results%s -----------------------------' % (bcolors.ENF, bcolors.END)
        print '--------------------------------------------------------------------------------'

        for key in result:
            print 'Software: %s%s%s' % (bcolors.ENF, key, bcolors.END)
            print '  Version in use: %s' % result[key]['current']
            print '  Latest Version: %s' % result[key]['latest']
            veredict = '  %sVersion not detected%s' % (bcolors.ENF, bcolors.END)
            if 'nok' == result[key]['result']:
                veredict = '  %sOut-Of-Date%s' % (bcolors.FAIL, bcolors.END)
            elif 'ok' == result[key]['result']:
                veredict = '  %smUp-To-Date%s' % (bcolors.OK, bcolors.END)
            print veredict
            print

        scan = 'Scan ended at %s' % str(datetime.now())
        print '%s %s %s\n' % ( ('-' * ((78 - len(scan))/2)), scan, ('-' * ((78 - len(scan))/2)) )

    except (ValueError) as e:
        if settings.DEBUG:
            stderr.write(traceback.format_exc())

def main():

    if '--debug' in argv:
        settings.DEBUG = True

    if '--url' in argv:
        try:
            url = argv[argv.index('--url') + 1]
        except IndexError:
            print 'No url given'; exit(0)

        run(url)

    elif '--json' in argv:
        try:
            url = argv[argv.index('--json') + 1]
        except IndexError:
            print '%sNo url given.%s' % (bcolors.FAIL, bcolors.END); exit(0)
        print test(url)

    elif '--update' in argv:
        versionsparser = VersionsParser()
        versionsparser.update_versions()
        versionsparser.save_versions()
        print '%sVersions updated.%s' % (bcolors.OK, bcolors.END)

    elif '--versions' in argv:
        versionsparser = VersionsParser()
        versions = versionsparser.latest_versions
        for key in versions:
            print '%s: %s' % (key, versions[key])

    elif '--settings' in argv:

        print '%sDEBUG%s: %s' % (bcolors.ENF, bcolors.END, 'ON' if settings.DEBUG else 'OFF')
        print '%stool\'s folder%s: %s' % (bcolors.ENF, bcolors.END, settings.tools_folder)
        print '%soutput\'s folder%s: %s' % (bcolors.ENF, bcolors.END, settings.output_folder)

        # tools settings:
        for tool in sorted(settings.version_checking_tools):
            if 'whatweb' in tool or 'nmap' in tool:
                info = settings.version_checking_tools[tool]
                try:
                    #imports module and class
                    module = __import__(info['module'], fromlist = [info['class']])
                    tool_settings = getattr(module, 'settings')

                    print '%s%s%s:' % (bcolors.ENF, tool, bcolors.END)
                    print '  %sDEBUG%s: %s' % (bcolors.ENF, bcolors.END, 'ON' if tool_settings.DEBUG else 'OFF')
                    print '  %stool\'s bin%s: %s' % (bcolors.ENF, bcolors.END, tool_settings.nmap_bin if 'nmap' in tool else tool_settings.whatweb_bin)
                    print '  %soutput\'s folder%s: %s' % (bcolors.ENF, bcolors.END, tool_settings.output_folder)

                except (AttributeError, Exception) as e:
                    stderr.write('%s - versionchecker - main - Import Error: %s\n' % (str(datetime.now()), e.message))
                    continue

    elif len(argv) > 1:
        run(argv[1])

    else:
        printhelp()

if __name__ == '__main__':
    main()
