# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler
import torndb
# import pymysql
from elasticsearch_dsl import DocType,Nested,Date,Boolean,analyzer,Completion,Text,Keyword,Integer
from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch
import json
import os
define("port", default=8688, type=int, help="run server on the given port.")
# db = torndb.Connection(host="172.18.115.15", database="Im", user="Dev3", password="123456", charset='utf8')
# connections.create_connection(hosts="127.0.0.1")
# esclient = Elasticsearch(['localhost:9200'])
esclient = Elasticsearch(['172.18.113.113:9200'])

class HouseHandler(RequestHandler):
    def get(self):
        # new_id = self.get_argument("NewsID")
        new_title = self.get_argument("seachStr")
        pagesize = self.get_argument("pageSize")
        try:
            response = esclient.search(
            index='yidian',
            doc_type='yidianew',
            body={
                "query": {"match": {"NewsTitle": new_title}},
                "size":pagesize,
                "sort": [
                    {
                        "NewsDate": {
                            "order": "desc"
                        }
                    }
                ]
            }
            )
            # response = esclient.search(
            # index='lynews',
            # doc_type='tbl_NewsDetails',
            # body={
            #     "query": {"match": {
            #         "NewsTitle": new_title
            #     }},
            #
            #     "size":1,
            # }
            # )

            # rets = json.dumps(response)
            # print(rets)
            # print(type(rets))
            # result=rets.encode('utf-8').decode('unicode_escape')
            self.write({"error": 0, "errmsg": "OK", "data": response})

            # self.render('index.html', response)

        except Exception as e:
            print(e)
            self.write({"error": 1, "errmsg": "db error", "data": []})


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
        (r"/data_es", HouseHandler),

    ], **settings)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    # tornado.ioloop.IOLoop.current().start()
    tornado.ioloop.IOLoop.instance().start()


# 127.0.0.1:8888/data_es?NewsTitle='飞机'