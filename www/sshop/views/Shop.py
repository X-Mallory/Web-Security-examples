# coding=utf-8
import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User, UserSecKill
from sshop.settings import limit,toSale,serverTime,saleTime


class ShopIndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.redirect('/shop')


class ShopListHandler(BaseHandler):
    def get(self):
        page = self.get_argument('page', 1)
        page = int(page) if int(page) else 1
        commoditys = self.orm.query(Commodity) \
            .filter(Commodity.amount > 0) \
            .order_by(Commodity.price.desc()) \
            .limit(limit).offset((page - 1) * limit).all()
        return self.render('index.html', commoditys=commoditys, preview=page - 1, next=page + 1, limit=limit, startTime =serverTime, toSale = toSale,saleTime=saleTime)


class ShopDetailHandler(BaseHandler):
    def get(self, id=1):
        try:
            commodity = self.orm.query(Commodity) \
                .filter(Commodity.id == int(id)).one()
        except NoResultFound:
            return self.redirect('/')
        return self.render('info.html', commodity=commodity)


class ShopPayHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        try:
            ciscn = " "
            price = self.get_argument('price')
            id = self.get_argument("cid", default=1)
            advice = self.get_argument("advice", default='Good')
            # advice = advice.replace("<script>", "", 1)
            # advice = advice.replace("</script>", "", 1)
            # advice = advice.replace("CISCN", "", 1)
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            commnuity = self.orm.query(Commodity).filter(Commodity.id == id).one()
            integ = user.pay(float(price))
            if integ != False and commnuity.amount > 0:
                user.integral = integ
                self.orm.commit()
                commnuity.amount -= 1
                self.orm.commit()
                #if '<script>' in advice and '</script>' in advice and 'CISCN' in advice:
                print "********"
                print advice
                return self.render('pay.html', success=1, ciscn=ciscn, user=user.username, advice=advice)
                #else:
                #    return self.render('pay.html', success=1, user=user.username, advice=advice)
            else:
                return self.render('pay.html', danger=1)
        except:
            return self.render('pay.html', danger=1)


class ShopCarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        id = self.get_secure_cookie('commodity_id')
        price = self.get_secure_cookie('shop_price')
        if id:
            commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
            if price==None:
                price=commodity.price
            return self.render('shopcar.html', commodity=commodity,price=price)
        return self.render('shopcar.html')

    @tornado.web.authenticated
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        try:
            price = self.get_argument('price')
            cid = self.get_argument('cid', default="none")
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            if cid == 'none':
                res = user.pay(float(price))
            else:
                good = self.orm.query(Commodity).filter(Commodity.id == cid).one()
                if good.amount > 0:
                    if (float(price)==good.price):
                        res = user.pay(float(good.price))
                    elif(float(price)==good.lowPrice):
                        res=user.pay(float(good.lowPrice))
                    else:
                        self.clear_cookie('commodity_id')
                        self.clear_cookie('shop_price')
                        return self.render('shopcar.html')
                    good.amount -= 1
                else:
                    res = False
            if res:
                user.integral = res
                self.orm.commit()
                self.clear_cookie('commodity_id')
                self.clear_cookie('shop_price')
                return self.render('shopcar.html', success=1)
        except Exception as ex:
            print str(ex)
        return self.redirect('/shopcar')


class ShopCarAddHandler(BaseHandler):
    def post(self, *args, **kwargs):
        id = self.get_argument('id',default=1)
        self.set_secure_cookie('commodity_id', id)
        return self.redirect('/shopcar')
class ShopSecKillCarAddHandler(BaseHandler):
    def post(self, *args, **kwargs):
        id = self.get_argument('id',default=1)
        price = self.get_argument('price',default=1)
        self.set_secure_cookie('commodity_id', id)
        self.set_secure_cookie('shop_price', price)
        try:

            user = self.orm.query(User).filter(User.username == self.current_user).one()
            username=user.username
            try:

                secUser=self.orm.query(UserSecKill).filter(UserSecKill.userName==username).one()

                if secUser.secKillTimes<10:
                    secUser.secKillTimes+=1

                else:
                    self.clear_cookie('commodity_id')
                    self.clear_cookie('shop_price')
                    return self.redirect('/shopcar')
                self.orm.commit()
            except NoResultFound:
                pass

        except NoResultFound:
            pass
        return self.redirect('/shopcar')
class SecKillHandler1(BaseHandler):
    def get(self, *args, **kwargs):
        page = self.get_argument('page', 1)
        page = int(page) if int(page) else 1
        commoditys = self.orm.query(Commodity) \
            .filter(Commodity.amount > 0) \
            .order_by(Commodity.price.desc()) \
            .limit(limit).offset((page - 1) * limit).all()
        return self.render('sale.html', commoditys=commoditys, preview=page - 1, next=page + 1, limit=limit,startTime =serverTime, toSale = toSale,saleTime=saleTime)
class SecKillHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.render('seckill.html')

    def post(self, *args, **kwargs):
        try:
            id = self.get_argument('id')
            commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
            commodity.amount -= 1
            self.orm.commit()
            return self.render('seckill.html', success=1)
        except:
            return self.render('seckill.html', danger=1)
