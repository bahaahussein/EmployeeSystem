import sys
from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Employee(Base):
	__tablename__ = 'employee'
	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	email = Column(String)
	mobile_number = Column(String)
	hire_date = Column(DateTime)

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	name = Column(String, nullable = False)
	email = Column(String,)
	password = Column(String, nullable = False)

class Attendance(Base):
	__tablename__ = 'attendance'
	id = Column(Integer, primary_key = True)
	status = Column(Integer, nullable = False)
	employee_id = Column(Integer, ForeignKey('employee.id'))
	employee = relationship(Employee)
	working_hours = Column(Integer)
	day = Column(DateTime)
	def getStatus(self):
		if self.status == 0:
			return 'Present'
		elif self.status == 1:
			return 'Absent'
		elif self.status == 2:
			return 'Sick Leave'
		else:
			return 'Day Off'


engine = create_engine('sqlite:///employee.db')
Base.metadata.create_all(engine)