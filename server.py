import tornado.ioloop
import tornado.web
from mc import *
from mcutil import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template.html")

class GenerateExamples(tornado.web.RequestHandler):
    def post(self):
        model = MarkovChain()
        train(self.get_argument("corpus"), model, False)
        
        self.write(sample(model, int(self.get_argument("length"))) + "<br /><br />")
        self.render("template.html")

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/generate", GenerateExamples),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
