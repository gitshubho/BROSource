import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
from pymongo import MongoClient
from bson.json_util import loads
from bson.json_util import dumps
from bson.objectid import ObjectId

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


#class IndexHandler(tornado.web.RequestHandler):
 #   def get(self):
  #      self.render('projectPage.html')
   #     self.redirect('/

class bidHandler(tornado.web.RequestHandler):
	def get(self):
		coll=self.application.db.projects
		#coll.find({},{bids:{'$slice':5}}).sort({bidAmt:-1})
		document=coll.find({'_id':ObjectId('56f53bc6f6603862ef3021de')})
		for doc in document:
			pass
			
		bids=doc['bids']
		amount=list()
		for bid in bids:
			bid['amount']=int(bid['amount'])
			amount.append(bid['amount'])
		
		amount.sort(reverse=True)
		maxbid=list()
		i=0
		for amt in amount:
			if(i==5):break
			for bid in bids:
				if bid['amount']==amt:						
					maxbid.append(bid)
					bids.remove(bid)
					i+=1
					break
		self.render('placeBid.html',maxbid=maxbid,amount=amount)
	def post(self):
		coll=self.application.db.projects
		#ID=coll.find({'name':'shubham'},{'_id':1})
		bidAmt=self.get_argument('bidAmt')
		days=self.get_argument('noOfDays')
		coll.update({'_id':ObjectId('56f53bc6f6603862ef3021de')},{'$push':{'bids':{'amount':bidAmt,'days':days}}})
		self.redirect('/')				
class Application(tornado.web.Application):
    def __init__(self):
        template_path=os.path.join(os.path.dirname(__file__), "templates")
        handlers = [(r"/",bidHandler)]
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["projectTest"]
        tornado.web.Application.__init__(self, handlers,template_path,debug=True)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

