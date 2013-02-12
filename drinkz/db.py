"""
Database functionality for drinkz information.
"""

import string

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = dict()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set()
    _inventory_db = dict()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

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
        total_amount = add_strings(curr_amount, amount)
        _inventory_db[(mfg, liquor)] = total_amount
        
    else:
        _inventory_db[(mfg, liquor)] = amount
        

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
    
    x = 'ml'
    o = 'oz'
    
    
    for conversion in amounts:
        volume, measurement = conversion.split()
        volume = float(volume)
        measurement = measurement.lower()
            
        if measurement == x:
            total += volume
            
        elif measurement == o:
            vc = volume * 29.5735
            total += vc
        
        else:
            raise Exception('Unknown unit %s' % measurement)

    return '%s ml' % (total,)

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        print key
        yield key
        
def add_strings(str1, str2):
    total = 0.0
    x = 'ml'
    o = 'oz'
    
    volume, measurement =  str1.split()
    volume = float(volume)
    measurement = measurement.lower()
    
    curr_volume, curr_measurement = str2.split()
    curr_volume = float(curr_volume)
    curr_measurement = curr_measurement.lower()
    
    if measurement == x:
        total += volume
        
    elif measurement == o:
        v1 = volume * 29.5735
        total += v1
    
    else:
        raise Exception('Unknown unit %s' % measurement)
    
    if curr_measurement == x:
        total += curr_volume
        
    elif curr_measurement == o:
        v2 = curr_volume * 29.5735
        total += v2
    else:
        raise Exception('Unknown unit %s' % measurement)
    
    final = str(total)+' ml'
    return final

