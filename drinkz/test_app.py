from drinkz import app
from drinkz import db
from drinkz import recipes

def test_recipes():
    db._reset_db()

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
    
    r = recipes.Recipe('whiskey bath', [('blended scotch', '2 liter')])
    db.add_recipe(r)
    
    environ = {}
    environ['PATH_INFO'] = '/recipes'
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Recipes') != -1, text
    assert text.find('whiskey bath') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'
