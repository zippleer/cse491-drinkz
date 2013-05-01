Readme, or don't. Make your own darn decisions!

Running the website:
<253 arctic:~/cse491-drinkz/bin >python make-test-database test_db.db
<254 arctic:~/cse491-drinkz/bin >python run-web test_db.db

6.1)
<261 arctic:~/cse491-drinkz >python server.py
Starting server on arctic 9061
Got connection from ('35.9.20.20', 48592)
got entire request: ('POST /rpc?hello HTTP/1.0\r\n\r\n',)
GOT POST /rpc?hello HTTP/1.0

<138 arctic:~/cse491-drinkz >python test_post.py arctic 9061
HTTP/1.0 200 OK
Content-Type: application/json

{"id": 1, "result": "world!", "error": null}

6.2)
When creating recipes there is now an option to add a rating to it. The rating of the recipeis displayed at the end of the recipe within the recipe list. In my make-test-database.py:

r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                        ('vermouth', '1.5 oz')])
    db.add_recipe(r)
    db.add_rating(r._recipeName,9)

6.3)
See save_db and load_db in db.py

6.4)
convertToMl uses an AJAX form in somefile.html

function do_convert() {
 b = $('input.b').val();
 $.ajax({
     url: '/rpc', 
     data: JSON.stringify ({method:'convert_units_to_ml', params:[b,], id:"0"} ),
     type: "POST",
     dataType: "json",
     success: function (data) { update_result(b,data.result) },
     error: function (err)  { alert ("Error");}
  });
}

6.5)
See login, logout, and status on app.py and on the website
