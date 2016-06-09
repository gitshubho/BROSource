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
import os, uuid, sys
import urllib2
import hashlib
from bson.objectid import ObjectId
import re
import pymongo
from utilityFunctions import sendMessage,sendRequestToken, hashingPassword, setUserInfo
import textwrap
import random
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Image

__PROFILEPHOTOS__ = 'static/uploads/profilePhotos/'
__FILES__ = 'static/uploads/files/'
__SIZE__ = 300, 300

db = MotorClient('mongodb://brsrc:brsrc@ds028559.mlab.com:28559/brosource')['brosource']

class MainHandler(RequestHandler):

    @removeslash
    @coroutine
    def get(self):

        userInfo = None
        if bool(self.get_secure_cookie('user')):
            current_id = self.get_secure_cookie('user')
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            userInfo = setUserInfo(userInfo, 'username', 'photo_link')
            #print userInfo

        featured_user= yield db.users.find({},{'username':1,'name':1,'aboutme':1,'services':1,'_id':0}).sort([('rating', -1)]).to_list(length=3)
        recent_user=yield db.users.find({},{'username':1,'name':1,'aboutme':1,'services':1,'_id':0}).sort([('$natural',-1)]).to_list(length=3)

        if len(featured_user) == 0:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name='Dummy',F1_Title='Dummy',F1_Uname='Dummy',F1_Desc='Dummy',S1={'Dummy ':'$0'},
                        F2_Name='Dummy',F2_Title='Dummy',F2_Uname='Dummy',F2_Desc='Dummy',S2={'Dummy ':'$0'},
                        F3_Name='Dummy',F3_Title='Dummy',F3_Uname='Dummy',F3_Desc='Dummy',S3={'Dummy ':'$0'},

                        R1_Name='Dummy',R1_Title='Dummy',R1_Uname='Dummy',R1_Desc='Dummy',S4={'Dummy' : '$0'},
                        R2_Name='Dummy',R2_Title='Dummy',R2_Uname='Dummy',R2_Desc='Dummy',S5={'Dummy' : '$0'},
                        R3_Name='Dummy',R3_Title='Dummy',R3_Uname='Dummy',R3_Desc='Dummy',S6={'Dummy':'$0'})

        elif len(featured_user) == 1:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name=featured_user[0]['name'],F1_Title='Cloud programmer',F1_Uname=featured_user[0]['username'],F1_Desc=featured_user[0]['aboutme'],S1=featured_user[0]['services'],
                        F2_Name='Dummy',F2_Title='Dummy',F2_Uname='Dummy',F2_Desc='Dummy',S2={'Dummy ':'$0'},
                        F3_Name='Dummy',F3_Title='Dummy',F3_Uname='Dummy',F3_Desc='Dummy',S3={'Dummy ':'$0'},

                        R1_Name=recent_user[0]['name'],R1_Title='Cloud programmer',R1_Uname=recent_user[0]['username'],R1_Desc=recent_user[0]['aboutme'],S4=recent_user[0]['services'],
                        R2_Name='Dummy',R2_Title='Dummy',R2_Uname='Dummy',R2_Desc='Dummy',S5={'Dummy' : '$0'},
                        R3_Name='Dummy',R3_Title='Dummy',R3_Uname='Dummy',R3_Desc='Dummy',S6={'Dummy':'$0'})

        elif len(featured_user) == 2:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name=featured_user[0]['name'],F1_Title='Cloud programmer',F1_Uname=featured[0]['username'],F1_Desc=featured[0]['aboutme'],S1=featured[0]['services'],
                        F2_Name=featured[1]['name'],F2_Title='Cloud programmer',F2_Uname=featured[1]['username'],F2_Desc=featured[1]['aboutme'],S2=featured[1]['services'],
                        F3_Name='Dummy',F3_Title='Dummy',F3_Uname='Dummy',F3_Desc='Dummy',S3={'Dummy ':'$0'},

                        R1_Name=recent_user[0]['name'],R1_Title='Cloud programmer',R1_Uname=recent_user[0]['username'],R1_Desc=recent_user[0]['aboutme'],S4=recent_user[0]['services'],
                        R2_Name=recent_user[1]['name'],R2_Title='Cloud programmer',R2_Uname=recent_user[1]['username'],R2_Desc=recent_user[1]['aboutme'],S5=recent_user[1]['services'],
                        R3_Name='Dummy',R3_Title='Dummy',R3_Uname='Dummy',R3_Desc='Dummy',S6={'Dummy':'$0'})

        else:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name=featured[0]['name'],F1_Title='Cloud programmer',F1_Uname=featured[0]['username'],F1_Desc=featured_user[0]['aboutme'],S1=featured_user[0]['services'],
                        F2_Name=featured_user[1]['name'],F2_Title='Cloud programmer',F2_Uname=featured_user[1]['username'],F2_Desc=featured_user[1]['aboutme'],S2=featured_user[1]['services'],
                        F3_Name=featured_user[2]['name'],F3_Title='Cloud programmer',F3_Uname=featured_user[2]['username'],F3_Desc=featured_user[2]['aboutme'],S3=featured_user[2]['services'],

                        R1_Name=recent_user[0]['name'],R1_Title='Cloud programmer',R1_Uname=recent_user[0]['username'],R1_Desc=recent_user[0]['aboutme'],S4=recent_user[0]['services'],
                        R2_Name=recent_user[1]['name'],R2_Title='Cloud programmer',R2_Uname=recent_user[1]['username'],R2_Desc=recent_user[1]['aboutme'],S5=recent_user[1]['services'],
                        R3_Name=recent_user[2]['name'],R3_Title='Cloud programmer',R3_Uname=recent_user[2]['username'],R3_Desc=recent_user[2]['aboutme'],S6=recent_user[2]['services'])

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
                self.redirect('/profile/update')
        else:
            self.redirect('/?credentials=False')

