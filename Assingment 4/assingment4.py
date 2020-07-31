import json
import sqlite3

dbname = "roster.sqlite"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.executescript('''
	DROP TABLE IF EXISTS User;
	DROP TABLE IF EXISTS Course;
	DROP TABLE IF EXISTS Member;
	CREATE TABLE User (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		name TEXT UNIQUE 
	);
	CREATE TABLE Course (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		title TEXT UNIQUE
	);
	CREATE TABLE Member (
		user_id INTEGER,
		course_id INTEGER,
		role INTEGER,
		PRIMARY KEY(user_id, course_id)
	)
''')

cur.execute("DELETE FROM User")
cur.execute("DELETE FROM Course")
cur.execute("DELETE FROM Member")

filename = "roster_data.json"
jsondata = open(filename)
data = json.load(jsondata)


for entry in data:
	user = entry[0]
	course = entry[1]
	instructor = entry[2]


	user_statement = """INSERT OR IGNORE INTO User(name) VALUES( ? )"""
	SQLparams = (user, )
	cur.execute(user_statement, SQLparams)

	course_statement = """INSERT OR IGNORE INTO Course(title) VALUES( ? )"""
	SQLparams = (course, )
	cur.execute(course_statement, SQLparams)


	courseID_statement = """SELECT id FROM Course WHERE title = ?"""
	SQLparams = (course, )
	cur.execute(courseID_statement, SQLparams)
	courseID = cur.fetchone()[0]

	userID_statement = """SELECT id FROM User WHERE name = ?"""
	SQLparams = (user, )
	cur.execute(userID_statement, SQLparams)
	userID = cur.fetchone()[0]

	member_statement = """INSERT INTO Member(user_id, course_id, role)
		VALUES(?, ?, ?)"""
	SQLparams = (userID, courseID, instructor)
	cur.execute(member_statement, SQLparams)

conn.commit()


test_statement = """
SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X
"""
cur.execute(test_statement)
result = cur.fetchone()
print("RESULT: " + str(result))


cur.close()
conn.close()