#Tornado Libraries
from tornado.ioloop import IOLoop
from tornado.escape import json_encode
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine

#Other Libraries
from motor import MotorClient
import json
import requests
import os
import urllib2
import hashlib
from bson.objectid import ObjectId
import re
import pymongo

db = MotorClient()['brosource']

class MainHandler(RequestHandler):
    @removeslash
    @coroutine
    def get(self):
        result_current = result_current_info = None
        userInfo = None
        if bool(self.get_secure_cookie("user")):
            current_id = self.get_secure_cookie("user")
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            print userInfo
        self.render("index.html",result = dict(name="BroSource",userInfo=userInfo,loggedIn = bool(self.get_secure_cookie("user"))))

class loginHandler(RequestHandler):
	@removeslash
	def get(self):
	        if bool(self.get_secure_cookie("user")):
	                self.redirect("/")
                self.render("login.html")

	@removeslash
	@coroutine
	def post(self):
		db = self.settings['db']
		username = self.get_argument("username")
		password = self.get_argument("password")
		result = yield db.users.find_one({'username':username,'password':password})
		if bool(result):
			self.set_secure_cookie("user", str(result['_id']))
			self.redirect("/")
		else:
			self.redirect("/login?status=False")

#Onboarding Handler. Once the user signs up, we will show him onboarding.(One time only)

class onBoardingHandler(RequestHandler):
    @removeslash
    @coroutine
    def get(self):
        result_current = result_current_info = None
        userInfo = None
        if bool(self.get_secure_cookie("user")):
            current_id = self.get_secure_cookie("user")
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            print userInfo
        self.render("onboarding.html",result = dict(name="Brosource",userInfo=userInfo,loggedIn = bool(self.get_secure_cookie("user"))))
class signupHandler(RequestHandler):
    @removeslash
    @coroutine
    def post(self):
        username = self.get_argument('username_signup')
        password = self.get_argument('password_signup')
        name = self.get_argument('name')
        email = self.get_argument('emailID')
        result = yield db.users.find_one({"username":username})
        print bool(result)
        if(bool(result)):
            self.redirect('/?username=taken')
        else:
            result = yield db.users.insert({'username':username,'password':password,'email':email, 'name':name})
            self.set_secure_cookie('user',str(result))
            self.redirect('/welcome')
            print bool(self.get_secure_cookie("user"))
class profileHandler(RequestHandler):
    @coroutine
    @removeslash
    def get(self):
        result_current = result_current_info = None
        userInfo = None
        if bool(self.get_secure_cookie("user")):
            current_id = self.get_secure_cookie("user")
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            print userInfo
        self.render("profile_self.html",result = dict(name="Brosource",userInfo=userInfo,loggedIn = bool(self.get_secure_cookie("user"))))
class logoutHandler(RequestHandler):
    @removeslash
    @coroutine
    def get(self):
        self.clear_cookie('user')
        self.redirect('login?loggedOut=true')

settings = dict(
		db=db,
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		debug=True,
		cookie_secret="35an18y3-u12u-7n10-4gf1-102g23ce04n6"
	)

#Application initialization
application = Application([
	(r"/", MainHandler),
    (r"/signup", signupHandler),
    (r"/login", loginHandler),
    (r"/logout",logoutHandler),
    (r"/profile", profileHandler),
    (r"/welcome",onBoardingHandler)
], **settings)

#main init
if __name__ == "__main__":
	server = HTTPServer(application)
	server.listen(8001)
	IOLoop.current().start()