class SignupHandler(RequestHandler):

    @removeslash
    @coroutine
    def post(self):
        username = self.get_argument('username_signup')
        password = self.get_argument('password_signup')
        name = self.get_argument('name')
        email = self.get_argument('emailID')
        result = yield db.users.find_one({'username':username, 'email':email})

        if(bool(result)):
            self.redirect('/?username&email=taken')
        else:
            password=hashingPassword(password)
            password=hashlib.sha256(password).hexdigest()
            now=datetime.now()
            time=now.strftime("%d-%m-%Y %I:%M %p")
            result = yield db.users.insert({'photo_link' : '','username' : username, 'password' : password, 'email' : email, 'name' : name, 'mobile' : '',
                                            'address' : '', 'skills' : [], 'dob': '', 'category' : '', 'certifications' : [], 'education_details' : [],
                                            'signup' : 0, 'aboutme' : '', 'ratings' : 0, 'projects' : [], 'views' : 0, 'services' : [], 'social_accounts' : {}, 'joined_on' : time})
            self.set_secure_cookie('user',str(result))
            self.redirect('/profile/update')

class UpdateProfileHandler(RequestHandler):

    @removeslash
    @coroutine
    def get(self):

        userInfo = None
        if bool(self.get_secure_cookie('user')):
            current_id = self.get_secure_cookie('user')
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            userInfo = setUserInfo(userInfo, 'photo_link', 'name', 'username', 'email', 'dob', 'address', 'skills', 'mobile', 'category', 'services', 'aboutme', 'certifications', 'education_details')
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
        print '\n',__PROFILEPHOTOS__ + cname,'\n'
        fh = open(__PROFILEPHOTOS__ + cname, 'w')
        fh.write(photoInfo['body'])

        dob = self.get_argument('dob')
        address = self.get_argument('address')
        skills = self.get_argument('skills',[]).split(',')
        contact = self.get_argument('mobile')

        services = []
        for service in self.get_argument('services',[]).split('|'):
            temp = service.split(':')
            services.append({'service' : temp[0], 'cost' : temp[1]})

        category = self.get_argument('category')
        aboutme = self.get_argument('aboutme')
        certifications = self.get_argument('certifications',[]).split(',')
        education_details = self.get_argument('education_details',[]).split(',')

        userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
        del(userInfo['password'])

        if userInfo['signup'] == 0:
            result = yield db.users.update({'_id': ObjectId(current_id)}, {'$set':{'photo_link' : __PROFILEPHOTOS__ + cname,'dob' : dob, 'address' : address, 'skills' : skills, 'mobile' : contact, 'services' : services,
                                            'category' : category, 'aboutme' : aboutme, 'certifications' : certifications, 'education_details' : education_details, 'signup' : '1'}})
            message = 'Hey'+userInfo['name']+', Welcome to BroSource! Develop, Work, Earn!'
            sendMessage(contact,message)
        else:
            result = yield db.users.update({'_id': ObjectId(current_id)}, {'$set':{'photo_link' : __PROFILEPHOTOS__ + cname,'dob' : dob, 'address' : address, 'skills' : skills, 'mobile' : contact, 'services' : services,
                                            'category' : category, 'aboutme' : aboutme, 'certifications' : certifications, 'education_details' : education_details}})
        self.redirect('/profile/me?update=True')

