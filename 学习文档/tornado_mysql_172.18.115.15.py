# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler
import torndb
# import pymysql

import os
define("port", default=8888, type=int, help="run server on the given port.")
db = torndb.Connection(host="172.18.115.15", database="Im", user="Dev3", password="123456", charset='utf8')


class HouseHandler(RequestHandler):
    def get(self):
        # new_id = self.get_argument("NewsID")
        new_title = self.get_argument("NewsTitle")

        # sql = "SELECT * FROM Im.tbl_NewsDetails201805 where NewsID='000bfc2c-5915-11e8-b3e3-fa163e10141e'"
        # sql = "SELECT NewsTitle FROM Im.tbl_NewsDetails201805 where NewsID=%s"

        sql = "SELECT * FROM Im.tbl_NewsDetails201805 where NewsTitle REGEXP %s "
        try:
            ret = db.query(sql, new_title)
            print(ret)
        except Exception as e:
            print(e)
            return self.write({"error": 1, "errmsg": "db error", "data": []})
        data_list = []
        if ret:
            for l in ret:
                house = {
                    'id': l['NewsID'],
                    'NewsCategory': l['NewsCategory'],
                    'SourceCategory': l['SourceCategory'],
                    'NewsType': l['NewsType'],
                    "title": l['NewsTitle'],
                    "content": l['NewsContent'],
                    'NewsRawUrl': l['NewsRawUrl'],
                    'NewsClickLike': l['NewsClickLike'],
                    'NewsBad': l['NewsBad'],
                    'NewsRead': l['NewsRead'],
                    'SourceName': l['SourceName'],
                    'AuthorName': l['AuthorName'],
                    'NewsOffline': l['NewsOffline'],
                    # 'InsertDate':l['InsertDate']
                    # 'NewsDate':l['NewsDate']
                }
                data_list.append(house)
            self.write({"error":0, "errmsg":"OK", "data":data_list, "data_num":len(data_list)})


class Application(tornado.web.Application):
    def __int__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "statics"),
    debug=True,
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    current_path = os.path.dirname(__file__)
    app = tornado.web.Application([
        # (r"/", HouseHandler),
        (r"/data", HouseHandler),

    ],**settings)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

# 127.0.0.1:8888/data?NewsTitle=京东