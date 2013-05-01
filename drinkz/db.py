"""
Database functionality for drinkz information.
"""
import cPickle
import recipes
import sqlite3
import base64

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()
_ratings = {}


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = set()
    _ratings = {}

def save_db(filename):

    # we could just pickle everything and put it into the sql table,
    # but i wasn't sure if that was cheating so i made seperate tables
    
    conn = sqlite3.connect(filename)

    c = conn.cursor()

  # Clear any existing tables
    c.execute('''drop table if exists bottle_types''')
    c.execute('''drop table if exists inventory''')
    c.execute('''drop table if exists recipes''')
    c.execute('''drop table if exists ratings''')

  # Create tables
    c.execute('''CREATE TABLE bottle_types
                 (mfg text,liquor text,typ text)''')
    c.execute('''CREATE TABLE inventory
                 (mfg text,liquor text,amount text)''')

    c.execute('''CREATE TABLE ratings
                 (recipe text, rating int)''')
    
    c.execute('''CREATE TABLE recipes
                 (recipe text)''')


    for val in _bottle_types_db:
        c.execute("INSERT INTO bottle_types (mfg,liquor,typ) VALUES (?,?,?)",val)    

    for val in _inventory_db:
        (val1,val2) = val
        val3 = _inventory_db[val]
        c.execute("INSERT INTO inventory (mfg,liquor,amount) VALUES (?,?,?)",(val1,val2,val3))

    for val in _ratings:
        #rec = _recipes_db.get_recipe(val)
        #name = rec._recipeName
        val1 = _ratings[val]
        c.execute("INSERT INTO ratings (recipe, rating) VALUES (?,?)",(val,val1))      
        

    for val in _recipes_db:
            serialized = cPickle.dumps(val)
            
            c.execute("INSERT INTO recipes (recipe) VALUES (?)",[sqlite3.Binary(serialized)]) 

    c.execute('SELECT * FROM bottle_types')
    conn.commit()
    conn.close()

def load_db(filename):

    db = sqlite3.connect(filename)
    c = db.cursor()
    
    c.execute('SELECT * FROM bottle_types')
    results = c.fetchall()
    for (mfg,liquor,typ)in results:
        add_bottle_type(mfg,liquor,typ)
        
    c.execute('SELECT * FROM inventory')
    results = c.fetchall()
    for (mfg,liquor,amount) in results:
        
        add_to_inventory(mfg, liquor, amount+' ml')

    c.execute('SELECT * FROM ratings')
    results = c.fetchall()
    for (recipe, rating) in results:
        
        add_rating(recipe, rating)
    
    for row in c.execute("select * from recipes"):
        add_recipe(cPickle.loads(str(row[0])))

    c.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass
class DuplicateRecipeName(Exception):
    pass
def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False


def add_rating(recipe, rating):
    try:
        _ratings[recipe] = rating
    except KeyError:
        _ratings[recipe] = {}
        _ratings[recipe] = rating       

def get_rating(recipe):
    return _ratings[recipe]
    

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    total = convert_to_ml(amount)
        
    if (mfg,liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)] += total
    else:
        _inventory_db[(mfg, liquor)] = total

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    total = 0
    for (m, l) in _inventory_db:
        if mfg == m and liquor == l:
            total = float(str(_inventory_db[(m,l)]))

    return float("%.2f" % total)

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db:
        yield m, l

def get_liquor_types():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l,_) in _bottle_types_db:
        yield m, l

def add_recipe(r):
    found = False
    for recipe in _recipes_db:
        if recipe._recipeName == r._recipeName:
            raise DuplicateRecipeName
    _recipes_db.add(r)
    #if r._recipeName not in _ratings:
        #_ratings[r._recipeName] = {}
    
def get_recipe(name):
    for recipe in _recipes_db:
        if name == recipe._recipeName:            
            return recipe
    return 0

def get_all_recipes():
    return _recipes_db

def check_inventory_for_type(typ):
    myList = list()
    
    for (m, l, t) in _bottle_types_db:

        if(typ == t or typ == l): #checks for generic or label
            myList.append((m,l))
    return myList


def convert_to_ml(amount):
    amounts = amount.split(" ")
    total = 0
    if amounts[1] == "oz":
        total += float(amounts[0])*29.5735
    elif amounts[1] == "ml":
        total += float(amounts[0])
    elif amounts[1] == "liter":
        total += float(amounts[0])*1000.0
    elif amounts[1] == "gallon":
        total += float(amounts[0])*3785.41
    return total

def get_bottle_types():
    for bottle in _bottle_types_db:
        yield bottle


