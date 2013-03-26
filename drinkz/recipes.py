#Recipe Class

import db

class Recipe(object):  
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
        
    def need_ingredients(self):
        supply_list = list()
        
        for curr_item in self.ingredients:
            banked = 0
            
            tup_list = db.check_inventory_for_type(curr_item[0])

            for tup in tup_list:
                amount = db.get_liquor_amount(tup[0],tup[1])
                
                if amount>banked:
                    banked = amount
                    
            how_short = banked - db.convert_to_ml(curr_item[1])
            
            if ( how_short < 0 ):
                supply_list.append((curr_item[0],how_short*-1.))
                
        return supply_list
                    
        
    def __str__(self):
        r_string = self.name + ': '
        for item in self.ingredients:
            r_string += ' ' + item[0] + '- ' + item[1]
        return r_string

    def get_html(self):
        r_string = '<b>' + self.name + '</b>: '
        for item in self.ingredients:
            r_string += ' ' + item[0] + '- <i>' + item[1] + '</i>'

        if self.need_ingredients():
            r_string +=  '\t\t<b>Heck yes!</b>' 
        else:
            r_string +=  '\t\t<b>Heck no!</b>' 

        return r_string

