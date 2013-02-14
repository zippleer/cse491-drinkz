"""
Tests basic recipe API.
"""

import unittest
from . import db, recipes

class TestBasicRecipeStuff(unittest.TestCase):
    def setUp(self):                    # This is run once per test, before.
        db._reset_db()

    def tearDown(self):                 # This is run once per test, after.
        pass

    def test_add_recipe_1(self):
        x = list(db.get_all_recipes())
        assert not x                    # should be no recipes
        
        r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                                   '4 oz')])

        db.add_recipe(r)

        x = list(db.get_all_recipes())
        assert len(x) == 1              # should be only one recipe
        assert r in x

    def test_get_recipe_2(self):
        r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                                   '4 oz')])
        db.add_recipe(r)
            
        r2 = recipes.Recipe('scotch on the rocks', [('vodka', '4 oz')])
        try:
            db.add_recipe(r2)
            assert 0, "this is a duplicate recipe and the add should fail"
        except db.DuplicateRecipeName:
            pass                        # success, we got an exception

    def test_get_recipe_1(self):
        r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                                   '4 oz')])

        db.add_recipe(r)

        x = db.get_recipe('scotch on the rocks')
        assert x == r

    def test_get_recipe_2(self):
        x = db.get_recipe('scotch on the rocks')
        assert not x, x                    # no such recipe

class TestIngredients(object):
    def setUp(self):
        db._reset_db()

        db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
        db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')
        
        db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
        db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

        db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
        db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    def test_need_ingredients_1(self):
        r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                                   '4 oz')])

        assert not r.need_ingredients()

    def test_need_ingredients_2(self):
        r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                            ('vermouth', '1.5 oz')])

        assert not r.need_ingredients()

    def test_need_ingredients_3(self):
        r = recipes.Recipe('vomit inducing martini', [('orange juice',
                                                      '6 oz'),
                                                     ('vermouth',
                                                      '1.5 oz')])

        x = r.need_ingredients()
        assert x
        assert len(x) == 1

        assert x[0][0] == 'orange juice'
        assert x[0][1] == '@@@' # 6 oz in ml @CTB
