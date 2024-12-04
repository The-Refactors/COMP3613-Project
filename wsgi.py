import click, pytest, sys
import nltk
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import (
    create_student, create_staff, create_admin, create_review, get_student_by_id, get_student_by_student_id, get_staff_by_id,
    get_student_reviews, get_all_students, get_all_users, get_all_users_json, get_all_admins, get_all_admins_json,
    get_all_staff, get_all_staff_json, get_all_reviews, create_karma_system, update_karma, update_karma_ranking,
    get_all_students_json, print_karma_ranking, update_username, update_password, get_user, update_name, update_email,
    delete_user, get_all_reviews_json, get_review, update_review_staff, update_review_student, update_review_points,
    update_review_details, delete_review, get_student_reviews_json, get_student_by_student_id_json, delete_student, get_karma_ranking_json)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

system_id = 1 # id of karma ranking system that all students observe


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  
  create_admin(username="bobby", firstname="Bob", lastname="Harris", email="bob@mail.com", password="bobpass")
  create_admin(username="lyss", firstname="Alyssa", lastname="Smith", email="alyssa@mail.com", password="lysspass")

  create_staff(username="henry", firstname="Henry", lastname="John", email="henry@mail.com", password="henrypass")
  create_staff(username="mike", firstname="Michael", lastname="Williams", email="mike@mail.com", password="mikepass")
  create_staff(username="cattie", firstname="Catherine", lastname="Singh", email="cattie@mail.com", password="cattiepass")

  create_karma_system()

  create_student(student_id='816011111', system_id=system_id)
  create_student(student_id='816022222', system_id=system_id)
  create_student(student_id='816033333', system_id=system_id)
  create_student(student_id='816044444', system_id=system_id)
  create_student(student_id='816055555', system_id=system_id)

  print("Database Initialized")


@app.cli.command("karma", help="Lists the karma rankings")
@click.argument("format", default="string")
def list_karma(format):
    if format == "string":
        print_karma_ranking(system_id)
    else:
        print(get_karma_ranking_json(system_id))


'''
User Commands
'''
user_cli = AppGroup('user', help= 'User Commands')

@user_cli.command("add", help="Adds a new user")
@click.argument("type", type=click.Choice(["staff", "admin"]))
@click.argument("username")
@click.argument("firstname")
@click.argument("lastname")
@click.argument("password")
@click.argument("email")
def create_user_command(type, username, firstname, lastname, password, email):
    user = None

    if type == "admin":
        user = create_admin(username, firstname, lastname, password, email)
    elif type == "staff":
        user = create_staff(username, firstname, lastname, password, email)

    if user:
        print(f'New {type} created with username: {username}, name: {firstname} {lastname}, email: {email}')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
@click.argument("type", type=click.Choice(["all", "staff", "admin"]), default="all")
def list_user_command(type, format):
    if type == "all":
        if format == 'string':
            print(get_all_users())
        else:
            print(get_all_users_json())
    if type == "staff":
        if format == 'string':
            print(get_all_staff())
        else:
            print(get_all_staff_json())
    if type == "admin":
        if format == 'string':
            print(get_all_admins())
        else:
            print(get_all_admins_json())

@user_cli.command("update", help="Updates given attribute of the user")
@click.argument("userid", type=int)
@click.argument("field", type=click.Choice(["username", "password", "firstname", "lastname", "email"]))
@click.argument("data")
def update_user_command(field, userid, data):
    check = False
    user = get_user(userid)

    if not user:
        print("User not found. Exiting...")
        return

    if field == "username":
        check = update_username(userid, data)
    if field == "password":
        check = update_password(userid, data)
    if field == "firstname":
        check = update_name(userid, data, user.lastname)
    if field == "lastname":
        check = update_name(userid, user.firstname, data)
    if field == "email":
        check = update_email(userid, data)

    if check:
        print(f'{field} updated successfully')
    else:
        print(f'{field} failed to update')

@user_cli.command("remove", help="Removes a user from the database")
@click.argument("userid", type=int)
def delete_user_command(userid):
    user = get_user(userid)
    if not user:
        print("User not found. Exiting...")
        return

    if not delete_user(user.id):
        print(f'User {user.id} failed to remove')
    else:
        print(f'User {user.id} removed successfully')

app.cli.add_command(user_cli)


'''
Student Commands
'''

student_cli = AppGroup('student', help= 'Student commands')

@student_cli.command("add", help='Adds a student')
@click.argument("student_id", type=int)
def add_student_command(student_id):
    student = create_student(student_id, system_id)
    if student:
        print(f'{student.student_id} has been added at id {student.id}!')
    else:
        print(f'Error creating student')

@student_cli.command("list", help='Lists all students')
@click.argument("format", default="string")
def list_students_command(format):
    if format == 'string':
        print(get_all_students())
    else:
        print(get_all_students_json())

