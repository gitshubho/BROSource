#Tornado Libraries
from tornado.ioloop import IOLoop
from tornado.escape import json_encode
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine

#Other Libraries
import urllib
from passlib.hash import sha256_crypt as scrypt
from motor import MotorClient
from bson import json_util
import json
import requests
import os
import urllib2
import hashlib
from bson.objectid import ObjectId
import re
import pymongo
from utilityFunctions import sendMessage,sendRequestToken
import textwrap
import random
from datetime import datetime

db = MotorClient('mongodb://brsrc:brsrc@ds028559.mlab.com:28559/brosource')['brosource']

class MainHandler(RequestHandler):

    @removeslash
    @coroutine
    def get(self):

        userInfo = None
        if bool(self.get_secure_cookie("user")):
            current_id = self.get_secure_cookie("user")
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            # print userInfo
        self.render("index.html",result = dict(name="BroSource",userInfo=userInfo,loggedIn = bool(self.get_secure_cookie("user"))))

class LoginHandler(RequestHandler):

	@removeslash
	@coroutine
	def post(self):

            username = self.get_argument("username")
	    password = self.get_argument("password")

            result = yield db.users.find_one({'username':username,'password':password})

	    if bool(result):
	        self.set_secure_cookie("user", str(result['_id']))
                if len(result["dob"]) > 0:
                    self.redirect("/profile/me")
                else:
                    self.redirect("/welcome")
            else:
	        self.redirect("/?status=False")

class OnBoardingHandler(RequestHandler):

    @removeslash
    @coroutine
    def get(self):

        userInfo = None
        if bool(self.get_secure_cookie("user")):
            current_id = self.get_secure_cookie("user")
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            # print userInfo
            self.render("onboarding.html",result = dict(name="Brosource",userInfo=userInfo,loggedIn = bool(self.get_secure_cookie("user"))))
        else:
            self.redirect('/?status=False')

class SignupHandler(RequestHandler):
    @removeslash
    @coroutine
    def post(self):
        username = self.get_argument('username_signup')
        password = self.get_argument('password_signup')
        name = self.get_argument('name')
        email = self.get_argument('emailID')
        result = yield db.users.find_one({"username":username, "email":email})
        print bool(result)
        if(bool(result)):
            self.redirect('/?username&email=taken')
        else:
            result = yield db.users.insert({'username':username,'password':password,'email':email, 'name':name,'mobile':'','address':'','skills':[], "dob": ""})
            self.set_secure_cookie('user',str(result))
            self.redirect('/welcome')
            print bool(self.get_secure_cookie("user"))

class UpdateProfileHandler(RequestHandler):
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
        self.redirect('/profile/me?update=True')

class SelfProfileHandler(RequestHandler):
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

class UserProfileHandler(RequestHandler):

    @coroutine
    def get(self, username):
        data = []
        userInfo = None
        # current_id = self.get_secure_cookie("user")
        # userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
        userData = yield db.users.find_one({'username':username})
        if bool(userData):
            data.append(json.loads(json_util.dumps(userData)))
            print bool(self.get_secure_cookie("user")),"\n"
            if bool(self.get_secure_cookie("user")):
                self.render('profile_others.html',result= dict(data=data,loggedIn = True))
            else:
                self.render('profile_others.html',result= dict(data=data,loggedIn = False))

class ForgotPasswordHandler(RequestHandler):

    def get(self):
        self.render('forgot.html')
    @coroutine
    def post(self):
        userName = self.get_argument('username','')
        userInfo = yield db.users.find_one({'username': userName})
        if(userInfo):
            authToken = random.randint(10000,99999)
            contact = userInfo['mobile']
            sendRequestToken(contact, authToken)
            self.set_secure_cookie("uid", str(userInfo['_id']))
            self.set_secure_cookie("authtoken", str(authToken))
            self.redirect('/forgot/verify')
        else:
            self.redirect('/forgot/authToken?username=False')

class AuthTokenHandler(RequestHandler):

    def get(self):
        self.render('forgot_verify.html')

    def post(self):
        otp = self.get_argument('otp')
        if self.get_secure_cookie('authtoken') == otp:
            self.redirect('/changepswd')
        else:
            self.redirect('/forgot/verify?otp=False')

class ChangePasswordHandler(RequestHandler):

    def get(self):
        self.render('changepswd.html')

    @coroutine
    def post(self):
        #userInfo = yield db.users.find_one({'_id':ObjectId()})
        print self.get_secure_cookie('uid')
        npswd = self.get_argument('npswd')
        yield db.users.update({'_id': ObjectId(self.get_secure_cookie('uid'))}, {'$set': {'password': npswd}})

class AddProjectHandler(RequestHandler):

    @coroutine
    @removeslash
    def get(self):
        if not bool(self.get_secure_cookie("user")):
            self.redirect('/?login=False')
            return
        now=datetime.now()
        time=now.strftime("%d-%m-%Y %I:%M %p")
        Id = ObjectId(self.get_secure_cookie("user"))
        user=yield db.users.find_one(Id)

        self.render('addproject.html',time=time,user=user['username'])

    @coroutine
    @removeslash
    def post(self):

        user_id = self.get_secure_cookie("user")
        now = datetime.now()
        time = now.strftime("%d-%m-%Y %I:%M %p")
        insert = yield db.project.insert({"user_id":str(ObjectId(user_id)),"name":self.get_argument('name'),"category":self.get_argument('category'),"tags" : self.get_argument('tags'),"nop":self.get_argument('nop'),"bid":self.get_argument('bid'),"urgent":self.get_argument('IsUrg'),"time":time,"description":self.get_argument('description')})
        userId = ObjectId(user_id)
        yield db.users.update({'_id': userId},{'$push':{"projectsAdded":str(insert)}})
        if bool (insert):
            pass
        self.redirect('/viewproject/'+str(insert))
        return

class ViewProjectHandler(RequestHandler):

    @coroutine
    def get(self, projId):
        data = []
        projData = yield db.project.find_one({'_id': ObjectId(projId)})
        userData = yield db.users.find_one({'_id' : ObjectId(projData['user_id'])})
        if bool(projData):
            data.append(json.loads(json_util.dumps(projData)))
            #print bool(self.get_secure_cookie("user")),"\n"
            #if bool(self.get_secure_cookie("user")):
            self.render('viewproject.html',result= dict(data=data, user = userData['username'],loggedIn = True))
            #else:
                #self.render('profile_others.html',result= dict(data=data,loggedIn = False))

class LogoutHandler(RequestHandler):
    @removeslash
    @coroutine
    def get(self):
        self.clear_cookie('user')
        self.redirect('/?loggedOut=true')

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
    (r"/signup", SignupHandler),
    (r"/login", LoginHandler),
    (r"/logout",LogoutHandler),
    (r"/profile/me", SelfProfileHandler),
    (r"/profile/(\w+)",UserProfileHandler),
    (r"/welcome",OnBoardingHandler),
    (r"/update",UpdateProfileHandler),
    (r"/forgot/authToken", ForgotPasswordHandler),
    (r"/forgot/verify", AuthTokenHandler),
    (r"/changepswd", ChangePasswordHandler),
    (r"/addproj", AddProjectHandler),
    (r"/viewproject/(\w+)", ViewProjectHandler)
], **settings)

#main init
if __name__ == "__main__":
	server = HTTPServer(application)
	server.listen(5000)
	IOLoop.current().start()
