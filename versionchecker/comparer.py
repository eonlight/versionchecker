from datetime import datetime
from pyquery import PyQuery
from sys import stderr
import traceback
import settings
import requests
import re

def cve_exists(software, version):
    url = settings.versions_info[software]['cve-search']
    try:
        # this in a while loop
        html = requests.get(url).text
        pq = PyQuery(html)

        try:
            max_page = len(pq('.paging a'))+1
        except (IndexError, Exception) as e:
            if settings.DEBUG:
                stderr.write(traceback.format_exc())
            max_page = 2

        for page in range(1, max_page):

            version_link = re.search("/vulnerability-list/.*-{version}\.html".format(version=str(version)), html)
            if version_link:
                html = requests.get("http://www.cvedetails.com{path}".format(path=version_link.group())).text
                return [i.group()[1:-1] for i in re.finditer("/CVE-(\d){4}-(\d)+/", html)]

            # get next page
            url = url.replace('/%s/' % str(page), '/%s/' % str(page+1))
            pq = PyQuery(requests.get(url).text)

            if settings.DEBUG:
                print '%s - comparer - compare_versions - Getting Page %s' % (str(datetime.now()), url)

    except (AttributeError, Exception) as e:
        if settings.DEBUG:
            stderr.write(traceback.format_exc())
        stderr.write('%s - comparer - cve_exists - Request Error: %s\n' % (str(datetime.now()), e.message))
        return None

    return False

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
        cve = 'not found'

        # if current version not found
        if isinstance(current, dict) and 'version' not in current:
            current = ''
            if not isinstance(latest, list):
                latest = [latest]
            result.update({software: {'current': current, 'latest': ', '.join(latest), 'result': status, 'cve': cve}})
            continue

        # if version found
        if 'version' in apps[software]:
            current = apps[software]['version']

        # latest version not found
        if 'Regex Error' in latest:
            if current:
                cve = cve_exists(software, current)
            result.update({software: {'current': current, 'latest': latest, 'result': status, 'cve': cve}})
            continue

        # current version not found
        if not current:
            current = ''
            if not isinstance(latest, list):
                latest = [latest]
            result.update({software: {'current': current, 'latest': ', '.join(latest), 'result': status, 'cve': cve}})
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
                if current:
                    cve = cve_exists(software, current)
                result.update({software: {'current': current, 'latest': ', '.join(latest), 'result': 'nok', 'cve': cve}})
                #stderr.write('%s - comparer - compare_versions - Version Finding Error: %s\n' % (str(datetime.now()), e.message))
                continue
            latest = tversion
        else:
            list_latest = [latest]

        if add_zeros(current) < add_zeros(latest):
            status = 'nok'

        cve = cve_exists(software, current)

        latest = list_latest

        result.update({software: {'current': current, 'latest': ', '.join(latest), 'result': status, 'cve': cve}})

    return result

def add_zeros(version=None):
    if not version:
        return None

    new_version = ''

    for i in version.split('.'):
        new_version = ''.join([new_version, '.0', i]) if len(i) == 1 else ''.join([new_version, '.', i])

    return new_version
