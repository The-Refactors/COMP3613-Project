# Flask Commands

This markdown file will serve to explain the usage of implemented flask commands. This is the general notation that will be used throughout:

    flask commandgroup commandname argument1 argument2 {choice} [option] [{default}]

commandgroup - There are four command groups in this implementation, User/Student/Review/Test. Not every command belongs to a group and thus not every command includes this block.

commandname - The names of commands typically try to follow a convention.

argumentx - These are the required data input into any given command. Not every command has these.

{choice} - this is a form of argument that can accept only specifically defined data as input

[option] - this is a form of argument that can be omitted from the inputted command to effect a different behaviour

[{default}] - this is a combination of choice and option where the argument can be omitted from the inputted command due to having a default choice. If included then it can accept only specifically defined data as input

# Group-less Commands

## Init

Initializes the database with test data

	flask init

## Karma

Lists the karma rankings of all students currently in the database. Optionally may return json format

	flask karma [format]

[format] - Any input aside from its default changes the format of output to json 

# Command Group - User

These commands are typically used to enact some behaviour on user-related objects within the database and will always be preceded with the following format

	flask user

## Create User

Creates a new user in the database with the specified attributes

	flask user add {type} username firtname lastname password email

{type} - Choices are ['admin' | 'staff']

## List Users

Lists users in the database of a type that is optionally chosen. Optionally may return json format

	flask user list [{type}] [format]

[{type}] - Choices are ['all' | 'admin' | 'staff'] and defaults to ['all']
[format] - Any input aside from its default changes the format of output to json


## Update User

Updates the user with specified userid's chosen field, with the given data

	flask user update userid {field} data

{field} - Choices are ['username' | 'password' | 'firstname' | 'lastname' | 'email']

## Remove User

Removes the user with specified userid from the database
	
	flask user remove userid


# Command Group - Student

These commands are typically used to enact some behaviour on student-related objects within the database and will always be preceded with the following format

	flask student

## Create Student

Creates a new student in the database with the specified student_id

	flask student add student_id


## List Students

Lists students in the database. Optionally may return json format

	flask student list [format]

[format] - Any input aside from its default changes the format of output to json


##  List Student Reviews

Lists the student with the specified student_id's reviews. Optionally may return as json format

	flask student reviews student_id [format]

[format] - Any input aside from its default changes the format of output to json


## View Student Details

Views the student with the specified student_id's details. optionally may return as json format

	flask student details student_id [format]

[format] - Any input aside from its default changes the format of output to json


## Remove Student

Removes the student with specified student_id from the database
	
	flask student remove student_id

# Command Group - Review

These commands are typically used to enact some behaviour on review-related objects within the database and will always be preceded with the following format

	flask review


## Create Review

Creates a new review in the database for the student with the specified student_id, by a staff user with the specified staff_id, the chosen points, as well as the given details. Creates a new student if they do not already exist.

	flask review add student_id staff_id {points} details

When entering a negative value for points, a double hyphen must be placed in a position prior, example

	flask review add -- student_id staff_id {points} details
	flask review add student_id staff_id -- {points} details

{points} - Choices are [-3 | -2 | -1 | 1 | 2 | 3]

## List Reviews

Lists reviews in the database. Optionally may return json format

	flask review list [format]

[format] - Any input aside from its default changes the format of output to json


## Update Review

Updates the review with specified reviewid's chosen field, with the given data

	flask review update reviewid {field} data

{field} - Choices are ['staff' | 'student' | 'points' | 'details']. The student choice accepts the database id of a student and thus the command only accepts students that are already in the database


## Remove Review

Removes the reeview with specified reviewid from the database
	
	flask review remove reviewid

# Command Group - Test

These commands are used to perform tests on the database and its stored data and will always be preceded with the following format

	flask test


## All Tests

Runs all tests in sequence

	flask test final


## User Tests

Runs user-related tests of the optionally chosen type in sequence

	flask test user [{type}]

[{type}] - Choices are ['all' | 'unit' | 'int'] and defaults to ['all']


## Admin Tests


Runs admin-related tests of the optionally chosen type in sequence

	flask test admin[{type}]

[{type}] - Choices are ['all' | 'unit' | 'int'] and defaults to ['all']


## Staff Tests

Runs staff-related tests of the optionally chosen type in sequence

	flask test staff [{type}]

[{type}] - Choices are ['all' | 'unit' | 'int'] and defaults to ['all']


## Student Tests

Runs student-related tests of the optionally chosen type in sequence

	flask test student [{type}]

[{type}] - Choices are ['all' | 'unit' | 'int'] and defaults to ['all']


## Review Tests

Runs review-related tests of the optionally chosen type in sequence

	flask test review [{type}]

[{type}] - Choices are ['all' | 'unit' | 'int'] and defaults to ['all']
