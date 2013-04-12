"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db, recipes                        # import from local packag


def data_reader(fp):
    
    reader = csv.reader(fp)
    
    for line in reader:
        if not line or not line[0].strip() or line[0].startswith('#') or len(line) != 3:
            continue

        (mfg, name, typ) = line

        yield line        
        
 

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    new_reader = data_reader(fp)

    x = []
    n = 0
    
    for (mfg, name, typ) in new_reader:
        try:
            db.add_bottle_type(mfg, name, typ)
            n+=1

        except ValueError:
            print 'failed to add to inv', mfg, name, typ
            continue
        
    return n
   

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    new_reader = data_reader(fp)

    x = []
    n = 0
    
    for (mfg, name, typ) in new_reader:
        try:
            db.add_to_inventory(mfg, name, typ)            
            n+=1

        except ValueError:
            print 'failed to add to inv', mfg, name, typ
            continue
        

    return n

def recipe_reader(fp):

    reader = csv.reader(fp)
    for line in reader:
        try:
            if line[0].startswith('#'):
                continue
            if not line[0].strip():
                continue

        except IndexError:
            pass

        try:
            recipe = line
            print recipe
        except ValueError:
            continue
        yield recipe 

def load_recipes(fp):

    new_reader = recipe_reader(fp)
    
    n = 0

    while(1):
        try:
            for recipe in new_reader:
                name = recipe[0]
                
                i = 1
                ingredients = []
                while(i<len(recipe)): 
                    i_name = recipe[i]
                    i_amount = recipe[i+1]
                    ing = (i_name, i_amount)
                    ingredients.append(ing)
                    i+=2
                r = recipes.Recipe(name, ingredients)
                db.add_recipe(r)
                n += 1
                
            new_reader.next()
        except StopIteration:
            break

    return n
