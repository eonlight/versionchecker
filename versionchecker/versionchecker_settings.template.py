# these are the Default Options

tools_name = 'versionchecker'
tools_folder = '{{ home }}/.config/audits'
output_folder = '{{ home }}/.config/audits/output'
#user_agent = 'VersionChecker/{{ version }}'

# if only module name is set, it will search for a function with the name of the software
versions_info = {
    # example
    #'my_software':    {
    #    'url': 'http://my-software.com/versions',
    #    'module': 'versionchecker_settings'
    #    'function': 'my_software_scrapper'
    #},
}

# receives as parameter the response of a GET to the url
# def my_software_scrapper(response):
#    html = response.html
#    versions = [do stuff with html]
#    return versions


# this are the tools that will run to check the verison of the software running
# you can use numbers before the names to specify which are going to run first
# Note: versions will be replaced by the newest detection
version_checking_tools = {
    '4.whatweb': {
        'module': 'parsers',
        'class': 'WhatWebParser',
    },
    '9.nmap': {
        'module': 'parsers',
        'class': 'NMapParser'
    },
    #'2.my_software': {
    #    'module': 'versionchecker_settings'
    #    'function': 'MySoftwareVersionChecker'
    #},
    #'1.other_checker': {
    #    'module': 'installed_module',
    #   ''
    #}
}

#class MySoftwareVersionChecker:
    #def __init__(self, tool='DefaultToolNameThatIsCallingThisChecker'):
    #    Do something
    #    self.executable = '/usr/bin/MySoftwareBinary'

    #def execute(self, url):
        # Do something to identify the version (eg.):
        # Run self.executable
        # return everything in lowercase
    #    return {
    #        'identified_software1':
    #            {'version': '1.2.3', 'other_info': 'info'},
    #        'my_software':
    #            {'version': 1.2}
    #    }

DEBUG = {{ debug }}
