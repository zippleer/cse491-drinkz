#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import db, recipes

dispatch = {
    '/' : 'index',
    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/liquor_types' : 'liquor_types',
    '/convert_result' : 'convert_result',
    '/convert_to_ml' : 'convert_to_ml',
    '/error' : 'error',
    '/rpc'  : 'dispatch_rpc'
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
        

    def load_db_file(self, file_name):
        db.load_db(file_name)
        
    def buildHtmlPage(self,title,head,body):
        page = """
                        <html>
                        <head>
                      """
        page = page + head
        
        page = page + """
                        <style type=\"text/css\">
                        h1 {color:black;}
                        p {color:blue;}
                        </style>
                        </head>
                        <body>
                      """
        page = page +"<h1>" + title + "</h1>"
        
        
        page = page + body
        
        page = page + "</body>"
        
        return page

    def index(self, environ, start_response):
        
        data = """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    """

        data = data +"""
                <input type=\"button\" onclick=\"PRESS_ME()\" value=\"PRESS ME!!\" />"""
        script = """
                <script>
                function PRESS_ME()
                {
                    alert('These are not the drinkz you are looking for');
                }
                </script>
             """
        data = self.buildHtmlPage("Grab Them Solo Cups and Lesgo!",script,data)
        start_response('200 OK', list(html_headers))
        return [data]

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.

    def liquor_types(self, environ, start_response):
        content_type = 'text/html'
        data = """
        <table border=\"1\" cellpadding =\"5\">
        <tr><th>Manfacturer</th><th>Liquor</th><th>Type</th></tr>
        """
        for mfg, liq in db.get_liquor_inventory():
            data = data + "<tr><td> %s </td><td> %s </td><td> %s </td></tr>" % mfg, liq
        
        data = data + "</table>"
        
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>"""

        data = self.buildHtmlPage("Liquor Types","",data)
        start_response('200 OK', [('Content-type', content_type)])
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


    def recipes(self, environ, start_response):
        content_type = 'text/html'
        data = """

        <table border=\"1\" cellpadding =\"5\">
        <tr><th>Name</th><th>Ingredients</th><th>Check Those Ingredients!</tr>
        """
        for recipe in db.get_all_recipes():
            data = data + "<tr><td> "+ recipe.name +"</td><td><table cellpadding =\"5\">"
            for item in recipe.ingredients:
                data = data + "<tr><td>"+ item[0] +"</td><td> " + item[1] +" </td></tr>"
            data = data + "</table></td><td>"
            
            missing = recipe.need_ingredients()
            if(missing):
                data = data + "we're missing some stuff, call Mikey"
            else:
                data = data + "nope, we're good to go, call Mikey"
            
            print data + "</td></tr>"
        data = data + "</table>"
     
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    """
        data = self.buildHtmlPage("Recipes","",data)
        start_response('200 OK', list(html_headers))
        return [data]


        start_response('200 OK', list(html_headers))
        return [data]


    def inventory(self, environ, start_response):
        content_type = 'text/html'
        data = """
        <table border=\"1\" cellpadding =\"5\">
        <tr><th>Manfacturer</th><th>Liquor</th><th>Amount</th></tr>
        """
        for item in db.get_liquor_inventory():
            data = data + "<tr><td> "+ item[0] +" </td><td> "+item[1]+" </td><td> "+db.get_liquor_amount(mfg,liquor)+" </td></tr>"
        data = data + "</table>"
        
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    """
        data = self.buildHtmlPage("Inventory","",data)
        start_response('200 OK', [('Content-type', content_type)])
        return [data]


    def convert_to_ml(self, environ, start_response):
        data = """
<form action='convert_result'>
Amount in oz/gallon/liter/ml? <input type='text' name='amount' size'20'>
<input type='submit' onclick ='whyConvert()' value='convert DRANK!'>
</form>
"""

        script = """
                    <script>
                    function whyConvert()
                    {
                        alert('Quantum Calculations Underway!');
                    }
                    </script>
                 """
        data = self.buildHtmlPage("Conversion",script,data)
        start_response('200 OK', list(html_headers))
        return [data]
   
    def convert_result(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        ml_amount = db.convert_to_ml(results['amount'][0])

        content_type = 'text/html'
        data = "Amount entered: %s:" % (str(ml_amount)+" ml")
        
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    """
        data = self.buildHtmlPage("Converted!! What more do you want from me?!","",data)
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
                #print "wsgi: "
                #print environ['wsgi.input'].read(length)
                #print "-=-=-=-"
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
        
    def rpc_convert_units_to_ml(self, amount):
        return str(db.convert_to_ml(amount))+" ml"
        
    def rpc_get_recipe_names(self):
        return str(db.get_all_recipe_names())

    def rpc_get_liquor_inventory(self):
        inventories = db.get_liquor_inventory()
        inventory_list = []
        for inventory in inventories:
            inventory_list.append((inventory[0],inventory[1]))
        return inventory_list


if __name__ == '__main__':

    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
