class Submarine:

	'''

	-------------------
	Test Documentation

	Program for submarine 
	-------------------

	'''

	#class that you can put  many functions
	#def that you put object

	def __init__(self,price=10000,budget=400000,battery_distance=10000): #self is reference of object/ price=10000 , budget = 
		self.cap_name = 'Chris'
		self.sub_name = 'Navy Force'
		self.price = price #milion
		self.kilometre = 0 #setting 0
		self.budget = budget
		self.totalcost = 0 #setting 0
		self.battery_distance = battery_distance


	def Missile(self):
		print('We are Department of Missile')

	def Calcommission(self):
		percent =  self.price * (10/100) #commissiom 10%
		print('Congrat! You got:  {} Million AUD'.format(percent))

	def Goto(self,enemypoint,distance):
		print(f"Let's go to {enemypoint} Distance: {distance} km")
		self.kilometre = self.kilometre + distance #self.kilometre += distance
		self.Fuel()


	def Fuel(self):
		diesel = 20 #per litre
		cal_fuel_cost = self.kilometre * diesel
		print('Current fuel cost: {:,d} AUD'.format(cal_fuel_cost))
		self.totalcost += cal_fuel_cost

	@property
	def BudgetRemaining(self):
		remaining = self.budget - self.totalcost
		print('Budget Remaining: {:,.2f} AUD'.format(remaining))
		return remaining


class ElectricSubmarine(Submarine): 

	def __int__(self,price=10000,budget=400000,battery_distance=100000):
		self.sub_name = 'Stark II'
		super().__init__(price,budget,battery_distance) #super()transfer/copy every function into class ElectricSubmarine
		#sybmarine can go out 10000km/ 100 percent



	def Battery(self):
		allbattery = 100
		print('kilometre',self.kilometre)
		calculate = (self.kilometre / self.battery_distance) * 100
		print('CAL: ',calculate)
		
		print('We have battery remaining: {}%'.format(allbattery-calculate)) 



	def Fuel(self):
		kilowattcost = 5 #per kilowatt
		cal_fuel_cost = self.kilometre * kilowattcost
		print('Current Power cost: {:,d} AUD'.format(cal_fuel_cost))
		self.totalcost += cal_fuel_cost

print(__name__)
if __name__== '__main__':

	tesla = ElectricSubmarine(40000,2000000,100000) #price+budget
	print(tesla.cap_name)
	print(tesla.budget)
	tesla.Goto('Japan',10000)
	print(tesla.BudgetRemaining) #call function fuel in fucntion Budgetremaining
	tesla.Battery()


	print('-------------------------------------')

	Navykongtab = Submarine(40000,2000000,10000) #price+budget
	print(Navykongtab.cap_name)
	print(Navykongtab.budget)
	Navykongtab.Goto('Japan',10000)
	print(Navykongtab.BudgetRemaining)

'''
Navykongtab = Submarine(1000)  #calculate here with amount
print(Navykon
gtab.cap_name) #ref object or Navykongtab
print(Navykongtab.sub_name)
print('-------------------')
print(Navykongtab.kilometre)
Navykongtab.Goto('China',7000)
print(Navykongtab.kilometre)
Navykongtab.Fuel()
#Navykongtab.BudgetRemaining() > from @property
current_budget = Navykongtab.BudgetRemaining
print(current_budget * 0.2)

#compare to non-function
#sub  =  ['Chris','NavyForce2',5000]
#print(sub[0])

Navykongtab.Calcommission()
########################################
print('-------------Sub no.2--------------')
print('Before..')
Military = Submarine(70000)
print(Military.cap_name)
print('After..')
Military.cap_name = 'Evan'
print(Military.cap_name)
'''
