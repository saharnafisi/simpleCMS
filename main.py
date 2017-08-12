import tornado.web
import tornado.ioloop
import os
import sqlite3


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        query="SELECT title FROM 'article'"
        cursor=self.application.db.cursor()
        cursor.execute(query)
        self.application.db.commit()
        articles=cursor.execute(query)
        self.render("mainPage.html",articles=articles)


class AddArticle(tornado.web.RequestHandler):
    def get(self):
        self.render("addArticle.html")
    def post(self):
        article_id=self.get_argument("id")
        title=self.get_argument("title")
        content=self.get_argument("content")
        query="insert into 'article' values(?,?,?)"
        cursor=self.application.db.cursor()
        cursor.execute(query,[article_id,title,content])
        self.application.db.commit()
        self.redirect("addArticle")




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
