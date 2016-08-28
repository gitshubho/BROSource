import urllib
import urllib2
from pymongo import MongoClient
db=MongoClient('mongodb://brsrc:brsrc@ds028559.mlab.com:28559/brosource')['brosource']
# function to get rerquired userdata only
def setUserInfo(userInfo, *args):
    userdata = {}
    for arg in args:
		try:
			userdata[arg] = userInfo[arg]
		except:
			pass
		if (arg=='certifications' or arg=='education_details'):
			userdata[arg]=str(','.join(userdata[arg]))
    return userdata

def getSkills(userSkills):
    skills=[]
    for skill in userSkills:
		try:
			skills.append(db.skills.find({skill:{'$exists':1}},{skill:1})[0][skill])
		except:
			pass
    return skills
# function to hash passwords
def hashingPassword(password):
    salt=[password[i] for i in range(0,len(password),2)]
    postsalt=''.join(salt[:len(salt)/2])
    presalt=''.join(salt[len(salt)/2:])
    return (presalt+password+postsalt)

# function to send the token for forgot password
def sendRequestToken(contact, authToken):

    authkey = "81434A3rGba9dY75583ac07"
    sender = "BROSRC"
    message = "Auth Token for Changing Password in Brosource is "+str(authToken)
    route = "transactional"
    values = {
              'authkey' : authkey,
              'mobiles' : contact,
              'message' : message,
              'sender' : sender,
              'route' : route
              }
    url = "https://control.msg91.com/api/sendhttp.php"  # API URL
    postdata = urllib.urlencode(values)                 # URL encoding the data here.
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)

# function to send welcome message to new user
def sendMessage(number,message):

    authkey = "81434A3rGba9dY75583ac07" # Your authentication key.
    mobiles = number                    # Multiple mobiles numbers separated by comma.
    message = message                   # Your message to send.
    sender = "BROSRC"                   # Sender ID,While using route4 sender id should be 6 characters long.
    route = "transactional"             # Define route
                                        # Prepare you post parameters
    values = {
              'authkey' : authkey,
              'mobiles' : mobiles,
              'message' : message,
              'sender' : sender,
              'route' : route
              }
    url = "https://control.msg91.com/api/sendhttp.php"  # API URL
    postdata = urllib.urlencode(values)                 # URL encoding the data here.
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
