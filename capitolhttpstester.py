#!/usr/bin/env python
"""
GNU General Public License v2.0

capitolhttpstester.py

this is a script to test various US Capitol Entities websites for valid-
ish https configurations . output is a json report of what it found .
use other script to make html from the json output . it forcibly
connects to the https port (443) even if the cert won't work .
equivalent of ignoring warnings in browser . also properly checks for
redirects via either meta-refresh or HTTP 3XX redirect .

went for extra credit and did cursory checks to see if there's mixed
http/https in the retrieved webpage . did not go for super bonus extra
credit and actually crawl the whole site to check for inconsistencies .

Data Sources: list of senators and reps comes from the sunlight api .
list of committees comes from unitedstates github repo . this script
relies mozilla.org's certifi lib for checking certs .

OUTPUT FORMAT:
XXX possibly should have a higher level thing so like {'body':'', 'type':'', 'reports': []}
results_row:
    # from get_representatives, get_senators, get_cmtes
    'name': '',
    'url': '',
    'body': house|senate|joint,
    'type': member|committee,

    # from get_cert_info
    'hostname_match': boolean,
    'cert_expire': date
    'cipher algo': '',
    'cipher SSL_ver': '',
    'cipher bits': '',

    # from make_request
    'http status': '',
    'redirects': boolean,
    'redirect_url': 'method and where redirect too',
    'SSL issues': 'packing to describe various issues',
    'mixed content': 'for extra credit'
        - non-relative urls
        - hrefs
        - img
        - script
        - <link> tags


Usage:
```sh
$ virtualenv --no-site-packages virt
$ source virt/bin/activate
$ pip install -r requirements.txt
$ cp settings.py.example settings.py
$ edit settings.py # put your sunlight key in API_KEY
$ python capitolhttpstester.py > output.json
```

Run Time: even w/ a setting of 0.3s between requests this
script takes some time . currently it's hitting 578 sites .

```sh
timball@thompson {130}$ time python ./capitolhttpstester.py > out.json
ERROR nothing worked for Robert Aderholt R-AL 4 https://aderholt.house.gov

real    7m10.743s
user    0m29.752s
sys     0m1.792s
```

--timball@sunlightfoundation.com
2015-05-17
"""

from __future__ import print_function

import logging
logging.captureWarnings(True)

import sunlight
from sunlight import congress
import settings
sunlight.config.API_KEY=settings.API_KEY
DEBUG=False


def get_paging_service(chamber, limit):
    from sunlight.pagination import PagingService

    paging_service = PagingService(congress)
    members = list(paging_service.legislators(chamber=chamber, limit=limit)) 

    return members

def get_senators():
    senators = get_paging_service('senate', 200) # limited future proofing

    # sucessfully learned list comprehensions w00t!
    return [ {'name': s['first_name'] +' '+ s['last_name'],
              'state_dist': s['party'] +'-'+ s['state'],
              'body': 'senate',
              'type': 'member',
              'url' :s['website'].replace('http://', 'https://')}
              for s in senators if s['website'] ]

def get_representatives():
    members = get_paging_service('house', 600) # limited future proofing
    return [ {'name': h['first_name'] +' '+ h['last_name'],
              'state_dist': h['party'] +'-'+ h['state'] +' '+ str(h['district']),
              'body': 'house',
              'type': 'member',
              'url' :h['website'].replace('http://', 'https://')}
              for h in members if h['website'] ]


def get_yaml(url):
    import requests
    import yaml

    r = requests.get(url)
    return yaml.load(r.content)


def get_house_cmte(url_label):
    y = get_yaml(settings.us_cmte_curr_url)

    if (url_label == 'url'):
        minority_prefix = ''
    elif (url_label == 'minority_url'):
        minority_prefix = 'Minority '

    return [ {'name': minority_prefix + cmte['name'],
              'url' : cmte['url'].replace('http://', 'https://'),
              'state_dist': None,
              'body': cmte['type'],
              'type': minority_prefix + 'committee',}
              for cmte in y if url_label in cmte ]


def get_cmtes():
    return get_house_cmte('url')


def get_house_minority_cmte():
    return get_house_cmte('minority_url')


def get_leadership():
    y = get_yaml(settings.us_leadership_url)

    return [ {'name': leader['office'],
              'url' : leader['url'].replace('http://', 'https://'),
              'state_dist': None,
              'body': leader['type'],
              'type': 'leadership',}
              for leader in y if 'url' in leader ]


