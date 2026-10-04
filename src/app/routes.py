'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Students: Carlos, Mason, Trevor, Abdal, Saran
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import User, Course, Enrollment
from app.forms import SignUpForm, LoginForm, EnrollmentForm, UpdateEnrollmentForm, DeleteEnrollmentForm, GRADE_CHOICES

from gpa_calculator import calculate_gpa
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data != form.passwd_confirm.data:
            form.passwd_confirm.errors.append('Passwords do not match.')
        elif User.query.filter_by(id=form.id.data).first():
            form.id.errors.append('That id is already taken.')
        else:
            hashed_passwd = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            new_user = User(
                id=form.id.data,
                name=form.name.data,
                about=form.about.data,
                passwd=hashed_passwd
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            return redirect(url_for('list_enrollments'))
        form.passwd.errors.append('Invalid id or password.')
    return render_template('login.html', form=form)

@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/enrollments')
@login_required
def list_enrollments():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    
    gpa_data = []
    
    for enrollment in enrollments:
        gpa_data.append({
            'grade': enrollment.grade,
            'credits': enrollment.course.credits
        })

    gpa = calculate_gpa(gpa_data)
    
    return render_template(
        'enrollments.html',
        enrollments=enrollments,
        gpa=gpa,
        delete_form=DeleteEnrollmentForm(),
        update_form=UpdateEnrollmentForm(),
        grade_choices=GRADE_CHOICES
    )


@app.route('/enrollments/delete/<course_prefix>/<course_number>', methods=['POST'])
@login_required
def delete_enrollment(course_prefix, course_number):
    
    form = DeleteEnrollmentForm()
    
    if form.validate_on_submit():
        
        enrollment = Enrollment.query.filter_by(
            user_id=current_user.id,
            course_prefix=course_prefix,
            course_number=course_number
        ).first()
        
        if enrollment:
            db.session.delete(enrollment)
            db.session.commit()
            
    return redirect(url_for('list_enrollments'))

@app.route('/enrollments/update/<course_prefix>/<course_number>', methods=['POST'])
@login_required
def update_enrollment(course_prefix, course_number):

    form = UpdateEnrollmentForm()

    if form.validate_on_submit():

        enrollment = Enrollment.query.filter_by(
            user_id=current_user.id,
            course_prefix=course_prefix,
            course_number=course_number
        ).first()

        if enrollment:
            enrollment.grade = form.grade.data
            db.session.commit()

    return redirect(url_for('list_enrollments'))

# TODO
@app.route('/enrollments/create', methods=['GET', 'POST'])
@login_required
def create_enrollment():
    
    form = EnrollmentForm()
    courses = Course.query.all()
    
    form.course.choices = [
        (f'{course.prefix}|{course.number}',
         f'{course.prefix} {course.number} - {course.name}'
        )
        for course in courses
    ]
    
    if form.validate_on_submit():
        
        course_prefix, course_number = form.course.data.split('|')
        
        existing_enrollment =Enrollment.query.filter_by(
            user_id=current_user.id,
            course_prefix=course_prefix,
            course_number=course_number
        ).first()
        
        if existing_enrollment:
            form.course.errors.append(
                'You are already enrolled in that course.'
                )
        
        else:
            enrollment = Enrollment(
                user_id=current_user.id,
                course_prefix=course_prefix,
                course_number=course_number,
                grade=form.grade.data
            )
            
            db.session.add(enrollment)
            db.session.commit()
            
            return redirect(url_for('list_enrollments'))
    
    return render_template(
        'create_enrollment.html',
        form=form
        )