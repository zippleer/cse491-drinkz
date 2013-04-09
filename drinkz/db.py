"""
Database functionality for drinkz information.
"""

from cPickle import dump, load

import os

import recipes


# private singleton variables at module level
_bottle_types_db = set(tuple())
_inventory_db = {}
_recipe_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set(tuple())
    _inventory_db = {}
    _recipe_db = {}


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

def convert_to_ml(amount):
        
		volume,unit = amount.split()
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

# Input r: recipe object
# Output: False if a recipe with the same name exists
#         True otherwise
def add_recipe(r):  
    if r.name not in _recipe_db:
        _recipe_db[r.name]=r
    else:
        raise DuplicateRecipeName()


def get_recipe(name):
    if name not in _recipe_db:
	    return None
    return _recipe_db[name]        


def get_all_recipe_names():
    return _recipe_db.keys()
    

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
        curr_amount = convert_to_ml(amount)
        prev_amount = get_liquor_amount(mfg, liquor)
        new_amount = float(curr_amount) + float(prev_amount)
        _inventory_db[(mfg, liquor)] = str(new_amount) + ' ml'
    else:
        _inventory_db[(mfg, liquor)] = amount
    

def check_inventory(mfg, liquor):
    for key in _inventory_db:
        if mfg == key[0] and liquor == key[1]:
            return True
        
    return False


def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    for key in _inventory_db:
        if mfg == key[0] and liquor == key[1]:
           amounts.append(_inventory_db[key])
            
    total_ml = 0.0

    for i in amounts:
        total_ml += float(convert_to_ml(i))    

    return total_ml 

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key[0], key[1]
        
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


    

