import tornado.web
import tornado.ioloop
import os
import sqlite3
import string
import random
import json


def generateRandomString(lenght):
    st = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join(random.sample(st, lenght))


def selectArticles():
    query = "SELECT title,id FROM 'article'"
    cursor = app.db.cursor()
    cursor.execute(query)
    app.db.commit()
    articles = cursor.execute(query)
    return articles


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class selectSpeech(BaseHandler):
    def get(self):
        query = "select speech,speaker,source from 'speechs' order by random() limit 1"
        cursor = self.application.db.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        data = {
            "speech": result[0],
            "speaker": result[1],
            "source": result[2]
        }
        json_data = json.dumps(data)
        self.write(str(json_data))

class AddSpeech(BaseHandler):
    def post(self):
        speech=self.get_argument("speech")
        speaker=self.get_argument("speaker")
        source=self.get_argument("source")
        query="insert into speechs (speech,speaker,source) values (?,?,?)"
        cursor=self.application.db.cursor()
        cursor.execute(query,[speech,speaker,source])
        self.application.db.commit()
        data={
            "status":True,
            "message":"جمله شما با موفقیت افزوده شد",
        }
        json_data=json.dumps(data)
        self.write(str(json_data))




class MainHandler(BaseHandler):
    def get(self):
        self.render("mainPage.html", articles=selectArticles(),
                    AddArticleMessage=None)


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
            self.set_secure_cookie("user", result[1])
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
        """self.render("mainPage.html", articles=selectArticles(),
                    AddArticleMessage=True)"""
        self.write("sahar")

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

    @tornado.web.authenticated
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
        "cookie_secret": "generateRandomString(50)"
    }

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", Login),
        (r"/selectSpeech", selectSpeech),
        (r"/add-speech",AddSpeech),
        (r"/addArticle", AddArticle),
        (r"/articles/([a-zA-Z0-9]+)", ShowArticle),
        (r"/deleteArticle/([a-zA-Z0-9]+)", DeleteArticle),
        (r"/editArticle/([a-zA-Z0-9]+)", UpdateArticle)
    ], **settings)

    app.db = sqlite3.connect("site.db")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
