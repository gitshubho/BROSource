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
from utilityFunctions import sendMessage,sendRequestToken, hashingPassword, setUserInfo,getSkills
import textwrap
import random
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from PIL import Image

__PROFILEPHOTOS__ = 'static/uploads/profilePhotos/'
__FILES__ = 'static/uploads/files/'
__SIZE__ = 300, 300

db = MotorClient('mongodb://brsrc:brsrc@ds028559.mlab.com:28559/brosource')['brosource']
#db=MotorClient().brosource
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

        projects = yield db.project.find({},{'name':1,'description':1,'skills':1,'_id':1}).sort([('$natural',-1)]).to_list(length=6)

        featured_user = yield db.users.find({},{'username':1,'name':1,'aboutme':1,'services':1,'category':1,'photo_link':1,'_id':0}).sort([('ratings', -1)]).to_list(length=3)

        recent_user = yield db.users.find({},{'username':1,'name':1,'aboutme':1,'services':1,'category':1,'photo_link':1,'_id':0}).sort([('$natural',-1)]).to_list(length=3)

        d = {'':"",'1':"Technical",'2':"Management",'3':"Design",'4':"Technical and Management",'5':"Technical and Design",'6':"Design and Management",'7':"Technical, Design and Management"}

        if len(featured_user) == 0:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name = 'Dummy',F1_Title='Dummy',F1_Uname='Dummy',F1_Desc='Dummy',S1=[{'service' :'Dummy ','cost':'$0'}],
                        F2_Name = 'Dummy',F2_Title='Dummy',F2_Uname='Dummy',F2_Desc='Dummy',S2=[{'service' :'Dummy ','cost':'$0'}],
                        F3_Name = 'Dummy',F3_Title='Dummy',F3_Uname='Dummy',F3_Desc='Dummy',S3=[{'service' :'Dummy ','cost':'$0'}],

                        R1_Name = 'Dummy',R1_Title='Dummy',R1_Uname='Dummy',R1_Desc='Dummy',S4=[{'service' :'Dummy ','cost':'$0'}],
                        R2_Name = 'Dummy',R2_Title='Dummy',R2_Uname='Dummy',R2_Desc='Dummy',S5=[{'service' :'Dummy ','cost':'$0'}],
                        R3_Name = 'Dummy',R3_Title='Dummy',R3_Uname='Dummy',R3_Desc='Dummy',S6=[{'service' :'Dummy ','cost':'$0'}])

        elif len(featured_user) == 1:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name = featured_user[0]['name'],F1_Title='Cloud programmer',F1_Uname=featured_user[0]['username'],F1_Desc=featured_user[0]['aboutme'],S1=featured_user[0]['services'],
                        F2_Name = 'Dummy',F2_Title='Dummy',F2_Uname='Dummy',F2_Desc='Dummy',S2=[{'service' :'Dummy ','cost':'$0'}],
                        F3_Name = 'Dummy',F3_Title='Dummy',F3_Uname='Dummy',F3_Desc='Dummy',S3=[{'service' :'Dummy ','cost':'$0'}],

                        R1_Name = recent_user[0]['name'],R1_Title='Cloud programmer',R1_Uname=recent_user[0]['username'],R1_Desc=recent_user[0]['aboutme'],S4=recent_user[0]['services'],
                        R2_Name = 'Dummy',R2_Title='Dummy',R2_Uname='Dummy',R2_Desc='Dummy',S5=[{'service' :'Dummy ','cost':'$0'}],
                        R3_Name = 'Dummy',R3_Title='Dummy',R3_Uname='Dummy',R3_Desc='Dummy',S6=[{'service' :'Dummy ','cost':'$0'}])

        elif len(featured_user) == 2:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name = featured_user[0]['name'],F1_Title='Cloud programmer',F1_Uname=featured_user[0]['username'],F1_Desc=featured_user[0]['aboutme'],S1=featured_user[0]['services'],
                        F2_Name = featured_user[1]['name'],F2_Title='Cloud programmer',F2_Uname=featured_user[1]['username'],F2_Desc=featured_user[1]['aboutme'],S2=featured_user[1]['services'],
                        F3_Name = 'Dummy',F3_Title='Dummy',F3_Uname='Dummy',F3_Desc='Dummy',S3=[{'service' :'Dummy ','cost':'$0'}],

                        R1_Name = recent_user[0]['name'],R1_Title='Cloud programmer',R1_Uname=recent_user[0]['username'],R1_Desc=recent_user[0]['aboutme'],S4=recent_user[0]['services'],
                        R2_Name = recent_user[1]['name'],R2_Title='Cloud programmer',R2_Uname=recent_user[1]['username'],R2_Desc=recent_user[1]['aboutme'],S5=recent_user[1]['services'],
                        R3_Name = 'Dummy',R3_Title='Dummy',R3_Uname='Dummy',R3_Desc='Dummy',S6=[{'service' :'Dummy ','cost':'$0'}])

        else:
            self.render('index.html',result = dict(name='BroSource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))),
                        F1_Name = featured_user[0]['name'],F1_Title=d[featured_user[0]['category']],F1_Uname=featured_user[0]['username'],F1_Desc=featured_user[0]['aboutme'],S1=featured_user[0]['services'],F1_photo=featured_user[0]['photo_link'],
                        F2_Name = featured_user[1]['name'],F2_Title=d[featured_user[1]['category']],F2_Uname=featured_user[1]['username'],F2_Desc=featured_user[1]['aboutme'],S2=featured_user[1]['services'],F2_photo=featured_user[1]['photo_link'],
                        F3_Name = featured_user[2]['name'],F3_Title=d[featured_user[2]['category']],F3_Uname=featured_user[2]['username'],F3_Desc=featured_user[2]['aboutme'],S3=featured_user[2]['services'],F3_photo=featured_user[2]['photo_link'],

                        R1_Name = recent_user[0]['name'],R1_Title=d[recent_user[0]['category']],R1_Uname=recent_user[0]['username'],R1_Desc=recent_user[0]['aboutme'],S4=recent_user[0]['services'],R1_photo=recent_user[0]['photo_link'],
                        R2_Name = recent_user[1]['name'],R2_Title=d[recent_user[0]['category']],R2_Uname=recent_user[1]['username'],R2_Desc=recent_user[1]['aboutme'],S5=recent_user[1]['services'],R2_photo=recent_user[1]['photo_link'],
                        R3_Name = recent_user[2]['name'],R3_Title=d[recent_user[0]['category']],R3_Uname=recent_user[2]['username'],R3_Desc=recent_user[2]['aboutme'],S6=recent_user[2]['services'],R3_photo=recent_user[2]['photo_link'],
                        projects = projects)

class LoginHandler(RequestHandler):

    @removeslash
    @coroutine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        password = hashingPassword(password)
        password = hashlib.sha256(password).hexdigest()
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
        if not(bool(username) and bool(password) and bool(name) and bool(re.search(r".+@\w+\.(com|co\.in)",email))):
            self.redirect('/?username&email=empty')
            return

        result = yield db.users.find_one({'username':username, 'email':email})
        if(bool(result)):
            self.redirect('/?username&email=taken')
        else:
            password = hashingPassword(password)
            password = hashlib.sha256(password).hexdigest()
            now = datetime.now()
            time = now.strftime("%d-%m-%Y %I:%M %p")
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
            userInfo['skills']=json.dumps(userInfo['skills'])

            self.render('onboarding.html',result = dict(name='Brosource',userInfo=userInfo,loggedIn = bool(self.get_secure_cookie('user'))))
        else:
            self.redirect('/?loggedIn=False')

    @coroutine
    @removeslash
    def post(self):
        db = self.settings['db']
        current_id = self.get_secure_cookie('user')
        email = self.get_argument('email')
        if not bool(re.search(r".+@\w+\.(com|co\.in)",email)):
            self.redirect('/onboarding.html?email=invalid')
            return
        dob = self.get_argument('dob')
        address = self.get_argument('address')
        skills = self.get_argument('skills').split(',')

        #skill_data = []
        #for skill in skills:
        #    temp = yield db.skills.find_one({skill :{'$exists':1}})
        #    skill_data.append(temp[skill])
        contact = self.get_argument('mobile')

        services = []
        try:
            for service in self.get_argument('services').split('|'):
                temp = service.split(':')
                services.append({'service' : temp[0], 'cost' : temp[1]})
        except IndexError:
            services = []

        category = self.get_argument('category')
        aboutme = self.get_argument('aboutme')
        certifications = self.get_argument('certifications',[]).split(',')
        education_details = self.get_argument('education_details',[]).split(',')

        userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
        del(userInfo['password'])

        try:
            import cStringIO
            photoInfo = self.request.files['photo'][0]
            extn = os.path.splitext(photoInfo['filename'])[1]
            cname = str(uuid.uuid4()) + extn
            photo_link = __PROFILEPHOTOS__ + cname
            imgstr = re.search(r'base64,(.*)', self.get_argument('profile_photo')).group(1)
            tempimg = cStringIO.StringIO(imgstr.decode('base64'))
            im = Image.open(tempimg)
            im = im.resize((160,160),Image.ANTIALIAS)
            print im.save(photo_link,optimize=True, quality=95)
        except:
            photo_link = ''


        if userInfo['signup'] == 0:
            result = yield db.users.update({'_id': ObjectId(current_id)}, {'$set':{'photo_link' : photo_link,'email':email,'dob' : dob, 'address' : address, 'skills' : skills, 'mobile' : contact, 'services' : services,
                                            'category' : category, 'aboutme' : aboutme, 'certifications' : certifications, 'education_details' : education_details, 'signup' : '1'}})
            message = 'Hey'+userInfo['name']+', Welcome to BroSource! Develop, Work, Earn!'
            sendMessage(contact,message)
        else:
            result = yield db.users.update({'_id': ObjectId(current_id)}, {'$set':{'photo_link' : photo_link,'email':email,'dob' : dob, 'address' : address, 'skills' : skills, 'mobile' : contact, 'services' : services,
                                            'category' : category, 'aboutme' : aboutme, 'certifications' : certifications, 'education_details' : education_details}})
        self.redirect('/profile/me?update=True')

class SelfProfileHandler(RequestHandler):
    @coroutine
    @removeslash
    def get(self):
        result_current = result_current_info = None
        userInfo = None
        validppl=list()
        validppl1=list()
        if bool(self.get_secure_cookie('user')):
            current_id = self.get_secure_cookie('user')
            userInfo = yield db.users.find_one({'_id':ObjectId(current_id)})
            userInfo['skills']=getSkills(userInfo['skills'])
            print userInfo
            views= yield db.views.aggregate([{'$match':{'profileId':ObjectId(current_id)}},{'$group':{'_id':'$date','count':{'$sum':1}}}]).to_list(length=10)
            print(views)
            validmsg=db.serviceRequests.find({'aliases':{'toid':ObjectId(current_id)},'Service.0.accepted':1})
            if validmsg:
             while (yield validmsg.fetch_next):
                         wdoc = validmsg.next_object()
                         print '\nrecieved requests'
                         print wdoc
                         if wdoc not in validppl1:
                          validppl.append(wdoc)
            validmsg=db.serviceRequests.find({'aliases.0.fromid':ObjectId(current_id),'Service.0.accepted':1})
            if validmsg:
             while (yield validmsg.fetch_next):
                         wdoc = validmsg.next_object()
                         print '\nsent requests'
                         print wdoc
                         if wdoc not in validppl1:
                          validppl1.append(wdoc) 
            msgsReceived=list()
            result=db.messages.find({'aliases':{'toid':ObjectId(current_id)}})
            while(yield result.fetch_next):
                doc=result.next_object()
                msgsReceived.append(doc)
            msgsSent=list()
            result=db.messages.find({'aliases':{'fromid':ObjectId(current_id)}})
            while(yield result.fetch_next):
                doc=result.next_object()
                msgsSent.append(doc)    
            self.render('profile_self.html',msgsReceived=msgsReceived,msgsSent=msgsSent,validppl1=validppl1,validppl=validppl,result = dict(name='Brosource',data=userInfo,loggedIn = bool(self.get_secure_cookie("user"))))
        else:
            self.redirect('/?loggedIn=False')

class UserProfileHandler(RequestHandler):

    @coroutine
    @removeslash
    def get(self, username):
        data = []
        userInfo = None
        validppl=list()
        validppl1=list()
        userInfo = yield db.users.find_one({'_id' : ObjectId(self.get_secure_cookie('user'))})
        current_id=userInfo['_id']
        if bool(self.get_secure_cookie('user')):
            userInfo=setUserInfo(userInfo,'username','email','photo_link')
        data.append(json.loads(json_util.dumps(userInfo)))

        userInfo = None

        if username != 'Dummy':

            userInfo = yield db.users.find_one({'username':username})
            if bool(userInfo):
                userInfo['skills']=getSkills(userInfo['skills'])
                data.append(json.loads(json_util.dumps(userInfo)))
                print(data)
                now=datetime.now()
                date=now.strftime("%d-%m-%Y")
                if bool(self.get_secure_cookie('user')):
                    if (data[0]['username']!= data[1]['username']):

                        viewinsert= yield db.views.update({'profileId':ObjectId(data[1]['_id']['$oid']),'viewerId':self.get_secure_cookie('user'),'date':date},{'profileId':ObjectId(data[1]['_id']['$oid']),'viewerId':self.get_secure_cookie('user'),'date':date},upsert=True)
                    
                    validmsg=db.serviceRequests.find({'aliases':{'toid':current_id},'Service.0.accepted':1})
                    if validmsg:
                     while (yield validmsg.fetch_next):
                                 wdoc = validmsg.next_object()
                                 print '\nrecieved requests'
                                 print wdoc
                                 if wdoc not in validppl:
                                  validppl.append(wdoc)
                    
                    validmsg=db.serviceRequests.find({'aliases.0.fromid':current_id,'Service.0.accepted':1})
                    if validmsg:
                     while (yield validmsg.fetch_next):
                                 wdoc = validmsg.next_object()
                                 print '\nsent requests'
                                 print wdoc
                                 if wdoc not in validppl1:
                                          validppl1.append(wdoc)
                    msgsReceived=list()
                    result=db.messages.find({'aliases':{'toid':ObjectId(current_id)}})
                    while(yield result.fetch_next):
                        doc=result.next_object()
                        msgsReceived.append(doc)
                    msgsSent=list()
                    result=db.messages.find({'aliases':{'fromid':ObjectId(current_id)}})
                    while(yield result.fetch_next):
                        doc=result.next_object()
                        msgsSent.append(doc)    
                    self.render('profile_others.html',msgsReceived=msgsReceived,msgsSent=msgsSent,validppl1=validppl1,validppl=validppl,result= dict(data=data,loggedIn = True))
                else:
                    self.render('profile_others.html',validppl1=validppl1,validppl=validppl,result= dict(data=data,loggedIn = False))
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
        password = hashingPassword(npswd)
        password = hashlib.sha256(password).hexdigest()
        yield db.users.update({'_id': ObjectId(self.get_secure_cookie('uid'))}, {'$set': {'password': password}})
        self.redirect('/?changepassword=True')

class AddProjectHandler(RequestHandler):

    @coroutine
    @removeslash
    def get(self):
        if not bool(self.get_secure_cookie('user')):
            self.redirect('/?loggedIn=False')
            return

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

        try:
            for i in range(len(self.request.files['project_files'])):
                fileinfo = self.request.files['project_files'][i]
                fname = fileinfo['filename']
                extn = os.path.splitext(fname)[1]
                cname = str(uuid.uuid4()) + extn
                fh = open(__FILES__ + cname, 'w')
                fh.write(fileinfo['body'])
                files_data.append({'fname' : fname, 'url' : __FILES__ + cname})

            file_id = yield db.files.insert({'userId' : str(ObjectId(user_id)), 'projId' : "", "files" : files_data})
        except:
            file_id = ''

        insert = yield db.project.insert({'user_id' : str(ObjectId(user_id)), 'name' : self.get_argument('project_title'), 'category' : self.get_argument('project_category'),
                                        'deadline' : self.get_argument('project_deadline'), 'nop' : self.get_argument('nop'), "budget" : self.get_argument('bid_amount'),
                                        'urgent' : self.get_argument('urgent'), 'time'  : time, 'skills' : self.get_argument('skills').split(','), 'description' : self.get_argument('project_description'),
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

        if bool(projData):
            userData = yield db.users.find_one({'_id': ObjectId(self.get_secure_cookie('user'))})
            if bool(self.get_secure_cookie('user')):
                userData = setUserInfo(userData, 'username', 'email', 'photo_link')
            data.append(json.loads(json_util.dumps(userData)))

            data.append(json.loads(json_util.dumps(projData)))

            userData = yield db.users.find_one({'_id' : ObjectId(projData['user_id'])})
            userData = setUserInfo(userData, 'name', 'email', 'address', 'mobile', 'photo_link')
            data.append(json.loads(json_util.dumps(userData)))

            try:
                fileData = yield db.files.find_one({'_id' : ObjectId(projData['files'])})
                data.append(json.loads(json_util.dumps(fileData)))
            except:
                fileData = {}
                data.append(fileData)
            print data
            if bool(data[0]):
                self.render('apply_project.html',result= dict(data=data,loggedIn = True))
            else:
                self.render('apply_project.html',result= dict(data=data,loggedIn = False))

        else:
            self.redirect('/?project=False')

class Donate(RequestHandler):
    @removeslash
    def get(self):
        self.render('donate.html')

    @coroutine
    @removeslash
    def post(self):
        anon=self.get_argument('anonymous')
        if not bool(self.get_secure_cookie('user')):
            anon = 'Anonymous'
        if (anon =='Anonymous'):
            yield db.donate.insert({'amt':self.get_argument('amt'),'msg':self.get_argument('msg'),'from':anon,'payment received':0})
        else:
            user_id = self.get_secure_cookie('user')
            yield db.donate.insert({'amt':self.get_argument('amt'),'msg':self.get_argument('msg'),'from':str(ObjectId(user_id)),'payment received':0})

class SearchHandler(RequestHandler):
    @coroutine
    @removeslash
    def get(self):
        data=list()
        l1 = list()
        l2 = list()
        STRING = self.get_argument('query')
        word_doc = db.project.find()
        choices = list()
        while (yield word_doc.fetch_next):
            doc = word_doc.next_object()
            try:
                choices.append(doc['name'])
            except:
                continue
        #substring check        
        probableMatch = process.extract(STRING, choices, limit=5)
        choices = list(set(choices))
        projlist = list()
        for LIST in probableMatch:
            print LIST[1]
            if LIST[1] >55:
                pname = LIST[0]
                if pname in choices:
                    choices.remove(pname)
               
                    #query must be atleast 1 fifth of the asked project
                    #ratio not used as project names are large                
                    lenstr=len(STRING)
                    lenpname=len(pname)
                    
                    if  not(lenstr<lenpname) and float(lenpname/lenstr)>=0.2:
                        continue
                        
                    doc = db.project.find({'name': pname}, {'name': 1, '_id': 1, 'bids': 1})
                    while (yield doc.fetch_next):
                        wdoc = doc.next_object()
                        l1.append(json_util.dumps(wdoc))
                        #l1 = list()
                        #l1.append(wdoc['name'])
                        #l1.append(wdoc['_id'])
                        #if 'bids' in wdoc:
                        #    l1.append(wdoc['bids'])
                        #projlist.append(l1)
        userlist = list()
        word_doc = db.users.find()
        while (yield word_doc.fetch_next):
            doc = word_doc.next_object()
            try:
                choices.append(doc['username'])
            except:
                continue
        #substring match
        probableMatch = process.extract(STRING, choices, limit=5)
        choices = list(set(choices))
        for LIST in probableMatch:
            if LIST[1] > 65:
                pname = LIST[0]
                if pname in choices:
                    choices.remove(pname)
                    #spelling match
                    if fuzz.ratio(STRING,pname)<45:
                        continue
                    doc = db.users.find({'username': pname}, {'username': 1, '_id': 1, 'category': 1, 'skills': 1})
                    
                    while (yield doc.fetch_next):
                        wdoc = doc.next_object()
                        l2.append(json_util.dumps(wdoc))
                        #l2 = list()
                        #l2.append(wdoc["username"])
                        #try:
                        #    l2.append(wdoc['category'])
                        #except:
                        #    pass
                        #try:
                        #    l2.append(wdoc['skills'])
                        #except:
                        #    pass
                        #userlist.append(l2)
                       
        data.append(l1)	
        data.append(l2)
        self.write('{data:%s}'%data)
        print '\nData:\n',data
        #self.render('searchresult.html', projlist=projlist, userlist=userlist)

class ServiceRequestHandler(RequestHandler):

    @coroutine
    @removeslash
    def get(self):

        if not bool(self.get_secure_cookie('user')):
            self.redirect('/?loggedIn=False')
            return

        service = self.get_argument('service')
        cost = self.get_argument('cost')
        email = self.get_argument('email')
        userInfo = yield db.users.find_one({'email': email})
        # validation
        for sinfo in userInfo['services']:
            if sinfo['service'] == service and sinfo['cost'] == cost:
                self.render('servicerequest.html',
                            result = {'user': userInfo['username'], 'service': service, 'cost': cost})

        self.redirect('/profile/' + userInfo['username']+'?serviceExists=False')
    @coroutine
    @removeslash
    def post(self):
        service = self.get_argument('service')
        cost = self.get_argument('cost')
        recvUser = self.get_argument('user')
        s = self.get_secure_cookie('user')

        now = datetime.now()
        time = now.strftime("%d-%m-%Y %I:%M %p")
        userInfo = yield db.users.find_one({'_id':ObjectId(s)})
        recvInfo = yield db.users.find_one({'username':recvUser})
        #srequest = yield db.serviceRequests.insert({'From' : s, 'To' : recvUser, 'Service' : {'service' : service, 'cost' : cost,'accepted':0}})
        result=db.serviceRequests.find({'aliases':[{'fromid':ObjectId(s)},{'toid':recvInfo['_id']}],'Service.1.service':service})
        if result:
            self.redirect('/?sendrequest=alreadyMade')
        srequest = yield db.serviceRequests.insert({'aliases':[{'fromid':ObjectId(s)},{'toid':recvInfo['_id']}],'Service':[{"accepted":0},{'service':service},{"sentby":userInfo["username"]},{"recievedby":recvInfo["username"]},{"time":time}]})
        if bool(srequest):
            self.redirect('/?sendrequest=True')
        else:
            self.redirect('/?sendrequest=False')

class AcceptServicesHandler(RequestHandler):
    @removeslash
    @coroutine
    def get(self):
        msgs = list()
        result = db.serviceRequests.find({'aliases': {'toid': ObjectId(self.get_secure_cookie('user'))},'Service.0.accepted':0})
        while (yield result.fetch_next):
            doc = result.next_object()
            print doc
            msgs.append(doc)
        self.render("view_services.html", msgs=msgs)

    @removeslash
    @coroutine
    def post(self):
        sid = self.get_argument('sid')
        result = yield db.serviceRequests.find_one(
            {'aliases': {'toid': ObjectId(self.get_secure_cookie('user'))}, '_id': ObjectId(sid)})
        if bool(result):
            yield db.serviceRequests.update({'_id': ObjectId(sid)}, {'$set': {'Service.0.accepted': 1}})
            self.redirect('/?acceptService=True')
        else:
            self.redirect('/?acceptService=False')

class MessageHandler(RequestHandler):
    @removeslash
    @coroutine
    def post(self):
        current_id = self.get_secure_cookie('user')
    
        obId=self.get_argument('obId')
        txt=self.get_argument('message')   
        #result=yield db.serviceRequests.find_one({'$or':[{'aliases':[{'fromid':ObjectId(current_id)},{'toid':ObjectId(obId)}]},{'aliases':[{'toid':ObjectId(current_id)},{'fromid':ObjectId(obId)}]}]})
        #not using result for validation as it is very slow
        userData = yield db.users.find_one({'_id':ObjectId(current_id)})
        recvInfo = yield db.users.find_one({'_id':ObjectId(obId)})
        if userData and recvInfo:
            now = datetime.now()
            time = now.strftime("%d-%m-%Y %I:%M %p")
            #print '\n\n\n',result
            #db schema looks big but search will happen only on aliases if an index is created on aliases 
            #and to remove the number of queries sentby and revieved by is added to db to faciltate visiting their profile
            #from both sides.
            
            
            result=yield db.messages.insert({'aliases':[{'fromid':ObjectId(current_id)},{'toid':ObjectId(obId)}],'msg':[{"isread":0},{'txt':txt},{"sentby":userData["username"]},{"recievedby":recvInfo["username"]},{"time":time}]})
            self.redirect('/profile/me')
        else:
            print 'unsuccessful'
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
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    cookie_secret="35an18y3-u12u-7n10-4gf1-102g23ce04n6"
)

# Application initialization
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
    (r"/search",SearchHandler),
    (r"/serviceRequest", ServiceRequestHandler),
     (r"/acceptService", AcceptServicesHandler),
     (r"/message", MessageHandler)
], **settings)

# main init
if __name__ == "__main__":
    server = HTTPServer(application)
    server.listen(5000)
    IOLoop.current().start()

