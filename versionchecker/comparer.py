from datetime import datetime
from sys import stderr
import traceback
import settings
import re

def compare_versions(apps=None, versions=None):
    """ returns [{software: {current: X.X, latest: Y.Y, result: 'ok|nok'}}] """
    if not apps or not versions:
        return {}

    if settings.DEBUG:
        print '%s - comparer - compare_versions - Starting to compare versions...' % str(datetime.now())

    result = {}
    for software in apps:

        if software not in versions:
            continue

        current = apps[software]
        latest = versions[software]
        status = 'ok'

        # if current version not found
        if isinstance(current, dict) and 'version' not in current:
            current = ''
            if not isinstance(latest, list):
                latest = [latest]
            result.update({software: {'current': current, 'latest': ', '.join(latest), 'result': status}})
            continue

        # if version found
        if 'version' in apps[software]:
            current = apps[software]['version']

        # latest version not found
        if 'Regex Error' in latest:
            result.update({software: {'current': current, 'latest': latest, 'result': status}})
            continue

        # current version not found
        if not current:
            current = ''
            if not isinstance(latest, list):
                latest = [latest]
            result.update({software: {'current': current, 'latest': ', '.join(latest), 'result': status}})
            continue

        #if whatweb finds a list, select the best one
        if isinstance(current, list):
            best_current = current[0]
            for i in current:
                if len(best_current.split('.')) < len(i.split('.')):
                    best_current = i
            current = best_current

        # if current is not a list, regex the current version to find only numbers
        if not isinstance(current, list):
            current = re.search('(\d\.?)*', current).group()

        list_latest = latest
        if isinstance(latest, list):
            try:
                prefix = re.search('\d\.\d', current).group()
                tversion = [v for v in latest if prefix in v][0]
            except (IndexError, Exception) as e:
                if settings.DEBUG:
                    stderr.write(traceback.format_exc())
                    print "%s - comparer - compare_versions - Current: %s" % (str(datetime.now()), current)
                    print "%s - comparer - compare_versions - Latest: %s" % (str(datetime.now()), latest)
                result.update({software: {'current': current, 'latest': ', '.join(latest), 'result': 'nok'}})
                stderr.write('%s - comparer - compare_versions - Version Finding Error: %s\n' % (str(datetime.now()), e.message))
                continue
            latest = tversion
        else:
            list_latest = [latest]

        if add_zeros(current) < add_zeros(latest):
            status = 'nok'

        latest = list_latest

        result.update({software: {'current': current, 'latest': ', '.join(latest), 'result': status}})

    return result

def add_zeros(version=None):
    if not version:
        return None

    new_version = ''

    for i in version.split('.'):
        new_version = ''.join([new_version, '.0', i]) if len(i) == 1 else ''.join([new_version, '.', i])

    return new_version
