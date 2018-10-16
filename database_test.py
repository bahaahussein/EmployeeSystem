from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
 
from database_setup import Base, Employee, User, Attendance
 
engine = create_engine('sqlite:///employee.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()



date1 = datetime.date(2018, 10, 15)
date2 = datetime.date(2018, 9, 2)
date3 = datetime.date(2017, 1, 6)
employee1 = Employee(name = 'ahmed', email = 'ahmed@gmail.com', mobile_number = '0111', hire_date = date1)
employee2 = Employee(name = 'hefny', email = 'ahmed@gmail.com', mobile_number = '0222', hire_date = date2)
employee3 = Employee(name = 'benzema', email = 'benzema@gmail.com', mobile_number = '03333', hire_date = date3)
session.add(employee1)
session.commit()
session.add(employee2)
session.commit()
session.add(employee3)
session.commit()

user = User(name = 'ancheloti', email = 'ancheloti@gmail.com', password = '0123456')
session.add(user)
session.commit()

attendace = Attendance(status=0, day=datetime.date(2018, 10, 16), working_hours=8, employee=employee1)
session.add(attendace)

session.commit()

employees = session.query(Employee).all()
for employee in employees:
	print employee.name + " " + employee.email + " " + employee.mobile_number + " " + employee.hire_date.strftime("%y-%m-%d")
users = session.query(User).all()
for user in users:
	print user.name + " " + user.email + " " + user.password
