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
import os, uuid
import urllib2
import hashlib
from bson.objectid import ObjectId
import re
import pymongo
from utilityFunctions import sendMessage,sendRequestToken, hashingPassword, setUserInfo
import textwrap
import random
from datetime import datetime

__PROFILEPHOTOS__ = "uploads/profilePhotos"
__FILES__ = "uploads/files"

db = MotorClient('mongodb://brsrc:brsrc@ds028559.mlab.com:28559/brosource')['brosource']

class MainHandler(RequestHandler):

    @removeslash
    @coroutine
    def get(self):

        userInfo = None
        if bool(self.get_secure_cookie('user')):
            current_id = self.get_secure_cookie('user')
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            userInfo = setUserInfo(userInfo, 'username')
            #print userInfo

        featured= yield db.users.find({},{'name':1,'aboutme':1,'services':1,'_id':0}).sort([('rating', -1)]).to_list(length=3)
        recent=yield db.users.find({},{'name':1,'aboutme':1,'services':1,'_id':0}).sort([('$natural',-1)]).to_list(length=3)

        try:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name=featured[0]['name'],F1_Title='Cloud programmer',F1_Desc=featured[0]['aboutme'],S1=featured[0]['services'],
                        F2_Name=featured[1]['name'],F2_Title='Cloud programmer',F2_Desc=featured[1]['aboutme'],S2=featured[1]['services'],
                        F3_Name=featured[2]['name'],F3_Title='Cloud programmer',F3_Desc=featured[2]['aboutme'],S3=featured[2]['services'],

                        R1_Name=recent[0]['name'],R1_Title='Cloud programmer',R1_Desc=recent[0]['aboutme'],S4=recent[0]['services'],
                        R2_Name=recent[1]['name'],R2_Title='Cloud programmer',R2_Desc=recent[1]['aboutme'],S5=recent[1]['services'],
                        R3_Name=recent[2]['name'],R3_Title='Cloud programmer',R3_Desc=recent[2]['aboutme'],S6=recent[2]['services'])
        except IndexError:
            #print('Index error encountered')
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name='Piyush',F1_Title='Cloud programmer',F1_Desc='I know c++,java,python',S1={'I can do backend in ':'$4'},
                        F2_Name='Piyush',F2_Title='Cloud programmer',F2_Desc='I know c++,java,python',S2={'I can do backend in ':'$4'},
                        F3_Name='Piyush',F3_Title='Cloud programmer',F3_Desc='I know c++,java,python',S3={'I can do backend in ':'$4'},

                        R1_Name='Piyush',R1_Title='Cloud programmer',R1_Desc='I know c++,java,python',S4={'I can do backend in ':'$4'},
                        R2_Name='Piyush',R2_Title='Cloud programmer',R2_Desc='I know c++,java,python',S5={'I can do backend in ':'$4'},
                        R3_Name='Piyush',R3_Title='Cloud programmer',R3_Desc='I know c++,java,python',S6={'I can do backend in ':'$4'}
                        )
        except KeyError:
            #print('key error encountred')
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name='Piyush',F1_Title='Cloud programmer',F1_Desc='I know c++,java,python',S1={'I can do backend in ':'$4'},
                        F2_Name='Piyush',F2_Title='Cloud programmer',F2_Desc='I know c++,java,python',S2={'I can do backend in ':'$4'},
                        F3_Name='Piyush',F3_Title='Cloud programmer',F3_Desc='I know c++,java,python',S3={'I can do backend in ':'$4'},

                        R1_Name='Piyush',R1_Title='Cloud programmer',R1_Desc='I know c++,java,python',S4={'I can do backend in ':'$4'},
                        R2_Name='Piyush',R2_Title='Cloud programmer',R2_Desc='I know c++,java,python',S5={'I can do backend in ':'$4'},
                        R3_Name='Piyush',R3_Title='Cloud programmer',R3_Desc='I know c++,java,python',S6={'I can do backend in ':'$4'}
                        )

