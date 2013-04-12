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
    '/recipe_input' : 'recipe_input',
	'/recipe_form' : 'recipe_form',
    '/recipe_add' : 'recipe_add',
    '/type_form' : 'type_form',
    '/type_add' : 'type_add',
    '/inv_form' : 'inv_form',
    '/inv_add' : 'inv_add',
    '/rate_form' : 'rate_form',
    '/rate_add' : 'rate_add',
    '/error' : 'error',
    '/rpc'  : 'dispatch_rpc'
}

def load_db_file(self, file_name):
        db.load_db(file_name)


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
                        h1 {color:orange;}
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
    <h2><> Menu </h2>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='recipe_input'>Add Recipe</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert Amount</a></br>
    <a href='type_form'>Add Bottle Type</a></br>
    <a href='inv_form'>Add to Inventory</a></br>
    """

        data = data +"""
                <input type=\"button\" onclick=\"PRESS_ME()\" value=\"Legal Note\" />"""
        script = """
                <script>
                function PRESS_ME()
                {
                    alert('These are not the drinkz you are looking for.. Unless you are over 21. In that case, Stay Thristy My Friend!');
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
        for mfg, liq, typ in db._bottle_types_db:
            data = data + "<tr><td>"+mfg+"</td><td>"+liq+ "</td><td>"+typ+ "</td><tr>"
        
        data = data + "</table>"
        
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='recipe_input'>Add Recipe</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    <a href='type_form'>Add Bottle Type</a></br>
    <a href='inv_form'>Add to Inventory</a></br>"""

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

    def inv_form(self, environ, start_response):
        data = """
<form action= 'inv_add'>
Manufacturer:  <input type="text" name="mfg"> <br>
Liquor Name:  <input type="text" name="liquor_name"> <br>
Liquor Amount:  <input type="text" name="liquor_amount"> <br>
<input type='submit' value='Submit to Inventory'>
</form>
"""
        start_response('200 OK', list(html_headers))
        return [data]

    def inv_add(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = (results['mfg'][0])
        liq = (results['liquor_name'][0])
        amount = (results['liquor_amount'][0])

        try:
            db.add_to_inventory(mfg, liq, amount)
        except db.LiquorMissing:
            content_type = 'text/html'
            data = "That Liquor Isn't in the Inventory!!!.  <a href='./'>return to index</a>"

            start_response('200 OK', list(html_headers))
            return [data]

        content_type = 'text/html'

        data = "Liquor Added to Inventory: " +mfg +' :'+ liq+' :' + amount
        
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    <a href='type_form'>Add Bottle Type</a></br>
    <a href='inv_form'>Add to Inventory</a></br>
    """
        data = self.buildHtmlPage("Added to Inventory!","",data)
        start_response('200 OK', list(html_headers))
        return [data]

    def type_form(self, environ, start_response):
        data = """
<form action= 'type_add'>
Manufacturer:  <input type="text" name="mfg"> <br>
Liquor Name:  <input type="text" name="liquor_name"> <br>
Liquor Type:  <input type="text" name="liquor_type"> <br>
<input type='submit' value='Submit Bottle Type'>
</form>
"""
        start_response('200 OK', list(html_headers))
        return [data]

    def type_add(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = (results['mfg'][0])
        liq = (results['liquor_name'][0])
        typ = (results['liquor_type'][0])

        db.add_bottle_type(mfg, liq, typ)

        content_type = 'text/html'

        data = "Bottle Type Entered: " + mfg+' :' + liq +' :'+ typ
        
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    <a href='type_form'>Add Bottle Type</a></br>
    <a href='inv_form'>Add to Inventory</a></br>
    """
        data = self.buildHtmlPage("Added Bottle Type!","",data)
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
                data = data + "Hell Nah, You are missing: <br>"
            else:
                data = data + "Hell Yeah, We Can Do That!"
            
            for tup in missing:
                data = data + tup[0] + ' ' + str(tup[1]) + ' ml' + '<br>' 

        data = data + "</table>"
     
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert Amount</a></br>
    <a href='recipe_input'>Add Recipe</a></br>
    <a href='type_form'>Add Bottle Type</a></br>
    <a href='inv_form'>Add to Inventory</a></br>
    """
        data = self.buildHtmlPage("Recipes","",data)
        start_response('200 OK', list(html_headers))
        return [data]

    def recipe_input(self, environ, start_response):
        data = """
<form action= 'recipe_form'>
Number of Ingredients? <input type="number" name="ing_num">
<input type='submit' value='Create Recipe!'>
</form>
"""

        start_response('200 OK', list(html_headers))
        return [data]

    def recipe_form(self, environ, start_response):

        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        i_num= results['ing_num'][0]
        try:
            i_num = int(i_num)
        except ValueError:
            content_type = 'text/html'
            data = "That's Not a Number!!!.  <a href='./'>return to index</a>"

            start_response('200 OK', list(html_headers))
            return [data]

        content_type = 'text/html'

        data = """
<form action='recipe_add'>
Your Recipe Name? <input type='text' name='r_name' size'20'> <br>"""
        for x in range (0, i_num):
            data = data + """
Type of Alcohol? <input type='text' name='r_liq' size='20'> 
Amount of Alcohol? <input type='text' name='r_amount' size='20'> <br>
"""
        data = data+ """
<input type='submit' value='Submit Recipe!'>
"""
     
        data = self.buildHtmlPage("Recipe",'',data)
        start_response('200 OK', list(html_headers))
        return [data]
   
    def recipe_add(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        ing_list = []

        #ing_num = (results['i_num'][0])
        #print ing_num
        x = 0
        rec_name = (results['r_name'][0])
        truthiness = True
        while(truthiness):
            try:        
                liq_name = (results['r_liq'][x])
                liq_amount = (results['r_amount'][x])
                new_ing = (liq_name, liq_amount)
                ing_list.append(new_ing)
                x = x + 1
            except IndexError:
                truthiness = False
                pass # Got all ingredients


        new_r = recipes.Recipe(rec_name, ing_list)

        db.add_recipe(new_r)

        content_type = 'text/html'

        data = "Recipe entered: %s:" % rec_name
        
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    <a href='type_form'>Add Bottle Type</a></br>
    <a href='inv_form'>Add to Inventory</a></br>
    """
        data = self.buildHtmlPage("Added, but would you really drink that?","",data)
        start_response('200 OK', list(html_headers))
        return [data]


    def inventory(self, environ, start_response):
        content_type = 'text/html'
        data = """
        <table border=\"1\" cellpadding =\"5\">
        <tr><th>Manfacturer</th><th>Liquor</th><th>Amount</th></tr>
        """
        for mfg,liquor in db.get_liquor_inventory():
            data = data + "<tr><td> "+ mfg +" </td><td> "+liquor+" </td><td> "+str(db.get_liquor_amount(mfg,liquor)) + " ml"+" </td></tr>"
        data = data + "</table>"
        
        data = data + """</br>
    </br>
    <h3> Menu </h3>
    <a href='/'>Home</a></br>
    <a href='recipes'>Recipes</a></br>
    <a href='inventory'>Inventory</a></br>
    <a href='liquor_types'>Liquor Types</a></br>
    <a href='convert_to_ml'>Convert amount</a></br>
    <a href='type_form'>Add Bottle Type</a></br>
    <a href='inv_form'>Add to Inventory</a></br>
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
    <a href='type_form'>Add Bottle Type</a></br>
    <a href='inv_form'>Add to Inventory</a></br>
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

    def rpc_add_bottle_type(self, mfg, liquor, typ):
        db.add_bottle_type(mfg, liquor, typ)

    def rpc_add_to_inventory(self, mfg, liquor, amount):
        db.add_to_inventory(mfg, liquor, amount)

    def rpc_add_recipe(self, name, ingredients):

        r = recipes.Recipe(name, ingredients)
        
        db.add_recipe(r)


if __name__ == '__main__':

    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
