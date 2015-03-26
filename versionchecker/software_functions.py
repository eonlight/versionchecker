from pyquery import PyQuery
import re

def apache(response):
    versions = []
    html = PyQuery(response.text)
    for version in html('#apcontents h1'):
        version = version.text
        if 'Released' in version:
            versions.append(re.search('(\d.?)+', version).group().strip())
    return versions

def nginx(response):
    html = response.text
    version = re.search('Changes with nginx (\d.?)+', html).group().replace('Changes with nginx', '').strip()
    return version

def iis(response):
    html = PyQuery(response.text)
    version = html('h1.no-article').text()
    version = re.search('(\d\.?)+', version).group().strip()
    return version

def joomla(response):
    html = PyQuery(response.text)
    version = html('a#latest').text()
    version = re.search('(\d\.?)+ Full Package', version).group().replace(' Full Package', '')
    return version

def wordpress(response):
    html = PyQuery(response.text)
    version = re.search('(\d\.?)+', html('p.intro').text()).group()
    return version

def php(response):
    versions = []
    html = PyQuery(response.text)
    for elem in html('div.download ul li a'):
        if 'Release Notes' not in elem.text:
            versions.append(elem.text)
    return versions

def openssl(response):
    html = PyQuery(response.text)
    version = re.search('(\d.?)+', html('pre font a font').text()).group()
    return version

def liferay(response):
    html = response.text
    version = re.search('Liferay Portal (\d\.?)+', html).group().replace('Liferay Portal ', '')
    return version

def ipboard(response):
    #html = PyQuery(response.text)
    #version = html('tr td')[0].text
    return PyQuery(PyQuery(response.text)('table.infobox td')[2])('b').text()
    #return version

def vbulletin(response):
    html = response.text
    version = re.search('announce the release of vBulletin (\d\.?)+', html).group()
    version = re.search('(\d\.?)+', version).group()
    return version

def mysql(response):
    html = response.text
    version = re.search('Current Generally Available Release: (\d.?)+', html).group()
    version = re.search('(\d.?)+', version).group()
    return version

def lighttpd(response):
    html = PyQuery(response.text)
    version = html('.entrytitle h2 a')[0].text
    return version

def postgre(response):
    versions = []
    html = PyQuery(response.text)
    for elem in html('#pgFrontLatestReleasesWrap b'):
        versions.append(elem.text)
    return versions

def drupal(response):
    html = PyQuery(response.text)
    version = html('.download-core a span')[0].text
    version = re.search('(\d.?)+', version).group()
    return version

def tomcat(response):
    versions = []
    for elem in re.findall('(Tomcat (\d.?)+ Released)', response.text):
        versions.append(elem[0].replace('Tomcat ', '').replace(' Released', '').strip())
    return versions