class LoginHandler(RequestHandler):

    @removeslash
    @coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        password=hashingPassword(password)
        password=hashlib.sha256(password).hexdigest()
        result = yield db.users.find_one({'username': username, 'password': password})

        if bool(result):
            self.set_secure_cookie('user', str(result['_id']))
            if len(result['dob']) > 0:
                self.redirect('/profile/me')
            else:
                self.redirect('/welcome')
        else:
            self.redirect('/?credentials=False')

"""class OnBoardingHandler(RequestHandler):

    @removeslash
    @coroutine
    def get(self):

        userInfo = None
        if bool(self.get_secure_cookie('user')):
            current_id = self.get_secure_cookie('user')
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            # print userInfo
            self.render('onboarding.html',result = dict(name='Brosource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))))
        else:
            self.redirect('/?loggedIn=False')
"""
class SignupHandler(RequestHandler):

    @removeslash
    @coroutine
    def post(self):
        username = self.get_argument('username_signup')
        password = self.get_argument('password_signup')
        name = self.get_argument('name')
        email = self.get_argument('emailID')
        result = yield db.users.find_one({'username':username, 'email':email})
        #print bool(result)
        if(bool(result)):
            self.redirect('/?username&email=taken')
        else:
            password=hashingPassword(password)
            password=hashlib.sha256(password).hexdigest()
            result = yield db.users.insert({'photo_link' : '','username' : username, 'password' : password, 'email' : email, 'name' : name, 'mobile' : '',
                                            'address' : '', 'skills' : [], 'dob': '', 'category' : '', 'certifications' : [], 'education_details' : [],
                                            'signup' : 0, 'aboutme' : '', 'ratings' : 0, 'projects' : [], 'views' : [], 'services' : [], 'social_accounts' : {}})
            self.set_secure_cookie('user',str(result))
            self.redirect('/profile/update')
            #print bool(self.get_secure_cookie('user'))

