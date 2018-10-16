from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Employee, User, Attendance
from datetime import datetime
import json

app = Flask(__name__)

engine = create_engine('sqlite:///employee.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def mainPage():
    if 'name' not in login_session:
        return redirect(url_for('showLogin'))
    employees = session.query(Employee).all()
    return render_template('index.html', employees=employees, name=login_session['name'])

@app.route('/login', methods=['GET', 'POST'])
def showLogin():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = session.query(User).filter_by(email=email).first()
        if user is None:
            response = make_response(json.dumps('Invalid email'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        if(user.password != password):
            response = make_response(json.dumps('Invalid password'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        login_session['name'] = user.name
        login_session['email'] = user.email
        return redirect(url_for('mainPage'))

@app.route('/new', methods=['GET', 'POST'])
def newEmployee():
    if 'name' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'GET':
        return render_template('newemployee.html')
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    date = getDate(request.form['date'])
    employee = Employee(name=name, email=email, mobile_number=mobile, hire_date=date)
    session.add(employee)
    session.commit()
    flash('New Employee %s is added' %name)
    return redirect(url_for('mainPage'))

@app.route('/employee/edit/<int:employee_id>', methods=['GET', 'POST'])
def editEmployee(employee_id):
    if 'name' not in login_session:
        return redirect(url_for('showLogin'))
    employee = session.query(Employee).filter_by(id=employee_id).one()
    if request.method == 'GET':
        return render_template('editemployee.html', employee=employee)
    isUpdated = False
    if request.form['name']:
        print 'entered Name'
        employee.name = request.form['name']
        isUpdated = True
    if request.form['email']:
        print 'entered email'
        employee.email = request.form['email']
        isUpdated = True
    if request.form['mobile']:
        print 'entered mobile'
        employee.mobile_number = request.form['mobile']
        isUpdated = True
    if request.form['date']:
        print 'entered date'
        employee.hire_date = getDate(request.form['date'])
        isUpdated = True
    if isUpdated:
        session.add(employee)
        session.commit()
        flash('Employee %s is updated' %employee.name)
    return redirect(url_for('mainPage'))

@app.route('/employee/delete/<int:employee_id>', methods=['GET', 'POST'])
def deleteEmployee(employee_id):
    if 'name' not in login_session:
        return redirect(url_for('showLogin'))
    employee = session.query(Employee).filter_by(id=employee_id).one()
    if request.method == 'GET':
        return render_template('deleteemployee.html', employee=employee)
    session.delete(employee)
    session.commit()
    flash('Employee %s is deleted' %employee.name)
    return redirect(url_for('mainPage'))

@app.route('/attendance/<int:employee_id>')
def showAttendance(employee_id):
    employee = session.query(Employee).filter_by(id=employee_id).one()
    attendances = session.query(Attendance).filter_by(employee_id=employee_id).all()
    return render_template('employeeattendances.html', attendances=attendances, employee=employee)

@app.route('/attendance/<int:employee_id>/new', methods=['GET', 'POST'])
def newAttendance(employee_id):
    if 'name' not in login_session:
        return redirect(url_for('showLogin'))
    employee = session.query(Employee).filter_by(id=employee_id).one()
    if request.method == 'GET':
        return render_template('addattendance.html', employee=employee)
    date = getDate(request.form['date'])
    hours = request.form['hours']
    status = request.form['status']
    attendance = Attendance(status=int(status), working_hours=hours, employee=employee, day=date)
    session.add(attendance)
    session.commit()
    return redirect(url_for('showAttendance', employee_id=employee.id))

@app.route('/report/<int:employee_id>/fromtodate', methods=['GET', 'POST'])
def fromToDate(employee_id):
    if 'name' not in login_session:
        return redirect(url_for('showLogin'))
    employee = session.query(Employee).filter_by(id=employee_id).one()
    if request.method == 'GET':
        return render_template('reportfromtodate.html', employee=employee)
    fromDate = getDate(request.form['from'])
    toDate = getDate(request.form['to'])


def getDate(date):
    return datetime.strptime(date, '%Y-%m-%d').date()

if __name__ == '__main__':
    print 'name = main'
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)