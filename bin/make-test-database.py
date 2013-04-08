import sys
import _mypath

import drinkz.db, drinkz.recipes

def main(args):
    drinkz.db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    drinkz.db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

    drinkz.db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    drinkz.db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        
    drinkz.db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    drinkz.db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

    drinkz.db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    drinkz.db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    r = drinkz.recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
    drinkz.db.add_recipe(r)

    r2 = drinkz.recipes.Recipe('vomit inducing martini', [('orange juice', '6 oz'), ('vermouth', '1.5 oz')])
    drinkz.db.add_recipe(r2)

    r3 = drinkz.recipes.Recipe('whiskey bath', [('blended scotch', '6 liter')])
    drinkz.db.add_recipe(r3)
    
    filename = args[1]

    drinkz.db.save_db(filename)

if __name__ == '__main__':
    main(sys.argv)
