'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s):
Description: Project 1 - GPA Calculator
'''

# grade points for the traditional college letter grade scale, A+ included (so GPA can exceed 4.0)
GRADE_POINTS = {
    'A+': 4.3, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0
}

def calculate_gpa(enrollments):
    '''
    Returns the credit-weighted GPA. Each enrollment is a dict with a 'grade'
    and 'credits'. Ungraded or unknown grades are skipped. Returns 0 if
    nothing is graded.
    '''
    total_points = 0.0
    total_credits = 0
    for enrollment in enrollments:
        grade = enrollment.get('grade')
        credits = enrollment.get('credits')
        if grade not in GRADE_POINTS or not credits:
            continue
        total_points += GRADE_POINTS[grade] * credits
        total_credits += credits
    if total_credits == 0:
        return 0
    return total_points / total_credits