def get_support_offices():
    y = get_yaml(settings.us_support_offices_url)

    return [ {'name': support['name'],
              'url' : support['url'].replace('http://', 'https://'),
              'state_dist': None,
              'body': support['type'],
              'type': 'support',}
              for support in y if 'url' in support and support['url'] ]


def find_commonname(subject):
    import re

    for i in subject:
        for j in i:
            if re.match('commonname', j[0], re.I):
                # pretty sure you can only have one CN per cert so bail
                return j[1]


def regex_from_list(names):
    # this turns a list of potential globs into a thing that re will work with
    from fnmatch import translate as xlate

    return "|".join( [xlate(x) for x in names] )


def get_cert_info(url):
    # ideally returns the bits of the cert in dict form
    # `if ret['cipher'] == None` is my "error condition"

    import socket, ssl, pprint, urllib3, re
    import certifi
    ret = {}
    ret['subjectAltName'] = [] # need this or .append won't work

    parsed_url = urllib3.util.parse_url(url)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(settings.TIME_OUT) # srsly if it takes you more than 10s that's an error
    # require a certificate from the server
    ssl_sock = ssl.wrap_socket(s,
                               ca_certs=certifi.where(),
                               cert_reqs=ssl.CERT_REQUIRED)
    # XXX do i have to call s.close() at the end or will the python GC do that ? or am i leaking memory ??

    try:
        ssl_sock.connect((parsed_url.host, 443))
    except Exception as e:
        # what if port 443 is not open ??? bail
        ret['notAfter'] = None
        ret['cipher']   = None
        ret['SSL_ver']  = None
        ret['bits']     = None
        return ret

    # XXX what if there's no cert ? not handled
    cert = ssl_sock.getpeercert()
    # subjectAlteName tuples are in useless form of (('DNS:', 'hostname'), (), (), ...)
    if 'subjectAltName' in cert:
        ret['subjectAltName'] = [ x[1] for x in cert['subjectAltName'] ]
    # there is no functional difference between CommonName (CN) and subjectAltName in this study
    ret['subjectAltName'].append(find_commonname(cert['subject']))

    re_g = regex_from_list(ret['subjectAltName'])
    if re.match(re_g, parsed_url.host, re.I|re.DOTALL):
        ret['hostname_match'] = True
    else:
        ret['hostname_match'] = False
    # not needed anymore
    del ret['subjectAltName']

    # when does cert expire ?
    ret['notAfter'] = cert['notAfter']

    # encryption details
    cipher = ssl_sock.cipher()
    ret['cipher']  = cipher[0]
    ret['SSL_ver'] = cipher[1]
    ret['bits']    = cipher[2]

    if DEBUG:
        print("========\nDEBUG:\n" + pprint.pformat(ssl_sock.getpeercert()) + "============", file=sys.stderr)
    return ret


def mixed_detector(elements):
    import re
    # freak out on first thing that gives mixed content
    ret = False

    # dumb bs4 hack ... there's some right way to do this w/ attrs.get() XXX
    for element in elements:
        try:
            foo = element['href']
        except KeyError:
            continue
        if re.match('.*http://.*', foo, re.I|re.DOTALL):
            return True
    return ret


def mixed_internal_anchor_detector(anchors, sec_url):
    from fnmatch import translate as xlate
    import re
    ret = False
    vul_url=sec_url.replace('https://','http://')
    vul_url=vul_url+"*"

    for link in anchors:
        try:
            foo = link['href']
        except KeyError:
            continue
        if re.match(xlate(vul_url), foo, re.I|re.DOTALL):
            #print "non-relative link: %s" % (foo)
            return True
    return ret

def mixed_content(sec_url, content):
    # vague mix-content checking
    # XXX for the moment only check <link href=''> <img src=''> <a href=''> <script src=''>

    import re
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content)

    links   = soup.find_all('link')
    anchors = soup.find_all('a')
    imgs    = soup.find_all('img')
    scripts = soup.find_all('script')

    # everyone gets to start clean
    ret={'resources': False, 'images': False, 'links': False}

    ret['resources'] = mixed_detector(links) or mixed_detector(scripts) or mixed_detector(imgs)
    ret['links']     = mixed_internal_anchor_detector(anchors, sec_url)

    if ((DEBUG) and (ret['resources'] or ret['images'] or ret['links'])):
        print ("mixed resources :(", file=sys.stderr)

    return ret


