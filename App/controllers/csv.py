import csv

from .admin import create_admin
from .review import create_review
from .staff import create_staff, get_staff_by_id
from .student import create_student, get_student_by_id
from .karmaSystem import update_karma, update_karma_ranking

def parse_users():
    with open('users.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for row in csvreader:
            username = row[0]
            firstname = row[1]
            lastname = row[2]
            password = row[3]
            email = row[4]
            user_type = row[5]

            if user_type == 'staff':
                create_staff(username=username, firstname=firstname, lastname=lastname, password=password, email=email)
            elif user_type == 'admin':
                create_admin(username=username, firstname=firstname, lastname=lastname, password=password, email=email)

def parse_students():
    with open('students.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for row in csvreader:
            student_id = row[0]
            system_id = row[1]

            create_student(student_id=student_id, system_id=system_id)

def parse_reviews():
    with open('reviews.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)

        for row in csvreader:
            staff_id = row[0]
            student_id = row[1]
            points = row[2]
            details = row[3]

            staff = get_staff_by_id(id=staff_id)
            student = get_student_by_id(id=student_id)

            create_review(staff=staff, student=student, points=points, details=details)
            update_karma(observer_id=student.id)
    update_karma_ranking(id=1)

def parse_all():
    parse_users()
    parse_students()
    parse_reviews()
    print('All Data Parsed')