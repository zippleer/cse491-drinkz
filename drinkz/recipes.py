#Recipe Class

import db

class Recipe(object):  
	def __init__(self, n = '', i =[]):
		self.name = n
		self.ingredients = i
        
#	def need_ingredients(self):
#		needed = []
#
#		for(typ, amount) in self.ingredients:
#			matching = db.check_inventory_for_type(typ)
#
#			max_m = ''
#			max_l = ''
#			max_amount = 0.0
#
#			for (m, l ,t) in matching:
#				if t > max_amount:
#					max_amount = t
#
#			amount_needed = db.convert_to_ml(amount)
#
#			if max_amount < amount_needed:
#				needed.append((typ, amount_needed - max_amount))
#
#		return needed
                    
        
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


	def need_ingredients(self):

		missing_list = []

        # PUT ALL THE LIQUOR TYPES NEEDED IN A LIST(see if they exist) ===========
		bottle_type_list = []
        
		for i in self.ingredients:
		    for item in db._bottle_types_db:
				if  i[0] == item[2]:
				    bottle_type_list.append(item)

        #print bottle_type_list, "bottle_type_list"

        #=========================================================================


        # CHECK INVENTORY FOR THOSE LIQUORS(put them in a list of tuples)=========

		amounts_list = []

		for i in bottle_type_list:
		    if db.check_inventory(i[0], i[1]):
				amount = (i[0], i[2], db.get_liquor_amount(i[0], i[1]))
				amounts_list.append(amount)


        #print amounts_list, "amounts_list"

        # CREATE THE MISSING LIST=================================================

        
                
		for i in self.ingredients:
			amount = 0.0
			for item in amounts_list: #replace smaller amount with larger
				if i[0]==item[1]:
					if amount < float(item[2]): 
						amount = float(item[2])
			ing_amount = db.convert_to_ml(i[1])#convert the ingredient to ml
            
			if float(amount) < float(ing_amount):#compare the amount with ing
				needed = float(ing_amount)-float(amount)
				needed_tup = (i[0], needed)
				missing_list.append(needed_tup)#add to missing list


		return missing_list
