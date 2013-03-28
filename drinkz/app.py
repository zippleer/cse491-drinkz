#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import db


dispatch = {
	'/' : 'index',
	'/liquor_type' : 'show_types',
 	'/inventory' : 'show_inv',
	'/recipies' : 'show_rec',
	'/conversion' : 'conversion_form',
	'/converted' : 'convert_result',
	'/recv' : 'recv'
}


html_headers = [('Content-type', 'text/html')]


class SimpleApp(object):
    def __call__(self, environ, start_response):


        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')


        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)


        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]


        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = open('index.html').read()
        start_response('200 OK', list(html_headers))
        return [data]
        
    def show_types(self, environ, start_response):
        content_type = 'text/html'
        data = open('html/liquor_types.html').read()


        start_response('200 OK', list(html_headers))
        return [data]
 
    def show_inv(self, environ, start_response):
        content_type = 'text/html'
        data = open(html/inventory.html)

        start_response('200 OK', list(html_headers))
        return [data]

    def show_rec(self,environ, start_response):
        content_type = 'text/html'
        data = open(html/recipes.html)

        start_response('200 OK', list(html_headers))
        return [data]

    def form(self, environ, start_response):
        data = form()


        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)


        amount = results['amount'][0]
        amount = db.convert_to_ml(amount)


        content_type = 'text/html'
        data = "Amount %s ml;  <a href='./'>return to index</a>" % (amount)


        start_response('200 OK', list(html_headers))
        return [data]


    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])


                return [response]


        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]


    def _decode(self, json):
        return simplejson.loads(json)


    def _dispatch(self, json):
        rpc_request = self._decode(json)


        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)


        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)


    def rpc_hello(self):
        return 'world!'


    def rpc_add(self, a, b):
        return int(a) + int(b)
    
def form():
    return """
<form action='recv'>
<Amount in oz/gallon/liter/ml? <input type='text' name='amount' size'20'>
<input type='submit'>
</form>
"""


if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
