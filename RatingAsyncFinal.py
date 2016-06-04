import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
from bson.json_util import loads
from bson.json_util import dumps
from bson.objectid import ObjectId
import motor
from tornado.options import define, options
from tornado.gen import coroutine,Task,engine

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
db=motor.motor_tornado.MotorClient().projectTest
class IndexHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        self.render('enterRating.html')
class RatingHandler(tornado.web.RequestHandler):
	@coroutine
	def post(self):
		STRING=self.get_argument('string')
		comments=self.get_argument('comments')
		newRating=float(STRING)
		if newRating>5 or newRating<0:
			self.write("Invalid rating!")
			self.redirect('/')
		else:
			yield db.users.update({"username":"shubham0704"},{'$push':{'ratings':newRating}})
			yield db.projects.update({"projectname":"website2"},{'$push':{'ratings':newRating,'comments':comments}})
			doc=yield db.users.find_one({"username":"shubham0704"})
			ratings=doc['ratings']
			i=0
			avg=0
			for rating in ratings:
				avg+=rating
				i+=1
			avg=avg/i
			self.render('updateRate.html',personRating=avg,projectRating=newRating)
		




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

