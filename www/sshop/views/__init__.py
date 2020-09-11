from Shop import *
from User import *
from Captcha import *
from Message import MessageHanlder

handlers = [

    (r'/', ShopIndexHandler),
    (r'/shop', ShopListHandler),
    (r'/info/(\d+)', ShopDetailHandler),
    (r'/seckill', SecKillHandler),
    (r'/shopcar', ShopCarHandler),
    (r'/shopcar/add', ShopCarAddHandler),
    (r'/shopcar/addSec', ShopSecKillCarAddHandler),
    (r'/pay', ShopPayHandler),
    (r'/sale',SecKillHandler1),

    (r'/captcha', CaptchaHandler),
    (r'/key.txt', KeyHandler),


    (r'/user', UserInfoHandler),
    (r'/test', TestHandler),
    (r'/user/change', changePasswordHandler),
    #(r'/pass/reset', ResetPasswordHanlder),
    (r'/pass/reset', ResetHandler),
    (r'/reset_1', ResetPasswordHanlder),



    (r'/login', UserLoginHanlder),
    (r'/logout', UserLogoutHandler),
    (r'/register', RegisterHandler),
    (r'/Message', MessageHanlder)
]