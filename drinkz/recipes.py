#Recipe Class

import db

class Recipe(object):  
	def __init__(self, name, ingredients):
		self.name = name
		self.ingredients = ingredients
        
	def need_ingredients(self):
		needed = []
		for(typ, amount) in self.ingredients:
			matching = db.check_inventory_for_type(typ)

			max_m = ''
			max_l = ''
			max_amount = 0.0

			for (m, l ,t) in matching:
				if t > max_amount:
					max_amount = t

			amount_needed = db.convert_to_ml(amount)

			if max_amount < amount_needed:
				needed.append((typ, amount_needed - max_amount))

		return needed
                    
        
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

