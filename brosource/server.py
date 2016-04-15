#Tornado Libraries
from tornado.ioloop import IOLoop
from tornado.escape import json_encode
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine

#Other Libraries
import urllib
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
	@coroutine
	def post(self):
		db = self.settings['db']
		username = self.get_argument("username")
		password = self.get_argument("password")
		result = yield db.users.find_one({'username':username,'password':password})
		if bool(result):
			self.set_secure_cookie("user", str(result['_id']))
			self.redirect("/profile")
		else:
			self.redirect("/?status=False")

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
        else:
            self.redirect('/?status=False')
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
            result = yield db.users.insert({'username':username,'password':password,'email':email, 'name':name,'mobile':'','address':'','skills':[]})
            self.set_secure_cookie('user',str(result))
            self.redirect('/welcome')
            print bool(self.get_secure_cookie("user"))

class updateProfileHandler(RequestHandler):
    @coroutine
    @removeslash
    def post(self):
        db = self.settings['db']
        current_id = self.get_secure_cookie("user")
        skills = self.get_argument('skills',[]).split(',')
        address = self.get_argument('address', '')
        contact = self.get_argument('mobile')
        userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
        result = yield db.users.update({'_id': ObjectId(current_id)}, {'$set':{'address': address,'mobile':contact,'skills':skills}})
        message = 'Hey'+userInfo['name']+', Welcome to BroSource! Develop, Work, Earn!'
        sendMessage(contact,message)
        self.redirect('/profile?update=True')
        

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
        else:
            self.redirect('/?loggedIn=False')
class logoutHandler(RequestHandler):
    @removeslash
    @coroutine
    def get(self):
        self.clear_cookie('user')
        self.redirect('/?loggedOut=true')


'''
I am creating some functions over here. Please create a new module, copy the following functions into that module. 
Import the module into this file and remove functions from this file.
'''
def sendMessage(number,message):

    authkey = "81434A3rGba9dY75583ac07" # Your authentication key.
    mobiles = number # Multiple mobiles numbers separated by comma.
    message = message # Your message to send.
    sender = "BROSRC" # Sender ID,While using route4 sender id should be 6 characters long.
    route = "transactional" # Define route
    # Prepare you post parameters
    values = {
              'authkey' : authkey,
              'mobiles' : mobiles,
              'message' : message,
              'sender' : sender,
              'route' : route
              }
    url = "https://control.msg91.com/api/sendhttp.php" # API URL
    postdata = urllib.urlencode(values) # URL encoding the data here.
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    # output = response.read() # Get Response
    # print output # Print Response

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
    (r"/welcome",onBoardingHandler),
    (r"/update",updateProfileHandler)
], **settings)

#main init
if __name__ == "__main__":
	server = HTTPServer(application)
	server.listen(5000)
	IOLoop.current().start()
