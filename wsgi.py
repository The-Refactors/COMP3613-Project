import click, pytest, sys
import nltk
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.models import User, Admin, Staff, KarmaObserver, Student, Review
from App.controllers import (
    create_student, create_staff, create_admin, create_review, get_student_by_id, get_student_by_student_id, get_staff_by_id,
    get_student_reviews, get_all_students, get_all_users, get_all_users_json, get_all_admins, get_all_admins_json,
    get_all_staff, get_all_staff_json, get_all_reviews, create_karma_system, update_karma)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  
  create_admin("bobby", "Bob", "Harris", "bobpass", "bob@mail.com")
  create_admin("lyss", "Alyssa", "Smith", "lysspass", "alyssa@mail.com")

  create_staff("henry", "Henry", "John", "henrypass", "henry@mail.com")
  create_staff("mike", "Michael", "Williams", "mikepass", "mike@mail.com")
  create_staff("cattie", "Catherine", "Singh", "cattiepass", "cattie@mail.com")

  create_student(student_id='816011111')
  create_student(student_id='816022222')
  create_student(student_id='816033333')
  create_student(student_id='816044444')
  create_student(student_id='816055555')

  print("Created Students")

  students = Student.query.all()

  for student in students:
    
    if student:
      print(student.id)

  create_karma_system()



'''
Admin Commands
'''
user_cli = AppGroup('user', help= 'Admin Commands')

@user_cli.command("addAdmin", help="Add an admin")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("firstname")
@click.argument("lastname")
@click.argument("email")
def create_admin_command(username, firstname, lastname, password, email):
    admin = create_admin(username, firstname, lastname, password, email)
    if admin:  
      print(f'{username} created!')


@user_cli.command("addStaff", help="Add a member of staff")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("firstname")
@click.argument("lastname")
@click.argument("email")
def create_user_command(username, firstname, lastname, password, email):
    user = create_staff(username, firstname, lastname, password, email)
    if user:
      print(f'{username} created!')


@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())


