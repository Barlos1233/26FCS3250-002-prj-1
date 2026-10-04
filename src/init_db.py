'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Students: Carlos, Mason, Trevor, Abdal, Saran
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import Course


courses = [
    ("CS", "1010", "Introduction to Computer Science", 3),
    ("MTH", "1410", "Calculus I", 4),
    ("CS", "3240", "Intro to Theory of Computation", 2),
    ("CS", "3700", "Networking & Distributed Computing", 4),
    ("MTH", "3210", "Probability and Statistics", 4)
]

with app.app_context():
    for prefix, number, name, credits in courses:
        db.session.add(Course(
            prefix=prefix,
            number=number,
            name=name,
            credits=credits
        ))
    db.session.commit()
    print(f'Loaded {len(courses)} courses.')
