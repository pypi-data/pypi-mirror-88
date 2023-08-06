ตัวอย่างโปรแกรมหัดเขียนPython
==================================

วิธีติดตั้ง
~~~~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

	pip install PtPclass


วิธีเล่น
~~~~~~~~~~~~~~
เปิด IDLE ขึ้นมาแล้วพิมพ์...

.. code:: python

	from PtPclass import Student, StudentSpecial

	print('=======1 Jan=======')	
	student0 = SpecialStudent('Will', 'Gates')
	student0.AskEXP()
	student0.ShowEXP()


	student1 = Student('Albert')
	print(student1.name)
	student1.Hello()

	print('--------------')
	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()
	print('=======2 Jan=======')
	print('----------uncle: ใครอยากเรียนโคดดิ้ง?-------(ให้ 10 exp)')

	print('=======3 Jan=======')

	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่กันแล้ว')

	print(student1.name, student1.exp)
	print(student2.name, student2.exp)
	print('=======4 Jan=======')

	for i in range(5):
		student2.Coding()

	student1.ShowEXP()
	student2.ShowEXP()




พัฒนาโดย: Phet THEPVONGSA
