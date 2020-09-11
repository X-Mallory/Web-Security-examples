import tornado.web
import hashlib
from sqlalchemy.orm.exc import NoResultFound
from tornado import escape
import sqlite3

from sshop.base import BaseHandler
from sshop.models import Message
from sshop.models import User, UserInvite, UserQuetion, UserSecKill
import bcrypt
from sshop.settings import *
con = sqlite3.connect(con_str)
cursor = con.cursor()

class MessageHanlder(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        sql = "select * from message;"
        messages = cursor.execute(sql).fetchall()
        # messages = self.orm.query(Message).all()
        print messages
        return self.render('message.html',messages= messages)

    def post(self):

        user = self.current_user

        str  = self.get_argument('msg')
        self.orm.add(Message(user=user,str=str))
        self.orm.commit()
        sql = "select * from message;"
        messages = cursor.execute(sql).fetchall()
        return self.render('message.html',messages= messages)