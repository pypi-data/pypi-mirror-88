class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0

		#call function
		#self.AddExp(10)

	def Hello(self):
		print('สวัสดีจ้าาา ฉันชื่อ {}'.format(self.name))	

	def Coding(self):
		print('{} กำลังเขียนโปรแกรม'.format(self.name))		
		self.exp += 5
		self.lesson += 1

	def ShowExp(self):
		print('{} ประสบการณ์ {} EXP'.format(self.name,self.exp))
		print('เรียนไป {} ครั้งแล้ว'.format(self.lesson))	

	def AddExp(self,score):
		self.exp += score
		self.lesson += 1
			


class SpecialStudent(Student):#inheritance
	def __init__(self,name,father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates','Thomas Edison','Thumpt']
		if father in mafia:
			self.exp = 100


	def AddExp(self,score):
		self.exp += (score * 3)
		self.lesson += 1


	def AskExp(self,score = 10):
		print('ครู! ขอคะแนนพิเศษหน่อยสัก {} exp'.format(score))
		self.AddExp(score)	

print ('main name: ', __name__)
if __name__ == '__main__':


	student0 = SpecialStudent('Mark','Bill Gates')

	student0.Hello()
	student0.AskExp()
	student0.ShowExp()

	student1 = Student('navapol')

	student1.Hello()
	student1.AddExp(10)

	student2 = Student('Steve')

	student2.Hello()
	student2.Coding()

	student1.name = 'Albert Einstain'

	for i in range(5):
		student2.Coding()

	student1.ShowExp()
	student2.ShowExp()