@user_cli.command("listAdmin", help="Lists admins in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_admins())
    else:
        print(get_all_admins_json())

@user_cli.command("listStaff", help="Lists staff members in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_staff())
    else:
        print(get_all_staff_json())


app.cli.add_command(user_cli)


'''
Student Commands
'''

student_cli = AppGroup('student', help= 'Student commands')

@student_cli.command("add", help='Add a student')
@click.argument("student_id")
def add_student_command(student_id):
    student = create_student(student_id)
    if student:
        print(f'{student.studentid} has been added at id {student.id}!')
    else:
        print(f'Error creating student')

@student_cli.command("list", help='Lists all students')
def list_students_command():
    students = get_all_students()

    for student in students:

      print(f'Student {student.id} - {student.student_id}')

@student_cli.command("search", help='Search for a student')
@click.argument("student_id")
def search_student_command(student_id):
    student = get_student_by_student_id(student_id)
    if student:
        print(student.get_json())
    else:
        print(f'Student does not exist')

@student_cli.command("review", help='Review a student')
@click.argument("student_id")
@click.argument("user_id")
@click.argument("points")
@click.argument("details")
def review_student_command(student_id, user_id, points, details):
    student = get_student_by_student_id(student_id)
    if student is None:
      print("Student has never been reviewed before")
      create_student(student_id)
      student = get_student_by_student_id(student_id)

    staff = get_staff_by_id(user_id)
    if staff is None:
      print("Invalid user id")
    if student and staff:

      review = create_review(staff, student, points, details)
      # update_karma(student_id)

      if review:
          print(f'Review was created for {student.student_id} by {staff.firstname} {staff.lastname} at {review.date_created}')
      else:
          print(f'Student does not exist')


@student_cli.command("viewReviews", help='View student reviews')
@click.argument("student_id")
def view_student_reviews_command(student_id):
    student = get_student_by_student_id(student_id)
    reviews = get_student_reviews(student.id)
    if reviews:
      for review in reviews:
        staff = get_staff_by_id(review.staffid)
        if staff: 
          print(f'{review.details}, points: {review.points}, created by {staff.firstname} {staff.lastname} at {review.datecreated}')
        else:
          print(f'{review.details}, points: {review.points}, created by unknown user {review.datecreated}')

    else:
      print(f'No reviews found')

@student_cli.command("details", help='View student details')
@click.argument("student_id")
def view_student_details_command(student_id):
    student = get_student_by_student_id(student_id)
    
    print(f'Student ID:\t{student.student_id}')
    print(f'Karma Score:\t{student.karma}')
    print(f'Karma Rank:\t{student.karma_rank}')

app.cli.add_command(student_cli)

'''
Review Commands
'''

review_cli = AppGroup('review', help= 'Review commands')

@review_cli.command("list", help='Lists all reviews')
def list_reviews_command():
    reviews = get_all_reviews()

    for review in reviews:

      staff = get_staff_by_id(review.staffid)
      student = get_student_by_id(review.studentid)

      print(f'Review {review.id} - {student.studentid}, {review.details}, points: {review.points}, created by {staff.firstname} {staff.lastname} at {review.datecreated}')

app.cli.add_command(review_cli)

# @app.cli.command("nltk_test", help="Tests nltk")
# @click.argument("sentence", default="all")
# def analyze(sentence):
#   analyze_sentiment(sentence)
#   return


# # '''
# # User Commands
# # '''

# # # Commands can be organized using groups

# # # create a group, it would be the first argument of the comand
# # # eg : flask user <command>
# # # user_cli = AppGroup('user', help='User object commands')

# # # # Then define the command and any parameters and annotate it with the group (@)
# # @user_cli.command("create", help="Creates a user")
# # @click.argument("username", default="rob")
# # @click.argument("password", default="robpass")
# # def create_user_command(id, username, firstname,lastname , password, email, faculty):
# #     create_user(id, username, firstname,lastname , password, email, faculty)
# #     print(f'{username} created!')

# # # this command will be : flask user create bob bobpass

# # @user_cli.command("list", help="Lists users in the database")
# # @click.argument("format", default="string")
# # def list_user_command(format):
# #     if format == 'string':
# #         print(get_all_users())
# #     else:
# #         print(get_all_users_json())

# # app.cli.add_command(user_cli) # add the group to the cli
# '''
# Test Commands
# '''

#test = AppGroup('test', help='Testing commands')

# @test.command("final", help="Runs ALL tests")
# @click.argument("type", default="all")
# def final_tests_command(type):
#   if type == "all":
#     sys.exit(pytest.main(["App/tests"]))

# @test.command("user", help="Run User tests")
# @click.argument("type", default="all")
# def user_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "UserUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


#@test.command("student", help="Run Student tests")
#@click.argument("type", default="all")
#def student_tests_command(type):
#  if type == "unit":
#    sys.exit(pytest.main(["-k", "StudentUnitTests"]))
#  elif type == "int":
#    sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
#  else:
#    sys.exit(pytest.main(["-k", "App"]))



# @test.command("staff", help="Run Staff tests")
# @click.argument("type", default="all")
# def staff_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "StaffUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("review", help="Run Review tests")
# @click.argument("type", default="all")
# def review_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("recommendation", help="Run Recommendation tests")
# @click.argument("type", default="all")
# def recommendation_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "RecommendationUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "RecommendationIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("karma", help="Run Karma tests")
# @click.argument("type", default="all")
# def karma_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
#   # else:
#   #   sys.exit(pytest.main(["-k", "App"]))


# @test.command("incidentreport", help="Run Incident Report tests")
# @click.argument("type", default="all")
# def incident_reports_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "IncidentReportUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "IncidentReportIntegrationTests"]))
#   # else:
#   #     sys.exit(pytest.main(["-k", "App"]))


# @test.command("accomplishment", help="Run Accomplishment tests")
# @click.argument("type", default="all")
# def accomplishment_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "AccomplishmentUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "AccomplishmentIntegrationTests"]))
#   # else:
#   #     sys.exit(pytest.main(["-k", "App"]))


# @test.command("grades", help="Run Grades tests")
# @click.argument("type", default="all")
# def grades_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "GradesUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "GradesIntegrationTests"]))
#   # else:
#   #     sys.exit(pytest.main(["-k", "App"]))


# @test.command("admin", help="Run Admin tests")
# @click.argument("type", default="all")
# def admin_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "AdminUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
#   # else:
#   #     sys.exit(pytest.main(["-k", "App"]))


# @test.command("nltk", help="Run NLTK tests")
# @click.argument("type", default="all")
# def nltk_tests_command(type):
#   if type == "unit":
#     sys.exit(pytest.main(["-k", "NLTKUnitTests"]))
#   elif type == "int":
#     sys.exit(pytest.main(["-k", "NLTKIntegrationTests"]))


# @test.command("print", help="print get_transcript")
# @click.argument("type", default="all")
# def print_transcript(type):
#   studentid = input("Enter student id: ")  # Prompt user to enter student id
#   transcripts = get_transcript(
#       studentid)  # Get transcript data for the student
#   if transcripts:
#     for transcript in transcripts:
#       if type == "all":
#         print(transcript.to_json())  # Print all transcript data as JSON
#       # elif type == "id":
#       #     print(transcript.studentid)  # Print student id
#       # elif type == "gpa":
#       #     print(transcript.gpa)  # Print GPA
#       # elif type == "fullname":
#       #     print(transcript.fullname)  # Print full name
#       # Add more options as needed
#       else:
#         print(
#             "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
#         )
#   else:
#     print("Transcript not found for student with id:", studentid)


# @test.command("printstu", help="print get_student")
# @click.argument("type", default="all")
# def print_student(type):
#   UniId = input("Enter student id: ")
#   student = get_student_by_UniId(UniId)
#   if student:
#     if type == "all":
#       print(student.to_json(0))
#     # elif type == "id":
#     #     print(student.UniId)
#     # elif type == "gpa":
#     #     print(student.gpa)
#     # elif type == "fullname":
#     #     print(student.fullname)
#     else:
#       print(
#           "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
#       )
#   else:
#     print("Student not found with id:", UniId)


# @test.command("printgradepointsandgpa_weight",
#               help="print student grade points from transcript")
# @click.argument("type", default="all")
# def print_grade_points(type):
#   UniId = input("Enter student id: ")
#   points = get_total_As(UniId)
#   cources_attempted = get_total_courses_attempted(UniId)
#   if points:
#     print('points ', points)
#     print('courses attepmtped:, ', cources_attempted)

#   else:
#     print("Student not found with id:", UniId)


# @test.command("printacademicscore", help="print student academic weight")
# @click.argument("type", default="all")
# def print_academic_weight(type):
#   UniId = input("Enter student id: ")
#   points = get_total_As(UniId)
#   cources_attempted = get_total_courses_attempted(UniId)
#   academic_score = calculate_academic_score(UniId)
#   if points:
#     print('points ', points)
#     print('courses attepmtped:, ', cources_attempted)
#     print('Academic Score:, ', academic_score)

#   else:
#     print("Student not found with id:", UniId)


#app.cli.add_command(test)
