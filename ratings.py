import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
from pymongo import MongoClient
from bson.json_util import loads
from bson.json_util import dumps

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('enterRating.html')
class RatingHandler(tornado.web.RequestHandler):
	def post(self):
		#self.write("inside post")
		STRING=self.get_argument('string')
		coll=self.application.db.profiles
		doc=coll.find_one({"name":"shubham0704"})
		curRating=doc['rating']
		newRating=float(STRING)
		UpdatedRating=(newRating+curRating)/2
		coll.update({"name":"shubham0704"},{'$set':{'rating':UpdatedRating}})
		coll=self.application.db.projects
		coll.insert({'rating':newRating})
		self.render('updateRate.html',personRating=UpdatedRating,projectRating=newRating)
		#self.write(str(doc['rating']))




class Application(tornado.web.Application):
    def __init__(self):
        template_path=os.path.join(os.path.dirname(__file__), "templates")
        handlers = [(r"/", IndexHandler),(r"/displayUpdate",RatingHandler)]
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["projectTest"]
        tornado.web.Application.__init__(self, handlers,template_path,debug=True)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
