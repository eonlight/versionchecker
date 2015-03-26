# these are the Default Options

tools_name = 'versionchecker'
tools_folder = '{{ home }}/.config/audits'
output_folder = '{{ home }}/.config/audits/output'
#user_agent = 'VersionChecker/{{ version }}'

# if only module name is set, it will search for a function with the name of the software
versions_info = {
    # example
    #'apache':    {
    #    'url': 'http://httpd.apache.org/',
    #    'function': 'versionchecker_settings.apache'
    #},
}

# receives as parameter the response of a GET to the url
# def apache(response):
    #html = response.html
    #versions = [do stuffs with html]
    #return versions
#

DEBUG = False
