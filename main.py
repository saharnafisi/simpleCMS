import tornado.web
import tornado.ioloop
import os
import sqlite3


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("user"):
            self.redirect("/login")
        else:
            query="SELECT title,id FROM 'article'"
            cursor=self.application.db.cursor()
            cursor.execute(query)
            self.application.db.commit()
            articles=cursor.execute(query)
            self.render("mainPage.html",articles=articles)

class Login(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html",message=None)
    def post(self):
        username=self.get_argument("userName")
        password=self.get_argument("password")
        query="SELECT * FROM 'user' WHERE userName=? AND password=?"
        cursor=self.application.db.cursor()
        cursor.execute(query,[username,password])
        result=cursor.fetchone()
        if not result:
            self.render("login.html",message=True)
        else:
            self.redirect("/")
            self.set_cookie("user",username)
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

class ShowArticle(tornado.web.RequestHandler):
    def get(self,article_id):
        query="SELECT * FROM 'article' WHERE id=?"
        cursor=self.application.db.cursor()
        cursor.execute(query,[article_id])
        self.application.db.commit()
        article=cursor.fetchone()
        self.render("showArticle.html",article=article)

class DeleteArticle(tornado.web.RequestHandler):
    def get(self,article_id):
        query="DELETE FROM 'article' WHERE id=?"
        cursor=self.application.db.cursor()
        cursor.execute(query,[article_id])
        self.application.db.commit()
        self.redirect("/")

class UpdateArticle(tornado.web.RequestHandler):
    def get(self,article_id):
        query="SELECT * FROM 'article' WHERE id=?"
        cursor=self.application.db.cursor()
        cursor.execute(query,[article_id])
        self.application.db.commit()
        article=cursor.fetchone()
        self.render("editArticle.html",article=article)

    def post(self,article_id):
        #article_id=self.get_argument("id")
        title=self.get_argument("title")
        content=self.get_argument("content")
        query="UPDATE 'article' SET title=?, text=? WHERE id=?"
        cursor=self.application.db.cursor()
        cursor.execute(query,[title,content,article_id])
        self.application.db.commit()
        self.redirect("/")


if __name__ == "__main__":
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    }

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login",Login),
        (r"/addArticle",AddArticle),
        (r"/articles/([a-zA-Z0-9]+)",ShowArticle),
        (r"/deleteArticle/([a-zA-Z0-9]+)",DeleteArticle),
        (r"/editArticle/([a-zA-Z0-9]+)",UpdateArticle)
    ], **settings)

    app.db = sqlite3.connect("site.db")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
