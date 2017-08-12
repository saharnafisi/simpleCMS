import tornado.web
import tornado.ioloop
import os
import sqlite3


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("base.html")

class AddArticle(tornado.web.RequestHandler):
    def get(self):
        self.render("addArticle.html")


if __name__ == "__main__":
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates")
    }

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/addArticle",AddArticle),
    ], **settings)

    app.db = sqlite3.connect("site.db")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
