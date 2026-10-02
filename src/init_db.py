'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s):
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import Course


courses = [
    ("CS1010", 1010, "Introduction to Computer Science", 3),
    ("CS1020", 1020, "Data Structures and Algorithms", 4),
    ("CS1030", 1030, "Computer Architecture", 3),
    ("CS1040", 1040, "Operating Systems", 4),
    ("CS1050", 1050, "Database Systems", 3),
    ("CS1060", 1060, "Software Engineering", 4),
    ("CS1070", 1070, "Computer Networks", 3),
    ("CS1080", 1080, "Artificial Intelligence", 4),
]

with app.app_context():
    for prefix, number, name, credits in courses:
        pass
    print(f'Loaded {len(courses)} courses.')