def make_request(url):
    import requests, re, urllib3
    import time
    probe = {}
    probe['http status']   = 'init'
    probe['redirects']     = 'init'
    probe['redirect_url']  = 'init'
    probe['SSL issues']    = 'init'
    probe['mixed content'] = False
    probe['non-rel links'] = False

    time.sleep(settings.SLEEP_TIME) # be nice, not too nice

    try:
        r = requests.get(url, headers=settings.FAKE_HEADERS, verify=False, allow_redirects=False)
    except requests.exceptions.SSLError as e:
        True
    except requests.exceptions.ConnectionError as e:
        probe['http status']  = None
        probe['redirects']    = False
        probe['redirect_url'] = None
        probe['SSL issues']   = 'unable to connect HARD FAIL',
        probe['mixed content'] = False
        probe['non-rel links'] = False
        print ('url: %s' % (url), file=sys.stderr)

    probe['http status'] = r.status_code
    if r.status_code == 200:
        # check for meta refresh in r.content
        # XXX is there another valid 2XX response ?
        m = re.match(r'.*meta http-equiv="refresh".*URL=(?P<url>.*)".*', r.content, re.IGNORECASE|re.DOTALL)
        if m:
            probe['redirects']    = True
            probe['redirect_url'] = m.group("url")
            parsed_url            = urllib3.util.parse_url(m.group("url"))
            if parsed_url.scheme != 'https':
                probe['SSL issues'] = 'unsecure connection enforced'
            else:
                probe['SSL issues'] = 'redirected to secure url'
                r   = requests.get(m.group("url"), headers=fake_headers, verify=False, allow_redirects=False)
                mix = mixed_content(m.group("url"), r.content)
                if (mix['resources'] or mix['images']):
                    probe['mixed content'] = True
                if mix['links']:
                    probe['non-rel links'] = True

        else:
            probe['redirects']    = False
            probe['redirect_url'] = None
            probe['SSL issues']   = 'none found in probe. may still have errors in content'

            # check for mixed content
            mix = mixed_content(url, r.content)
            if (mix['resources']):
                probe['mixed content'] = True
            if mix['links']:
                probe['non-rel links'] = True

    elif str(r.status_code).startswith('3'):
        # 3XX statuses are redirects
        probe['redirects']    = True
        probe['redirect_url'] = r.headers['location']
        parsed_url = urllib3.util.parse_url(r.headers['location'])
        if parsed_url.scheme != 'https':
            probe['SSL issues'] = 'unsecure connections enforced'
        else:
            probe['SSL issues'] = 'redirected to secure url'
    elif (str(r.status_code).startswith('4') or str(r.status_code).startswith('5')):
        # 4XX and 5XX are bad
        probe['redirects']    = False
        probe['redirect_url'] = None
        probe['SSL issues']   = r.reason
    else:
        # some other response outside of 200,3XX,4XX,5XX probably an error
        probe['redirects']    = False
        probe['redirect_url'] = None
        probe['SSL issues']   = r.reason

    return probe


def main(argv):
    import json

    report = []
    for get_capitol_entity in (get_senators, get_representatives, get_cmtes, get_house_minority_cmte, get_leadership, get_support_offices):
        congress_members = get_capitol_entity()
        for member in congress_members:
            result = {}
            result.update(member)

            info = get_cert_info(member['url'])
            if info['cipher'] is None:
                    # no cipher , no ssl
                    print ("ERROR nothing worked for %(name)s %(url)s" % member, file=sys.stderr)
                    result['hostname_match'] = False
                    result['cert_expire']    = None
                    result['cipher algo']    = None
                    result['cipher SSL_ver'] = None
                    result['cipher bits']    = None
                    result['http status']    = None # check for this in html output
                    result['redirects']      = None
                    result['redirect_url']   = None
                    result['SSL issues']     = "unable to make ssl connection"
                    result['mixed content']  = False
                    result['non-rel links']  = False
                    report.append(result)
                    continue
            else:
                result.update(info)

            # go out and actually try to make a request
            probe = make_request(member['url'])
            result.update(probe)

            report.append(result)
    print (json.dumps(report, indent=4, sort_keys=True))

import sys
if __name__ == "__main__":
    main(sys.argv[1:])
