#!/usr/bin/python
# -*- coding:utf-8 -*-
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

""" python��������ת���������Խ��䲿���κ�һ��֧��WSGI���йܿռ䡣
�÷���
  http://hostedurl?u=url&k=AUTHKEY&t=timeout
  ������
  hostedurl: ����ת����������URL
  url: ��Ҫת����url����Ҫ��ʹ��urllib.quoteת�壬�ر��������&����
  AUTHKEY: Ϊ�˷�ֹ���ã���Ҫ�ṩһ��key��ΪALLOW_KEYS������κ�һ��ֵ
  timeout: [��ѡ]��ʱʱ�䣬Ĭ��Ϊ30s
 """

__Version__ = "1.0"
__Author__ = "Arroz"

from wsgiref.util import is_hop_by_hop
import urllib, urllib2, socket, bottle

ALLOW_KEYS = ('xzSlE','ILbou','DukPL')

application = app = bottle.Bottle()

@app.route(r'/')
def Home():
    resp = bottle.response
    qry = bottle.request.query
    url,k,timeout = qry.u, qry.k, int(qry.get('t','30'))
    if k and k not in ALLOW_KEYS:
        return 'Auth Key is invalid!'

    if url and k:
        url = urllib.unquote(url)
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)")
            req.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
            ret = urllib2.urlopen(req,timeout=timeout)
            content = ret.read()
            headers = [(n,v) for n,v in ret.info().items() if not is_hop_by_hop(n)]
            cookieadded = False
            for n,v in headers:
                if n == 'Set-Cookie' and cookieadded:
                    resp.add_header(n, v)
                else:
                    resp.set_header(n, v)
                    if n == 'Set-Cookie':
                        cookieadded = True
            return content
        except socket.timeout:
            pass
        except Exception as e:
            print("ERR:%s:%s" % (type(e),str(e)))
            bottle.abort(400)
    else:
        return "<html><head><title>Forwarder Url</title></head><body>Forwarder : thisurl?u=url&k=AUTHKEY&t=timeout</body></html>"

if __name__ == '__main__': #for debug
    bottle.run(app, reloader=True)
