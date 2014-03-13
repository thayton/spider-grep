import re, getopt, sys, urlparse, time

from bs4 import BeautifulSoup
from mechanize import Browser

#
# python spider-grep.py -u 'http://www.jesupga.gov/bids.html' -r '(\bbids\b|rfp)'
#
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:r:", ["url=", "regex="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)

    url = None
    regex = None

    for o, a in opts:
        if o in ("-u", "--url"):
            url = a
        elif o in ("-r", "--regex"):
            regex = a
        else:
            assert False, "unhandled option"
    
    br = Browser()
    br.open(url)        

    s = BeautifulSoup(br.response().read())
    r = re.compile(r'%s' % regex, re.I)

    visited = []
    reported = []

    for a in s.findAll('a'):
        time.sleep(2)

        url = urlparse.urljoin(br.geturl(), a['href'])

        print 'Opening page %s' % url
        br.open(url)        

        z = BeautifulSoup(br.response().read())

        page = br.geturl()
        print '\n'.join(['%s: %s' % (page, x.parent) for x in z.findAll(text=r)])
        
        for y in z.findAll('a', href=r):
            u = '%s' % urlparse.urljoin(br.geturl(), y['href'])
            if u not in reported:
                print page + ':', u
                reported.append(u)
                print reported