class UpdateProfileHandler(RequestHandler):

    @removeslash
    @coroutine
    def get(self):

        userInfo = None
        if bool(self.get_secure_cookie('user')):
            current_id = self.get_secure_cookie('user')
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            # print userInfo
            self.render('onboarding.html',result = dict(name='Brosource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))))
        else:
            self.redirect('/?loggedIn=False')

    @coroutine
    @removeslash
    def post(self):
        db = self.settings['db']
        current_id = self.get_secure_cookie('user')

        photoInfo = self.request.files['photo'][0]
        extn = os.path.splitext(photoInfo['filename'])[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__PROFILEPHOTOS__ + cname, 'w')
        fh.write(fileinfo['body'])

        dob = self.get_argument('dob')
        address = self.get_argument('address')
        skills = self.get_argument('skills',[]).split(',')
        contact = self.get_argument('mobile')
        services = self.get_argument('services',[]).split(',')
        category = self.get_argument('category')
        aboutme = self.get_argument('aboutme')
        certifications = self.get_argument('certifications',[]).split(',')
        education_details = self.get_argument('education_details',[]).split(',')

        userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
        del(userInfo['password'])

        if userInfo['signup'] == 0:
            result = yield db.users.update({'_id': ObjectId(current_id)}, {'$set':{'dob' : dob, 'address' : address, 'skills' : skills, 'mobile' : contact, 'services' : services,
                                            'category' : category, 'aboutme' : aboutme, 'certifications' : certifications, 'education_details' : education_details, 'signup' : '1'}})
            message = 'Hey'+userInfo['name']+', Welcome to BroSource! Develop, Work, Earn!'
            sendMessage(contact,message)
        else:
            result = yield db.users.update({'_id': ObjectId(current_id)}, {'$set':{'dob' : dob, 'address' : address, 'skills' : skills, 'mobile' : contact, 'services' : services,
                                            'category' : category, 'aboutme' : aboutme, 'certifications' : certifications, 'education_details' : education_details}})
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

    @coroutine
    @removeslash
    def post(self):
        userName = self.get_argument('username','')
        userInfo = yield db.users.find_one({'username': userName})
        if(userInfo):
            authToken = random.randint(10000,99999)
            contact = userInfo['mobile']
            sendRequestToken(contact, authToken)
            self.set_secure_cookie("uid", str(userInfo['_id']))
            self.set_secure_cookie("authtoken", str(authToken))
            self.redirect('/')
        else:
            self.redirect('/forgot/authToken?username=False')

class AuthTokenHandler(RequestHandler):

    @coroutine
    @removeslash
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
        password=hashingPassword(npswd)
        password=hashlib.sha256(password).hexdigest()
        yield db.users.update({'_id': ObjectId(self.get_secure_cookie('uid'))}, {'$set': {'password': password}})
        self.redirect("/?changepassword=True")

class AddProjectHandler(RequestHandler):

    @coroutine
    @removeslash
    def get(self):
        if not bool(self.get_secure_cookie("user")):
            self.redirect('/?login=False')
            return

        #now=datetime.now()
        #time=now.strftime("%d-%m-%Y %I:%M %p")
        Id = ObjectId(self.get_secure_cookie("user"))
        userInfo = yield db.users.find_one(Id)
        userInfo = setUserInfo(userInfo, 'username', 'email')
        self.render('add_project.html',data=userInfo)

    @coroutine
    @removeslash
    def post(self):

        user_id = self.get_secure_cookie("user")
        now = datetime.now()
        time = now.strftime("%d-%m-%Y %I:%M %p")
        insert = yield db.project.insert({"user_id" : str(ObjectId(user_id)), "name" : self.get_argument('project_title'), "category" : self.get_argument('project_category'),
                                        "deadline" : self.get_argument('project_deadline'), "nop" : self.get_argument('nop'), "budget" : self.get_argument('bid_amount'),
                                        "urgent" : self.get_argument('urgent'), "time" : time,"skills" : self.get_argument('skills[]'), "description" : self.get_argument('project_description'),
                                        "files" : [],"bids" : [],"userAwarded" : []})
        userId = ObjectId(user_id)
        yield db.users.update({'_id': userId},{'$push':{"projects":str(insert)}})
        if bool (insert):
            pass
        self.redirect('/viewproject/'+str(insert))
        return

class ViewProjectHandler(RequestHandler):

    @coroutine
    @removeslash
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

class Donate(RequestHandler):

    @removeslash
    def get(self):
        self.render('donate.html')

    @coroutine
    @removeslash
    def post(self):
        anon=self.get_argument('anonymous')
        if not bool(self.get_secure_cookie("user")):
            anon= "Anonymous"
        if (anon=='Anonymous'):
            yield db.donate.insert({'amt':self.get_argument('amt'),'msg':self.get_argument('msg'),'from':anon,'payment received':0})
        else:
            user_id = self.get_secure_cookie("user")
            yield db.donate.insert({'amt':self.get_argument('amt'),'msg':self.get_argument('msg'),'from':str(ObjectId(user_id)),'payment received':0})

"""class BidHandler(RequestHandler):"""

class LogoutHandler(RequestHandler):
    @removeslash
    @coroutine
    def get(self):
        if bool(self.get_secure_cookie('user')):
            self.clear_cookie('user')
            self.redirect('/?loggedOut=true')
        else:
            self.redirect('/?activesession=false')

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
    (r"/profile/update",UpdateProfileHandler),
    (r"/login", LoginHandler),
    (r"/logout",LogoutHandler),
    (r"/profile/me", SelfProfileHandler),
    (r"/profile/(\w+)",UserProfileHandler),
    #(r"/welcome",OnBoardingHandler),
    (r"/forgot/getToken", ForgotPasswordHandler),
    (r"/forgot/verifyToken", AuthTokenHandler),
    (r"/changepswd", ChangePasswordHandler),
    (r"/addproj", AddProjectHandler),
    (r"/viewproject/(\w+)", ViewProjectHandler),
    (r"/donate", Donate)
], **settings)

#main init
if __name__ == "__main__":
	server = HTTPServer(application)
	server.listen(5000)
	IOLoop.current().start()
