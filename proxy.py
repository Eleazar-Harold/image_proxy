from flask import send_file, Flask
from requests import get
from redis import StrictRedis
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

app = Flask(__name__)
redis_server = StrictRedis(host='localhost', port=6379)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    cached = redis_server.get(path)
    if cached:
        b_image = StringIO(cached).seek(0)
    else:
        b_image = StringIO(get(path).content)
        b_image.seek(0)
        redis_server.setex(path, (60*60*24*7),
                           b_image.getvalue())
    return send_file(b_image, mimetype='image/png')


if __name__ == '__main__':
  app.run()
