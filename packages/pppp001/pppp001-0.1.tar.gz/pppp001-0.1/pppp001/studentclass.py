class Student:
	def __init__(self,name): #must have name
		self.name = name
		self.exp = 0
		self.lesson = 0
		# call function
		self.AddEXP(10)

	def Hello(self):
		print('Hola... i am {}'.format(self.name))

	def Coding(self):
		print('now coding')
		self.exp += 5
		self.lesson += 1

	def ShowEXP(self):
		print('{} has {} EXP'.format(self.name,self.exp))
		print('for {} time'.format(self.lesson))

	def AddEXP(self,score):
		self.exp += score
		self.lesson += 1


class SpecialStudent(Student): #import student class

	def __init__(self,name,father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates','Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddEXP(self,score):
		self.exp += score * 3
		self.lesson += 1

	def AskEXP(self,score=10):
		print('Give me {} score!!!'.format(score))
		self.AddEXP(score)

print('Main: ',__name__)

if __name__ == '__main__':

	print('===1 jan===')
	student0 = SpecialStudent('Mark Zuckerberg','Bill Gates')
	student0.AskEXP()
	student0.ShowEXP()

	student1 = Student('Albert')
	print(student1.name)
	student1.Hello()

	print('--------------------')
	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()

	print('===2 jan===')
	student1.AddEXP(20)
	print(student1.name,student1.exp)
	print(student2.name,student2.exp)

	for i in range(5):
		student2.Coding()

	student1.ShowEXP()	
	student2.ShowEXP()
