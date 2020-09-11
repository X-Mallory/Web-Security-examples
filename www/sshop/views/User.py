# coding=utf-8
import tornado.web
import hashlib
from sqlalchemy.orm.exc import NoResultFound
from tornado import escape
import sqlite3


from sshop.base import BaseHandler
from sshop.models import User, UserInvite, UserQuetion, UserSecKill
import bcrypt
from sshop.settings import *
con = sqlite3.connect(con_str)
cursor = con.cursor()



class UserLoginHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('login.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self):
        # if not self.check_captcha():
        #     return self.render('login.html', danger=1, ques=self.application.question, uuid=self.application.uuid)
        username = self.get_argument('username')
        password = self.get_argument('password')
        mode = self.get_argument('mode', default='user')
        if mode == 'user':
            if username and password:
             try:
                hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                sql = "SELECT * FROM USER where username = '" + username + "'and password = '" + hash_password + "';"
                print sql
                my_user = cursor.execute(sql).fetchone()
                print my_user
                con.commit()
                if my_user:

                    try:
                        self.set_secure_cookie('username', my_user[1])
                        self.redirect('/user')
                    except:
                        pass
                else:
                    return self.render('login.html', danger=1, ques=self.application.question,
                                       uuid=self.application.uuid)

             except NoResultFound:
                return self.render('login.html', danger=1, ques=self.application.question,
                                   uuid=self.application.uuid)

        else:
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            sql = "SELECT * FROM ADMIN where username = '" + username + "'and password = '" + hash_password + "';"
            print sql
            my_user = cursor.execute(sql).fetchone()
            con.commit()
            if my_user:
                try:
                    self.set_secure_cookie('username', my_user[1])
                    self.redirect('/user')
                except:
                    pass
            else:
                return self.render('login.html', danger=1, ques=self.application.question,
                                       uuid=self.application.uuid)



              #  print create_signed_value(selfNone, 'username', 'aaa', version=None,
               # a=UserLoginHanlder(BaseHandler(tornado.web.RequestHandler))
                #print escape.native_str(a.create_signed_value('username', 'aaa',version=None))                                         #    key_version="JDIOtOQQjLXklJT/N4aJE.tmYZ.IoK9M0_IHZW448b6exe7p1pysO")
                #self.create_signed_value('username', 'aaa',version=None)
               # print self.create_signed_value('username', 'aaa',version=None)
              #  print self.get_secure_cookie('usename')
              #  print self.decode_signed_value('username', 'aaa', version = None)
                ###change11
               # self.set_cookie('username', user.username)


class RegisterHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('register.html', ques=self.application.question, uuid=self.application.uuid)

    def post(self, *args, **kwargs):
        if not self.check_captcha():
            return self.render('login.html', danger=1)
        username = self.get_argument('username')
        mail = self.get_argument('mail')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        invite_user = self.get_argument('invite_user')

        #####change 7777777

        quetion = self.get_argument('question',default='111')
        answer = self.get_argument('answer',default='111')
        if password != password_confirm:
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid)

        if mail and username and password and quetion and answer:
            try:
                user = self.orm.query(User).filter(User.username == username).one()
            except NoResultFound:
                self.orm.add(User(username=username, mail=mail,
                                  password=hashlib.sha256(password.encode('utf-8')).hexdigest()))
                ##### change666
                self.orm.add(UserInvite(username=username, invitedTime=0))
                self.orm.add(UserSecKill(userName=username,secKillTimes=0))
                ##### change666

                ###change 777
                self.orm.add(UserQuetion(username=username, question=quetion,answer=answer))
                ###change 777
                self.orm.commit()
                try:
                    ###666
                  if not invite_user == username:

                     inviteUser = self.orm.query(User).filter(User.username == invite_user).one()

                     ####change 666
                     try:
                        invite_user_Times=self.orm.query(UserInvite).filter(UserInvite.username == invite_user).one()
                        print 222
                        if invite_user_Times.invitedTime<5:
                          ####change 666
                             inviteUser.integral += 10
                             invite_user_Times.invitedTime+=1
                     ####change 666
                     except NoResultFound:
                         pass
                     self.orm.commit()
                except NoResultFound:
                    pass
                print 1111
                self.redirect('/login')
        else:
            return self.render('register.html', danger=1, ques=self.application.question, uuid=self.application.uuid)


class ResetPasswordHanlder(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        #####change 7777
        username = self.current_user

        user_question = self.orm.query(UserQuetion).filter(UserQuetion.username == username).one()

        return self.render('reset.html', ques=self.application.question, uuid=self.application.uuid,question=user_question.question,username=username)
         #####change 77777

    def post(self, *args, **kwargs):
        if not self.check_captcha():
            username = self.current_user

            user_question = self.orm.query(UserQuetion).filter(UserQuetion.username == username).one()
            question=user_question.question
            self.clear_cookie('username')
            return self.render('reset.html', danger=1, ques=self.application.question, uuid=self.application.uuid,question=question,username=username)
        #####77777
        usr_answer = self.get_argument('answer')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')

        username = self.current_user
        user_question = self.orm.query(UserQuetion).filter(UserQuetion.username == username).one()
        question = user_question.question
        user = self.orm.query(User).filter(User.username == username).one()
        answer = user_question.answer


        if password != password_confirm:
            self.clear_cookie('username')
            return self.render('reset.html', danger=1, ques=self.application.question, uuid=self.application.uuid,question=question,username=username)
        if answer != usr_answer:
            self.clear_cookie('username')
            return self.render('reset.html', danger=1, ques=self.application.question, uuid=self.application.uuid,question=question,username=username)
        else:
           user.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
           self.orm.commit()
           self.clear_cookie('username')
           return self.redirect('/login')

        ######77777
class ResetHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.application._generate_captcha()
        return self.render('reset_1.html',ques=self.application.question, uuid=self.application.uuid)

    def post(self, *args, **kwargs):
        try:
            usr_mail = self.get_argument('mail')

            if usr_mail:
                return self.render('reset_1.html', success=1)
        except:
         username = self.get_argument('username')
         try:
             user = self.orm.query(User).filter(User.username == username).one()



             self.set_secure_cookie('username', username)

             self.redirect('/reset_1')
         except NoResultFound:
             return self.render('reset_1.html', danger=1)


   ####change77777

class changePasswordHandler(BaseHandler):
    def get(self):
        return self.render('change.html')

    def post(self, *args, **kwargs):
        old_password = self.get_argument('old_password')
        password = self.get_argument('password')
        password_confirm = self.get_argument('password_confirm')
        print old_password, password, password_confirm
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        if password == password_confirm:
            if user.check(old_password):
                user.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
                self.orm.commit()
                return self.render('change.html', success=1)
        return self.render('change.html', danger=1)


class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        print user
        ###change flag
        with open('flag1.txt','r') as f:
            flag=f.read()
        if self.current_user == 'Jack_Ma':
           return self.render('user.html', user=user,flag=flag)
        else:
            return self.render('user.html', user=user,flag='null')


class UserLogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.clear_cookie('username')
        self.redirect('/login')


# change 333
class KeyHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render('key.txt')

class TestHandler(BaseHandler):
    def get(self,*args, **kwarg):
        parameter = self.get_argument('parameter')
        sql = "SELECT * FROM USER where username = '" + parameter + "';"
        print sql
        result = cursor.execute(sql).fetchall()
        print str(result)
        return self.render('test.html', info = result)