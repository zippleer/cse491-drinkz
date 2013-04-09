#! /usr/bin/env python

import os
import sys
import drinkz.db
import drinkz.recipes


drinkz.db._reset_db()

#db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
#db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

#db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
#db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
    
#db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
#db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

#db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
#db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

#db.add_bottle_type('Various', 'Blue Curacao', 'liqeur')
#db.add_to_inventory('Various', 'Blue Curacao', '1 liter')

#db.add_bottle_type('Bombay', 'Sapphire', 'gin')
#db.add_to_inventory('Bombay', 'Sapphire', '750 ml')

#db.add_bottle_type('Bacardi', 'Gold', 'rum')
#db.add_to_inventory('Bacardi', 'Gold', '750 ml')

#db.add_bottle_type('Patron', 'Silver', 'tequila')
#db.add_to_inventory('Patron', 'Silver', '750 ml')
    
#r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
#db.add_recipe(r)

#r2 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
#db.add_recipe(r2)

#r3 = recipes.Recipe('Adios MotherF*cker!', [('tequila','1 oz'),('gin','1 oz'),('rum','1 oz'),('liquer','2 oz'),("Sprite","2 oz")])
#db.add_recipe(r3)

drinkz.db.load_db("bin/test_database")


try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

###

fp = open('html/index.html', 'w')



print >>fp, """

<a href='recipes.html'>Recipes</a></br>
<a href='inventory.html'>Inventory</a></br>
<a href='liquor_types.html'>Liquor Types</a></br>

"""

fp.close()

################################################

fp = open('html/recipes.html', 'w')

print >>fp,"""

<table border=\"1\" cellpadding =\"5\">
<tr><th>Name</th><th>Ingredients</th><th>Check those ingredients!</tr>
"""
recipes = drinkz.db.get_all_recipes()
for recipe in recipes:
    print >>fp,"<tr><td> %s </td><td><table cellpadding =\"5\">" % recipe.name
    for item in recipe.ingredients:
        print >>fp, "<tr><td> %s </td><td> %s </td></tr>" % item
    print >>fp,"</table></td><td>"

    
    #missing = recipe.need_ingredients()
    #if(missing):
    if len(recipe.need_ingredients()) > 0:
        print >>fp,"Hell Nah!"
    else:
        print >>fp,"Hell Yeah!"
    
    print >>fp,"</td></tr>"


print >>fp,"""
</table>
"""

print >>fp, """

<a href='index.html'>Home</a></br>
<a href='inventory.html'>Inventory</a></br>
<a href='liquor_types.html'>Liquor Types</a></br>

"""

fp.close()

################################################
fp = open('html/liquor_types.html', 'w')


print >>fp, "<b>Liquor Types</b><p>Manufacturer, Liquor Type</p><ul>"

for mfg, liquor in drinkz.db.get_liquor_inventory():
    print >>fp, "<p> </p>"
    print >>fp, '<li> %s, %s' % (mfg, liquor)

print >>fp, "</ul>"

print >>fp, """

<p><a href='index.html'>Back to Index</a>
</p>
<p><a href='recipes.html'>Recipes</a>
</p>
<p><a href='inventory.html'>Inventory</a>
</p>
"""
fp.close()
###########################################33
fp = open('html/inventory.html', 'w')

print >>fp, "<b>Inventory</b><p>Manufacturer, Liquor Type, Amount (ml)</p><ul>"
for mfg, liquor in drinkz.db.get_liquor_inventory():
    #print mfg + "              " + liquor + "          " + drinkz.db.get_liquor_amount(mfg,liquor)
    print >>fp, "<p> </p>"
    print >>fp , "<li> %s,  %s, %s" % (mfg, liquor, drinkz.db.get_liquor_amount(mfg,liquor))
    
print >>fp, "</ul>"

print >>fp, """

<p><a href='index.html'>Back to Index</a>
</p>
<p><a href='recipes.html'>Recipes</a>
</p>
<p><a href='liquor_types.html'>Liquor Types</a>
</p>
"""

fp.close()
