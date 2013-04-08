#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import db, recipes


dispatch = {
	'/' : 'index',
    '/error' : 'error',
    '/content' : 'somefile',
	'/liquor_types' : 'liquor_t',
 	'/inventory' : 'inv',
	'/recipes' : 'rec',
	'/conversion' : 'conversion',
	'/converted' : 'convert_result',
	'/recv' : 'recv'
}


html_headers = [('Content-type', 'text/html')]


class SimpleApp(object):
    def __call__(self, environ, start_response):


        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')
#            
#    def index(self, environ, start_response):sho
#        data = open('index.html').read()
#        start_response('200 OK', list(html_headers))
#        return [data]

        fn = getattr(self, fn_name, None)


        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]


        return fn(environ, start_response)
        

    def index(self, environ, start_response):
        data = """
<html>
<head>
<title>CSE491</title>
<style type='text/css'>
h1 {color:blue;}
body {font-size: 18px;}
</style>
<script>
function alertBox()sh
{
alert("Gratuitous Box");
}
</script>
</head>
<body>

<b><h1>Home</h1></b><p>

<a href='conversion'>Covert to ml</a>
<p>
<a href='recipes'>Recipes</a>
<p>
<a href='inventory'>Inventory</a>
<p>
<a href='liquor_types'>Liquor Types</a>
<p>
<input type="button" onclick="alertBox()" value="Show alert box" />

</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.

    def liquor_t(self, environ, start_response):

        data = """
<html>
<head>
<title>Liquor-Types</title>
<style type = 'text/css'>
h1 {color:green;}
body {font-size: 18px;}
</style>
</head>
<body>
"""
        
        data += "<b><h1>Liquor Types</h1></b><p>Manufacturer, Liquor Type</p><ul>"

        for mfg, liquor in db.get_liquor_inventory():
            data += "<p> </p>"
            data += '<li> %s, %s' % (mfg, liquor)

        data += "</ul>"

        data += """
<p><a href='/'>Home</a>
</p>
<p><a href='recipes'>Recipes</a>
</p>
<p><a href='inventory'>Inventory</a>
</p>
</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]


    def somefile(self, environ, start_response):
        content_type = 'text/html'
        data = open('somefile.html').read()

        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]



    def rec(self, environ, start_response):

        data = """
<html>
<head>
<title>CSE491-Recipes</title>
<style type = 'text/css'>
h1 {color:green;}
body {font-size: 18px;}
</style>
</head>
<body>
"""
        data += "<b><h1>Recipes</h1></b><p>Recipe, Do We Have All the Ingredients?</p><ul>"

        for key in db._recipe_db:
            a = db._recipe_db[key].ingredients[0][0]
            b = db._recipe_db[key].ingredients[0][1]
            if len(db._recipe_db[key].need_ingredients())>0:
                answer = "No"
                data += answer
            else:
                answer = "Yes"
                data += answer

        data += "</ul>"

        data += """
<p><a href='/'>Home</a>
</p>
<p><a href='inventory'>Inventory</a>
</p>
<p><a href='liquor_types'>Liquor Types</a>
</p>
</body>
</html>
"""

        start_response('200 OK', list(html_headers))
        return [data]


    def conversion(self, environ, start_response):
        data = form()


        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)


        amount = results['amount'][0]
        amount_ml = db.convert_to_ml(amount)


        content_type = 'text/html'
        data = "Amount %s ml;  <a href='./'>return to index</a>" % (amount_ml)


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


    def inv(self, environ, start_response):

        data = """
<html>
<head>
<title>CSE491-Inventory</title>
<style type = 'text/css'>
h1 {color:green;}
body {font-size: 18px;}
</style>
</head>
<body>
"""
        
        data += "<b><h1>Inventory</h1></b><p>Manufacturer, Liquor Type, Amount (ml)</p><ul>"

        for mfg, liquor in db.get_liquor_inventory():
            data += "<p> </p>"
            data += "<li> %s,  %s, %s" % (mfg, liquor, db.get_liquor_amount(mfg,liquor))

        data += "</ul>"

        data += """
<p><a href='/'>Home</a>
</p>
<p><a href='recipes'>Recipes</a>
</p>
<p><a href='liquor_types'>Liquor Types</a>
</p>
</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]


if __name__ == '__main__':

    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
