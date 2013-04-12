import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded;
import os

from . import db, load_bulk_data
from cStringIO import StringIO
import imp


def test_script_load_liquor_recipes():
    db._reset_db()

    scriptpath = 'bin/load-liquor-recipes'
    module = imp.load_source('llt', scriptpath)

    exit_code = module.main([scriptpath, 'test-data/test_rec.txt'])

    assert exit_code == 0
    assert 'Abe Lincoln' in db.get_all_recipe_names()
    assert 'Adios Mother F*cker' in db.get_all_recipe_names()
    assert len(db._recipe_db)==2
