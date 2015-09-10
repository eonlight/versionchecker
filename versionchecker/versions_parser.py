from json import dumps, loads
import requests

from datetime import datetime
from sys import stderr
import traceback
import os

import settings

class VersionsParser():

    def __init__(self, versions_file=None):
        if settings.DEBUG:
            print '%s - VersionsParser - __init__ - Creating VersionsParser object...' % str(datetime.now())

        self.latest_versions = {}
        self._versions_file = versions_file or settings.versions_file
        self.load_latest_versions()

    def load_latest_versions(self):
        if settings.DEBUG:
            print '%s - VersionsParser - load_latest_versions - Loading last versions...' % str(datetime.now())

        if not self._versions_file:
            return

        try:
            if os.path.exists(settings.versions_file):
                with open(self._versions_file, 'r') as f:
                    versions = f.read()

                if versions:
                    self.latest_versions = loads(versions)

        except (IOError, ValueError, Exception) as e:
            if settings.DEBUG:
                stderr.write(traceback.format_exc())
            stderr.write('%s - VersionsParser - load_latest_versions - Error %s\n' % (str(datetime.now()), e.message))

    def update_versions(self):
        result = {}
        hs = {'User-Agent': settings.user_agent}

        for software, info in settings.versions_info.iteritems():

            if settings.DEBUG:
                print "%s - VersionsParser - update_versions - Updating %s..." % (str(datetime.now()), software)

            try:
                response = requests.get(info['url'], verify=False, timeout=10, headers=hs)
            except:
                # Any exceptions will be catch and this will continue
                continue

            if not response:
                result.update({software: 'request error'})
                continue

            try:
                module = __import__(info['module'], fromlist = [info['function']])
                function = getattr(module, info['function'])
                version = function(response)
            except (AttributeError, Exception) as e:
                if settings.DEBUG:
                    stderr.write(traceback.format_exc())
                stderr.write('%s - VersionsParser - update_versions - Regex Error: %s\n' % (str(datetime.now()), e.message))
                version = 'Regex Error'

            result.update({software: version})

        self.latest_versions = result

    def save_versions(self):
        if settings.DEBUG:
            print '%s - VersionsParser - save_versions - Saving last versions...' % str(datetime.now())

        if not self._versions_file:
            return

        try:
            with open(self._versions_file, 'w') as f:
                f.write(dumps(self.latest_versions))
        except (IOError, ValueError, Exception) as e:
            if settings.DEBUG:
                stderr.write(traceback.format_exc())
            stderr.write('%s - VersionsParser - save_versions - Error %s\n' % (str(datetime.now()), e.message))
