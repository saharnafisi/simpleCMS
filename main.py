import tornado.web
import tornado.ioloop
import os
import sqlite3
import string
import random


def generateRandomString(lenght):
    st=string.ascii_lowercase+string.digits+string.ascii_uppercase
    return ''.join(random.sample(st,lenght))

def selectArticles():
    query = "SELECT title,id FROM 'article'"
    cursor =app.db.cursor()
    cursor.execute(query)
    app.db.commit()
    articles = cursor.execute(query)
    return articles

class BaseHandler(tornado.web.RequestHandler):
    def get_secure_cookie(self):
        return self.get_secure_cookie("user")



class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
            self.render("mainPage.html", articles=selectArticles(),AddArticleMessage=None)


class Login(BaseHandler):
    def get(self):
        self.render("login.html", message=None)

    def post(self):
        username = self.get_argument("userName")
        password = self.get_argument("password")
        query = "SELECT * FROM 'user' WHERE userName=? AND password=?"
        cursor = self.application.db.cursor()
        cursor.execute(query, [username, password])
        result = cursor.fetchone()
        if not result:
            self.render("login.html", message=True)
        else:
            self.set_secure_cookie("user",result[1])
            self.redirect("/")

class AddArticle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("addArticle.html")

    def post(self):
        article_id = self.get_argument("id")
        title = self.get_argument("title")
        content = self.get_argument("content")
        query = "insert into 'article' values(?,?,?)"
        cursor = self.application.db.cursor()
        cursor.execute(query, [article_id, title, content])
        self.application.db.commit()
        self.render("mainPage.html",articles=selectArticles(),AddArticleMessage=True)


class ShowArticle(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        query = "SELECT * FROM 'article' WHERE id=?"
        cursor = self.application.db.cursor()
        cursor.execute(query, [article_id])
        self.application.db.commit()
        article = cursor.fetchone()
        self.render("showArticle.html", article=article)


class DeleteArticle(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        query = "DELETE FROM 'article' WHERE id=?"
        cursor = self.application.db.cursor()
        cursor.execute(query, [article_id])
        self.application.db.commit()
        self.redirect("/")


class UpdateArticle(BaseHandler):
    @tornado.web.authenticated
    def get(self, article_id):
        query = "SELECT * FROM 'article' WHERE id=?"
        cursor = self.application.db.cursor()
        cursor.execute(query, [article_id])
        self.application.db.commit()
        article = cursor.fetchone()
        self.render("editArticle.html", article=article)

    def post(self, article_id):
        title = self.get_argument("title")
        content = self.get_argument("content")
        query = "UPDATE 'article' SET title=?, text=? WHERE id=?"
        cursor = self.application.db.cursor()
        cursor.execute(query, [title, content, article_id])
        self.application.db.commit()
        self.redirect("/")


if __name__ == "__main__":
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "login_url": "/login",
        "cookie_secret":generateRandomString(50)
    }

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", Login),
        (r"/addArticle", AddArticle),
        (r"/articles/([a-zA-Z0-9]+)", ShowArticle),
        (r"/deleteArticle/([a-zA-Z0-9]+)", DeleteArticle),
        (r"/editArticle/([a-zA-Z0-9]+)", UpdateArticle)
    ], **settings)

    app.db = sqlite3.connect("site.db")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
