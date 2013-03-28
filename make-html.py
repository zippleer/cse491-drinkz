#! /usr/bin/env python

import os
from drinkz import db
from drinkz import recipes

db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
    
db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

db.add_bottle_type('Various', 'Blue Curacao', 'liqeur')
db.add_to_inventory('Various', 'Blue Curacao', '1 liter')

db.add_bottle_type('Bombay', 'Sapphire', 'gin')
db.add_to_inventory('Bombay', 'Sapphire', '750 ml')

db.add_bottle_type('Bacardi', 'Gold', 'rum')
db.add_to_inventory('Bacardi', 'Gold', '750 ml')

db.add_bottle_type('Patron', 'Silver', 'tequila')
db.add_to_inventory('Patron', 'Silver', '750 ml')
    
r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
db.add_recipe(r)

r2 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
db.add_recipe(r2)

r3 = recipes.Recipe('Adios MotherF*cker!', [('tequila','1 oz'),('gin','1 oz'),('rum','1 oz'),('liquer','2 oz'),("Sprite","2 oz")])
db.add_recipe(r3)



try:
    os.mkdir('html')

except OSError:
    # already exists
    pass

# index
fp = open('html/index.html', 'w')

print >>fp, "<b> I'm not slurring my words, I'm just talking in cursive officer!!!</b>"

print >>fp, "<p><a href='recipes.html'>Recipes</a>"
print >>fp, "<p><a href='inventory.html'>Inventory</a>"
print >>fp, "<p><a href='liquor_types.html'>Liquors</a>"
print >>fp, "<a href = 'form'>Convert-to-html<a/>"
fp.close()
#

# recipes
recipes = db.get_all_recipes()

fp2 = open('html/recipes.html', 'w')

r_string = "<b>Recipes</b>\n\n<ul>"

for recipe in recipes:
    r_html = recipe.get_html()
    r_string += '<li>' + r_html + '</li>\n'

r_string+= '</ul>'

print >>fp2, r_string

fp2.close()

# inv

fp3 = open('html/inventory.html', 'w')

i_string = "<b>Inventory</b>\n\n<table>\n "

for item in db.get_liquor_inventory():
    m = item[0]
    l = item[1]
    amount = db.get_liquor_amount(m,l)
    i_string += '<tr>\n' + '<td>' +  m + '</td>\n'
    i_string += '  <td>:  ' + l + '      </td>\n'
    i_string += '  <td>:<i>      ' + str(amount) + ' ml </i> </td>\n </tr>\n'

print >>fp3, i_string
fp3.close()

# types

fp4 = open('html/liquor_types.html', 'w')
t_string = "<b>Liquor Types</b>\n<ul>\n\n"
for m, l in db.get_liquor_inventory():
    t_string += '<li>' +  '<b>%s</b>  \t  <i>%s</i>' % (m, l) + '</li>\n'

t_string += '</ul>'

print >>fp4, t_string

fp4.close()
