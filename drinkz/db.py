"""
Database functionality for drinkz information.
"""

from cPickle import dump, load


# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipe_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipe_db = {}

def convert_to_ml(amount):
        
		volume,unit = amount.split(" ")
		unit = unit.lower()
		volume = float(volume)
        
		if unit == "oz":
			volume = volume*29.5735
            
		elif unit == "ml":
			pass
            
		elif unit == "liter":
			volume = volume*1000.0

		elif unit == "liters":
			volume = volume*1000.0
            
		elif unit == "gallon":
			volume = volume*3785.41

		elif unit == "gallons":
			volume = volume*3785.41

		else:
			raise Exception('Unknown unit %s' % unit)
            
		return volume

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

def add_recipe(r):  
    _recipe_db[r.name] = r
        
        
def get_recipe(name):
    if name in _recipe_db:
        return _recipe_db[name]
    else:
        return 0
    

def get_all_recipes():
    return _recipe_db.values()

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True
    return False

def add_to_inventory(mfg, liquor, amount):

    volume = 0.0
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err) 

    if (mfg, liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)].append(amount)
    else:
        _inventory_db[(mfg, liquor)] = []
        _inventory_db[(mfg, liquor)].append(amount)
    

def check_inventory(mfg, liquor):
        
    return ((mfg, liquor) in _inventory_db)

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    added = _inventory_db[(mfg, liquor)]
    volume = 0.0

    for value in added:
        value = convert_to_ml(value)
        volume += value

    return str(volume) + ' ml'


def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for m, l in _inventory_db:
        yield m, l
        
def add_amounts(value, str2): 
	total = 0.0
	total += value
    
	new_val = convert_to_ml(str2)
	total += new_val
    
	return total

def check_inventory_for_type(typ):
    type_list = list()
    
    for (m, l, t) in _bottle_types_db:

        if t == typ:
            amount = _inventory_db.get((m, l), 0.0)
            type_list.append((m,l, amount))
            
    return type_list


def save_db(filename):
	fp =open(filename, 'wb')

	saveit = (_bottle_types_db, _inventory_db, _recipe_db)
	dump(saveit, fp)

	fp.close()

def load_db(filename):
	global _bottle_types_db, _inventory_db, _recipe_db
	fp =open(filename, 'rb')

	loader = load(fp)

	(_bottle_types_db, _inventory_db, _recipe_db) = loader

	fp.close()
    

