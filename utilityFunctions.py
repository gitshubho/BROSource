import urllib
import urllib2

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
