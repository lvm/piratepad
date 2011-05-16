import urllib2
from BeautifulSoup import BeautifulSoup
import re


piratepad = "http://piratepad.net/"


def parse_rev(pagename, script=None):
    if script:
        return re.findall('"rev":([0-9]+)', script)[0]
    else:
        page = urllib2.urlopen("%s%s" % (piratepad, pagename))
        soup = BeautifulSoup(page)
        script = "\n".join(soup.html.script.text.split("\n")[1:-1])[17:]
        return parse_rev(0, script)


def parse_pp(pagename=None):
    data = {}
    if pagename:
        data = {pagename: {'url': "%s%s" % (piratepad, pagename),
                         'related': {},
                         'export': {},
                         'rev': 0,
                         }
              }
        page = urllib2.urlopen("%s%s" % (piratepad, pagename))
        soup = BeautifulSoup(page)
        script = "\n".join(soup.html.script.text.split("\n")[1:-1])[17:]
        pages = re.findall("(%s[a-zA-Z0-9\-]+)" % piratepad, script)
        rev = parse_rev(0, script)
        data[pagename]['rev'] = rev
        for format in ['html', 'txt', 'doc', 'pdf']:
            data[pagename]['export'][format] = \
                "%sep/pad/export/%s/rev.%s?format=%s" %\
                (piratepad, pagename, rev, format)
        for page in pages:
            page_id = page.replace(piratepad, '')
            rev = parse_rev(page_id)
            data[pagename]['related'][page_id] = {'url': "%s%s" %\
                                                      (piratepad, page_id),
                                                  'export': {},
                                                  'rev': rev,
                                             }
            for format in ['html', 'txt', 'doc', 'pdf']:
                data[pagename]['related'][page_id]['export'][format] = \
                    "%sep/pad/export/%s/rev.%s?format=%s" %\
                    (piratepad, page_id, rev, format)
    return data

#print parse_pp('you-name-it')
