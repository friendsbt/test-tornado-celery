import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen
import tasks
import task_simple
import tcelery
import upyun
try:
    from config import *
except ImportError:
    BUCKETNAME = os.environ['BUCKETNAME']
    UPYUN_USERNAME = os.environ['UPYUN_USERNAME']
    UPYUN_PASSWORD = os.environ['UPYUN_PASSWORD']

tcelery.setup_nonblocking_producer()

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        f = yield tornado.gen.Task(
            tasks.upload_image_to_upyun.apply_async,
            args=("mr.jpg", "/mr.jpg")
        )
        # f = yield tornado.gen.Task(
        #     task_simple.sleep.apply_async,
        #     args=(5, )
        # )
        print(f.result)
        self.write(str(f.result))
        self.finish()

if __name__ == "__main__":
    up = upyun.UpYun(BUCKETNAME, UPYUN_USERNAME, UPYUN_PASSWORD, timeout=30,
                 endpoint=upyun.ED_AUTO)
    try:
        up.delete("/mr.jpg")
    except Exception as e:
        print(e)
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()