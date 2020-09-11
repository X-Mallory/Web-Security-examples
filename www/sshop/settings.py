import os
import time

serverTime=time.time()
saleTime=3600
toSale=10
limit = 10
username = '4uuu'
email = 'i@qvq.im'
debug = True
con_str = '%s' % os.path.join(os.getcwd(), 'sshop.db3')

connect_str = 'sqlite:///%s' % os.path.join(os.getcwd(), 'sshop.db3')
cookie_secret = 'JDIOtOQQjLXklJT/N4aJE.tmYZ.IoK8M0_IHZW448b6exe7p1pysO'