class SelfProfileHandler(RequestHandler):

    @coroutine
    @removeslash
    def get(self):
        result_current = result_current_info = None
        userInfo = None
        if bool(self.get_secure_cookie('user')):
            current_id = self.get_secure_cookie('user')
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            print userInfo
            self.render('profile_self.html',result = dict(name='Brosource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie("user"))))
        else:
            self.redirect('/?loggedIn=False')

class UserProfileHandler(RequestHandler):

    @coroutine
    @removeslash
    def get(self, username):
        data = []
        userInfo = None
        userInfo = yield db.users.find_one({'_id' : ObjectId(self.get_secure_cookie('user'))})
        data.append(setUserInfo(userInfo,'username','email','photo_link'))
        userInfo = None

        if username != 'Dummy':

            userInfo = yield db.users.find_one({'username':username})
            if bool(userInfo):
                data.append(json.loads(json_util.dumps(userInfo)))

                if bool(self.get_secure_cookie('user')):
                    self.render('profile_others.html',result= dict(data=data,loggedIn = True))
                else:
                    self.render('profile_others.html',result= dict(data=data,loggedIn = False))
            else:
                self.redirect('/?username=False')
        else:
            userInfo = {}
            self.render('profile_others.html',result= dict(data=data,loggedIn = True))

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
            self.set_secure_cookie('uid', str(userInfo['_id']))
            self.set_secure_cookie('authtoken', str(authToken))
            self.redirect('/')
        else:
            self.redirect('/?username=False')

class AuthTokenHandler(RequestHandler):

    @coroutine
    @removeslash
    def post(self):
        otp = self.get_argument('otp')
        if self.get_secure_cookie('authtoken') == otp:
            self.redirect('/changepswd')
        else:
            self.redirect('/?otp=False')

class ChangePasswordHandler(RequestHandler):

    @removeslash
    def get(self):
        self.render('changepswd.html')

    @coroutine
    @removeslash
    def post(self):
        #userInfo = yield db.users.find_one({'_id':ObjectId()})
        print self.get_secure_cookie('uid')
        npswd = self.get_argument('npswd')
        password=hashingPassword(npswd)
        password=hashlib.sha256(password).hexdigest()
        yield db.users.update({'_id': ObjectId(self.get_secure_cookie('uid'))}, {'$set': {'password': password}})
        self.redirect('/?changepassword=True')

class AddProjectHandler(RequestHandler):

    @coroutine
    @removeslash
    def get(self):
        if not bool(self.get_secure_cookie('user')):
            self.redirect('/?loggedIn=False')
            return

        #now=datetime.now()
        #time=now.strftime("%d-%m-%Y %I:%M %p")
        Id = ObjectId(self.get_secure_cookie('user'))
        userInfo = yield db.users.find_one(Id)
        userInfo = setUserInfo(userInfo, 'username', 'email', 'photo_link')
        self.render('add_project.html',data=userInfo)

    @coroutine
    @removeslash
    def post(self):

        user_id = self.get_secure_cookie('user')
        now = datetime.now()
        time = now.strftime("%d-%m-%Y %I:%M %p")

        files_data = []

        for i in range(len(self.request.files['project_file'])):
            fileinfo = self.request.files['project_file'][i]
            fname = fileinfo['filename']
            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn
            fh = open(__FILES__ + cname, 'w')
            fh.write(fileinfo['body'])
            files_data.append({'fname' : fname, 'url' : __FILES__ + cname})

        file_id = yield db.files.insert({'userId' : str(ObjectId(user_id)), 'projId' : "", "files" : files_data})

        insert = yield db.project.insert({'user_id' : str(ObjectId(user_id)), 'name' : self.get_argument('project_title'), 'category' : self.get_argument('project_category'),
                                        'deadline' : self.get_argument('project_deadline'), 'nop' : self.get_argument('nop'), "budget" : self.get_argument('bid_amount'),
                                        'urgent' : self.get_argument('urgent'), 'time'  : time, 'skills' : self.get_argument('skills'), 'description' : self.get_argument('project_description'),
                                        'files' : str(file_id),'bids' : [],'userAwarded' : []})
        userId = ObjectId(user_id)
        yield db.files.update({'_id': file_id},{'$set' : {'projId' : str(insert)}})
        yield db.users.update({'_id': userId},{'$push': {'projects':str(insert)}})
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
        if not bool(self.get_secure_cookie('user')):
            anon= 'Anonymous'
        if (anon=='Anonymous'):
            yield db.donate.insert({'amt':self.get_argument('amt'),'msg':self.get_argument('msg'),'from':anon,'payment received':0})
        else:
            user_id = self.get_secure_cookie('user')
            yield db.donate.insert({'amt':self.get_argument('amt'),'msg':self.get_argument('msg'),'from':str(ObjectId(user_id)),'payment received':0})

class SearchHandler(RequestHandler):

	@coroutine
    	@removeslash
	def post(self):
		STRING = self.get_argument('query')
		word_doc = db.project.find()
		choices = list()
		while(yield word_doc.fetch_next):
			doc = word_doc.next_object()
			try:
				choices.append(doc['name'])
			except:
				continue
		probableMatch = process.extract(STRING, choices, limit = 5)
		choices = list(set(choices))
		projlist = list()
		for LIST in probableMatch:
			if LIST[1] > 70:
				pname = LIST[0]
				if pname in choices:
					choices.remove(pname)
					doc = db.project.find({'name' : pname}, {'name' : 1,'_id' : 1,'bids' : 1})
					while(yield doc.fetch_next):
						wdoc = doc.next_object()
						l1 = list()
						l1.append(wdoc['name'])
						l1.append(wdoc['_id'])
						if 'bids' in wdoc:
							l1.append(wdoc['bids'])
						projlist.append(l1)
		userlist = list()
		word_doc = db.users.find()
		while(yield word_doc.fetch_next):
			doc = word_doc.next_object()
			try:
				choices.append(doc['username'])
			except:
				continue
		probableMatch = process.extract(STRING, choices, limit = 5)
		choices = list(set(choices))

		for LIST in probableMatch:
			if LIST[1]>70:
				pname = LIST[0]
				if pname in choices:
					choices.remove(pname)
					doc = db.users.find({'username' : pname}, {'username' : 1, '_id' : 1, 'category' : 1, 'skills' : 1})
					while(yield doc.fetch_next):
						wdoc = doc.next_object()
						l2 = list()
						try:
							l2.append(wdoc['category'])
						except:
							pass
						try:
							l2.append(wdoc['skills'])
						except:
							pass
						userlist.append(l2)
		self.render('searchresult.html', projlist = projlist, userlist = userlist)

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
    (r"/forgot/getToken", ForgotPasswordHandler),
    (r"/forgot/verifyToken", AuthTokenHandler),
    (r"/changepswd", ChangePasswordHandler),
    (r"/addproj", AddProjectHandler),
    (r"/viewproject/(\w+)", ViewProjectHandler),
    (r"/donate", Donate),
    (r"/search",SearchHandler)
], **settings)

#main init
if __name__ == "__main__":
	server = HTTPServer(application)
	server.listen(5000)
	IOLoop.current().start()