@student_cli.command("reviews", help='Lists all reviews for a given student id')
@click.argument("student_id", type=int)
@click.argument("format", default="string")
def view_student_reviews_command(student_id, format):
    student = get_student_by_student_id(student_id)
    if not student:
        print("Student not found. Exiting...")
        return

    if format == 'string':
        reviews = get_student_reviews(student.id)
        if reviews:
          for review in reviews:
            staff = get_staff_by_id(review.staff_id)
            if staff:
              print(f'{review.details}, points: {review.points}, created by {staff.firstname} {staff.lastname} at {review.date_created}')
            else:
              print(f'{review.details}, points: {review.points}, created by unknown user {review.date_created}')
        else:
          print('No reviews found')
    else:
        reviews = get_student_reviews_json(student.id)
        if reviews:
            print(reviews)
        else:
            print('No reviews found')

@student_cli.command("details", help='Views student details from given student id')
@click.argument("student_id", type=int)
@click.argument("format", default="string")
def view_student_details_command(student_id, format):
    if format == 'string':
        student = get_student_by_student_id(student_id)
    else:
        student = get_student_by_student_id_json(student_id)
    if not student:
        print("Student not found. Exiting...")
        return
    print(student)

@student_cli.command("remove", help="Removes a student from the database")
@click.argument("student_id", type=int)
def delete_student_command(student_id):
    student = get_student_by_id(student_id)
    if not student:
        print("Student not found. Exiting...")
        return

    if not delete_student(student.student_id):
        print(f'Student {student.id} failed to remove')
    else:
        update_karma_ranking(system_id)
        print(f'Student {student.id} removed successfully')


app.cli.add_command(student_cli)

'''
Review Commands
'''

review_cli = AppGroup('review', help= 'Review commands')

@review_cli.command("add", help='Creates a review for a student by a staff')
@click.argument("student_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("points", type=int)
@click.argument("details")
def create_review_command(student_id, staff_id, points, details):
    if not points in [-3, -2, -1, 1, 2, 3]:
        print("Invalid points entered. Exiting...")
        return

    student = get_student_by_student_id(student_id)
    if student is None:
      print("Student has never been reviewed before")
      student = create_student(student_id, system_id)

    staff = get_staff_by_id(staff_id)
    if staff is None:
      print("Invalid user id")

    if student and staff:
      review = create_review(staff, student, points, details)
      if review:
          print(f'Review was created for {student.student_id} by {staff.firstname} {staff.lastname} at {review.date_created}')
      else:
          print(f'Student does not exist')

      update_karma(student.id)
      update_karma_ranking(system_id)
      print_karma_ranking(system_id)

@review_cli.command("list", help='Lists all reviews')
@click.argument("format", default="string")
def list_reviews_command(format):
    if format == 'string':
        print(get_all_reviews())
    else:
        print(get_all_reviews_json())

@review_cli.command("update", help='Updates given attribute of the review')
@click.argument("reviewid", type=int)
@click.argument("field", type=click.Choice(["staff", "student", "points", "details"]))
@click.argument("data")
def update_review_command(field, reviewid, data):
    check = False
    review = get_review(reviewid)

    if not review:
        print("Review not found. Exiting...")
        return

    if field == "staff":
        data = get_staff_by_id(data)
        if not data:
            print("Staff not found. Exiting...")
            return
        check = update_review_staff(reviewid, data)
    if field == "student":
        data = get_student_by_id(data)
        if not data:
            print("Student not found. Exiting...")
            return
        check = update_review_student(reviewid, data)
        update_karma_ranking(system_id)
    if field == "points":
        check = update_review_points(reviewid, data)
        update_karma_ranking(system_id)
    if field == "details":
        check = update_review_details(reviewid, data)

    if check:
        print(f'{field} updated successfully for review {reviewid}')
    else:
        print(f'{field} failed to update')

@review_cli.command("remove", help='Removes a review from the database')
@click.argument("reviewid", type=int)
def delete_review_command(reviewid):
    review = get_review(reviewid)
    if not review:
        print("Review not found. Exiting...")
        return

    if not delete_review(review.id):
        print(f'Review {review.id} failed to remove')
    else:
        update_karma_ranking(system_id)
        print(f'Review {review.id} removed successfully')

app.cli.add_command(review_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')

@test.command("final", help="Runs ALL tests")
def final_tests_command():
  sys.exit(pytest.main(["App/tests"]))

@test.command("user", help="Run User tests")
@click.argument("type", type=click.Choice(["all", "unit", "int"]), default="all")
def user_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "UserUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "test_user.py"]))

@test.command("admin", help="Run Admin tests")
@click.argument("type", type=click.Choice(["all", "unit", "int"]), default="all")
def user_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "AdminUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "test_admin.py"]))


@test.command("student", help="Run Student tests")
@click.argument("type", type=click.Choice(["all", "unit", "int"]), default="all")
def student_tests_command(type):
 if type == "unit":
   sys.exit(pytest.main(["-k", "StudentUnitTests"]))
 elif type == "int":
   sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
 else:
   sys.exit(pytest.main(["-k", "test_student.py"]))



@test.command("staff", help="Run Staff tests")
@click.argument("type", type=click.Choice(["all", "unit", "int"]), default="all")
def staff_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StaffUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "test_staff.py"]))


@test.command("review", help="Run Review tests")
@click.argument("type", type=click.Choice(["all", "unit", "int"]), default="all")
def review_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "test_review.py"]))

app.cli.add_command(test)
