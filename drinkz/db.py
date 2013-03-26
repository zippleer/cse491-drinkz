"""
Database functionality for drinkz information.
"""

import string
import drinkz.recipes

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipe_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set()
    _inventory_db = dict()
    _recipe_db = dict()

def convert_to_ml(amount):
        
		volume,unit = amount.split(" ")
		unit = unit.lower()
		total = 0
        
		if unit == "oz":
			total += float(volume)*29.5735
            
		elif unit == "ml":
			total += float(volume)
            
		elif unit == "liter":
			total += float(volume)*1000.0

		elif unit == "liters":
			total += float(volume)*1000.0
            
		elif unit == "gallon":
			total += float(volume)*3785.41178

		elif unit == "gallons":
			total += float(volume)*3785.41178

		else:
			raise Exception('Unknown unit %s' % measurement)
            
		return total

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
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

	if (mfg, liquor) in _inventory_db:
		curr_amount = _inventory_db[(mfg, liquor)]
		total_amount = add_amounts(curr_amount, amount)
		_inventory_db[(mfg, liquor)] = total_amount

	else:
		volume = db.convert_to_ml(amount)
		_inventory_db[(mfg, liquor)] = volume
        

def check_inventory(mfg, liquor):
    for key in _inventory_db:
        if key == (mfg,liquor):
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    
    for key in _inventory_db:
        if key == (mfg, liquor):
            amounts.append(_inventory_db[key])
    
    total = 0.0
    
    for volume in amounts:
        total += volume

    return total

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        print key
        yield key
        
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
            type_list.append((m,l))
            
    return type_list
    

