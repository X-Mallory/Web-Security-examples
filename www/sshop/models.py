import os
import string
import bcrypt
import random
from hashlib import *
from datetime import date

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import FLOAT, VARCHAR, INTEGER
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TEXT

from settings import connect_str

BaseModel = declarative_base()
engine = create_engine(connect_str, echo=True, pool_recycle=3600)
db = scoped_session(sessionmaker(bind=engine))


class Commodity(BaseModel):
    __tablename__ = 'commoditys'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(200), unique=True, nullable=False)
    desc = Column(VARCHAR(500), default='no description')
    amount = Column(INTEGER, default=10)
    price = Column(FLOAT, nullable=False)
    lowPrice = Column(FLOAT, nullable=False)

    def __repr__(self):
        return '<Commodity: %s>' % self.name

    def __price__(self):
        return self.price

class Admin(BaseModel):
    __tablename__ = 'admin'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50))
    password = Column(VARCHAR(60))

    def __repr__(self):
        return '<Admin: %s>' % self.username


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50))
    mail = Column(VARCHAR(50))
    password = Column(VARCHAR(60))
    integral = Column(FLOAT, default=1000)

    def check(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf8'))

    def __repr__(self):
        return '<User: %s>' % self.username

    def pay(self, num):
        res = (self.integral - num) if (self.integral - num) else False
        if res >= 0:
            return res
        else:
            return False

    def __integral__(self):
        return self.integral


class Shopcar(BaseModel):
    __tablename__ ='shopcar'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
class UserInvite(BaseModel):
    __tablename__ = 'user_invited_Times'

    username = Column(TEXT,nullable=False, primary_key=True)
    invitedTime=Column(INTEGER)


    def __repr__(self):
        return '<user_invited_Times: %s>' % self.name

    def __invitedTime__(self):
        return self.invitedTime
#####change 44444
class UserSecKill(BaseModel):
    __tablename__ = 'userSecKillTimes'

    userName = Column(TEXT,nullable=False ,primary_key=True)
    secKillTimes=Column(INTEGER)

    def __repr__(self):
        return '<user_invited_Times: %s>' % self.userName
    def __secKillTimes__(self):
        return  self.secKillTimes


###change 77777
class UserQuetion(BaseModel):
    __tablename__ = 'user_question'

    username = Column(TEXT,nullable=False, primary_key=True)
    question=Column(TEXT)
    answer=Column(TEXT)


    def __repr__(self):
        return '<user_invited_Times: %s>' % self.username

    def __question__(self):
        return self.invitedTime

    def __answer__(self):
        return self.invitedTime

class Message(BaseModel):
    __tablename__ = 'message'

    user = Column(TEXT,nullable=False, primary_key=True)
    str = Column(TEXT)

    def __repr__(self):
        return '<Message: %s>' % self.user

if __name__ == "__main__":
    BaseModel.metadata.create_all(engine)
    for i in xrange(49):
        name = ''.join(random.sample(string.ascii_letters, 16))
        desc = ''.join(random.sample(string.ascii_letters * 5, 100))
        price = random.randint(50, 200)
        lowPrice = price - 20
        db.add(Commodity(name=name, desc=desc, price=price,lowPrice=lowPrice))
    db.commit()
    db.add((User(username='Jack_Ma',mail='ciscn@cis.com',password=bcrypt.hashpw('c56e507eeb34f71fc5070291b0620fe7b73473ba2b611b1e07ccbf5a48550080a8b686a828c0813f60b6c62753ba973a860bfcad3b60953ccab4969795405ca4'.encode('utf8'), bcrypt.gensalt()),integral=1000)))
    db.add((Admin(username='admin', password=md5("ciscn".encode('utf-8')).hexdigest())))
    db.commit()

