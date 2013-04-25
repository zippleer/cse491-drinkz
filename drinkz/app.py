#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson

from drinkz import db

dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/recipes' : 'recipes',
    '/liquor_types' : 'liquor_types',
    '/inventory' : 'inventory',
    '/convert_form' : 'convert_form',
    '/do_convert' : 'do_convert',
    '/rpc'  : 'dispatch_rpc'
}

html_headers = [('Content-type', 'text/html')]

style = """
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
"""

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", list(html_headers))
            return ["No path %s found" % path]

        return fn(environ, start_response)

    def index(self, environ, start_response):
        start_response("200 OK", list(html_headers))

        
        return ["""\
<html><head><title>Recipes</title></head>
%s<body>
<h1>Index</h1>
<A href='recipes'>Recipes</a>
<p>
<a href='liquor_types'>Liquor types</a>
<p>
<a href='inventory'>Inventory</a>
<p>
<hr>
<a href='convert_form'>Form to convert amounts</a>
<hr>

<script>
function myFunction()
{
alert("Hello! I am an alert box!");
}
</script>
<input type="button" onclick="myFunction()" value="Show alert box" />
</body>
</html>
""" % (style,)]

    def recipes(self, environ, start_response):
        start_response("200 OK", list(html_headers))
        x = ["<html><head><title>Recipes</title>%s</head><body><h1>Recipes:</h1><p><ul>" % style]

        for r in db.get_all_recipes():
            x.append("<li> Recipe name: %s" % r.name)

        x.append("</ul></body></html>")

        return x

    def liquor_types(self, environ, start_response):
        start_response("200 OK", list(html_headers))

        x = ["<html><head><title>Recipes</title>%s</head><body><h1>Liquor types</h1>:<p><ul>" % style]
        for (mfg, liquor, typ) in db._bottle_types_db:
            x.append("<li> %s - %s - %s" % (mfg, liquor, typ))
        x.append("</ul></body></html>")
        return x

    def inventory(self, environ, start_response):
        start_response("200 OK", list(html_headers))
        x = ["<html><head><title>Recipes</title>%s</head><body><h1>Inventory:</h1><p><ul>" % style]

        for (mfg, liquor) in db.get_liquor_inventory():
            x.append("<li> %s - %s" % (mfg, liquor))
        x.append("</ul></body></html>")
        return x

    def convert_form(self, environ, start_response):
        start_response("200 OK", list(html_headers))

        return ["""\
<html>
<head>
<title>Conversion form</title>
%s
</head>
<body>
<h1>Conversion form</h1>
<form action='/do_convert'>
Amount: <input type=text name=amount>
<input type=submit>
</form>
</body>
</html>
""" % style]

    def do_convert(self, environ, start_response):
        start_response("200 OK", list(html_headers))

        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        amount = results['amount'][0]
        amount = db.convert_to_ml(amount)

        x = ["Amount is: %s ml" % (amount,)]
        return x

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

    def rpc_convert_units_to_ml(self, amount):
        return "%s ml" % (db.convert_to_ml(amount))

    def rpc_get_recipe_names(self):
        return [ r.name for r in db.get_all_recipes() ]

    def rpc_get_liquor_inventory(self):
        return [ (mfg, liquor) for (mfg, liquor) in db.get_liquor_inventory() ]
    
if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
