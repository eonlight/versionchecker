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
    ENDC = '\033[0m'

def printhelp():
    print 'Usage: %s command' % argv[0]
    print 'Available commands:'
    print '  --url url'
    print '    checks the software versions of the given url'
    print '  --json url'
    print '    checks the software version of the given url and prints the results in json format'
    print '  --update'
    print '    updates the latest versions of all software'
    print '  --versions'
    print '    prints the latest versions of all the software'
    print '  --settings'
    print '    prints the settings of VersionChecker'

def test(url=None):
    if not url:
        return None

    whatwebparser = WhatWebParser(tool=settings.tools_name)
    versionsparser = VersionsParser()

    stats = {'issues': 0}

    try:
        stats['start'] = datetime.now()
        stats['host'] = url

        wwr = whatwebparser.execute(url)
        result = compare_versions(wwr, versionsparser.latest_versions)

        if wwr and result:
            for key in result:
                if 'result' in result[key]:
                    stats['issues'] = stats['issues'] + 1 if 'nok' == result[key]['result'] else stats['issues']

        stats['end'] = datetime.now()

        return result
    except (ValueError) as e:
        if settings.DEBUG:
            stderr.write(traceback.format_exc())
    return None

def main():

    if '--url' in argv:
        try:
            url = argv[argv.index('--url') + 1]
        except IndexError:
            print 'No url given'; exit(0)

        try:
            scan = 'Scan started at %s' % str(datetime.now())
            print '\n%s %s %s\n' % ( ('-' * ((78 - len(scan))/2)), scan, ('-' * ((78 - len(scan))/2)) )
            result = test(url)
            print '--------------------------------------------------------------------------------'
            print '--------------------------- \033[1mVersionChecker Results\033[0m -----------------------------'
            print '--------------------------------------------------------------------------------'
            for key in result:
                print 'Software: \033[1m%s\033[0m' % key
                print '  Version in use: %s' % result[key]['current']
                print '  Latest Version: %s' % result[key]['latest']
                print '  \033[91mOut-Of-Date\033[0m' if 'nok' == result[key]['result'] else '  \033[92mUp-To-Date\033[0m' if result[key]['current'] else '  Version not detected'
                print
            scan = 'Scan ended at %s' % str(datetime.now())
            print '%s %s %s\n' % ( ('-' * ((78 - len(scan))/2)), scan, ('-' * ((78 - len(scan))/2)) )

        except (ValueError) as e:
            if settings.DEBUG:
                stderr.write(traceback.format_exc())

    elif '--json' in argv:
        try:
            url = argv[argv.index('--json') + 1]
        except IndexError:
            print '\033[91mNo url given.\033[0m'; exit(0)
        print test(url)

    elif '--update' in argv:
        versionsparser = VersionsParser()
        versionsparser.update_versions()
        versionsparser.save_versions()
        print '\033[92mVersions updated.\033[0m'

    elif '--versions' in argv:
        versionsparser = VersionsParser()
        versions = versionsparser.latest_versions
        for key in versions:
            print '%s: %s' % (key, versions[key])

    elif '--settings' in argv:
        print 'DEBUG: %s' % ('ON' if settings.DEBUG else 'OFF')
        print 'tools folder: %s' % settings.tools_folder
        print 'output folder: %s' % settings.output_folder

    else:
        printhelp()

if __name__ == '__main__':
    main()
