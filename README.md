# VersionChecker
Checks a URL for which software the server is running and its versions.

Gets the latest versions and reports the ones that are outdated.

## Base Suported Software

* apache
* nginx
* microsoft-iis
* joomla
* wordpress
* php
* openssl
* liferay
* ipboard
* vbulletin
* mysql
* lighttpd
* postgre
* drupal
* tomcat

## Installation

```
pip install git+https://github.com/eonlight/parsers
pip install git+https://github.com/eonlight/versionchecker
```

or

```
git clone https://github.com/eonlight/parsers
cd parsers
./setup.py install
cd ..
git clone https://github.com/eonlight/versionchecker
cd versionchecker
./setup.py install
```

## Configuration

* Requires parsers module
    * It will automatically install the module but you should check the configurations:
        * https://github.com/eonlight/parsers

* Run `versionchecker --update' to update the lastest versions

* You can add you're own functions to get the latest versions of other software in:
    * `~/.config/audits/verisonchecker_settings.py'

* You can also add you're one software to check for versions, check:
    * `~/.config/audits/verisonchecker_settings.py'

## How it works

* Starts by running WhatWeb & NMap (and any other tool in the local settings) against the provided URL
* Uses parsers to get a json result from WhatWeb & NMap
* Using the preloaded latest versions compares with the result from the identified versions
* Reports if the identified software is out-of-date or not

## Examples

* Check the installed versions on https://www.github.com
```
versionchecker https://www.github.com
```

* Cherk the installed versions on https://www.github.com and get the result in json format
```
versionchecker --json https://www.github.com
```

* Check the settings
```
versionchecker --settings
```

## To Do List

* Nothing

## Changelog

### Version 0.2.0 (current)

* Adds Support for the CVE reporting
    * In the report it will show if any and how many CVEs were found
    * Requires a URL for each new software added in the configs.
    * It reports both if it is out-of-date and if there are any CVEs
* Checks for the latest versions file before running

### Version 0.1.0

* Adds Support to add your own software version identification
    * check the Configuration section
* Refactors the latest software fetch functions
* Adds more detailed information about errors or misconfigurations
* Adds option to run without arguments
* Improves setup with pre and post instalation scripts
* Fixes some bugs

### Version 0.0.1

* First official release
