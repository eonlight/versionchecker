# VersionChecker
Checks a URL for which software the server is running and its versions.

Gets the latest versions and reports the ones that are outdated.

## Instalation

`pip install git+https://github.com/eonlight/versionchecker`

or

```
git clone https://github.com/eonlight/versionchecker
cd versionchecker
./setup install
```

## Configuration

* Requires parsers module
    * It will automatically install the module but you should check the configurations:
        * https://github.com/eonlight/parsers

* Run `versionchecker --update' to update the lastest versions

* You can add you're own functions to get tyhe latest versions of other software in:
    * `~/.config/audits/verisonchecker_settings.py'

## How it works

* Starts by running WhatWeb against the provided URL
* Uses parsers to get a json result from WhatWeb
* Using the preloaded latest versions compares with the result from WhatWeb
* Reports if the identified software is out-of-date or not

## Examples

* Check the installed versions on https://www.github.com
```
versionchecker --url https://www.github.com
```

* Cherk the installed versions on https://www.github.com and get the result in json format
```
versionchecker --json https://www.github.com
```

## To Do List

* Add support for more version identification tools
* Add CVE verification feature
    * Report as Out-Of-Date only if current version has known CVEs