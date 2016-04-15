import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
from bson.json_util import loads
from bson.json_util import dumps
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('SEARCHING.html')
 
 

class FormHandler(tornado.web.RequestHandler):
	def post(self):
		STRING=self.get_argument('string')
		coll=self.application.db.projects
		word_doc=coll.find()
		choices=list()
		for doc in word_doc:
			choices.append(doc["category"])
		probableMatch=process.extract(STRING,choices,limit=5)	
		self.write("Matching Search Results are:\n")
		for LIST in probableMatch:
			if LIST[1]>70:
				doc=coll.find_one({"category":LIST[0]})
				doc=dumps(doc)
				self.write(doc)
	
       
class Application(tornado.web.Application):
    def __init__(self):
        template_path=os.path.join(os.path.dirname(__file__), "templates")
        handlers = [(r"/", IndexHandler),(r"/displayall",FormHandler)]
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["projectTest"]
        tornado.web.Application.__init__(self, handlers,template_path,debug=True)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

