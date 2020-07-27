import sqlite3

conn = sqlite3.connect('emaildb.sqlite') #connect/create sql db with the name
cur = conn.cursor() 

cur.execute('DROP TABLE IF EXISTS Counts') #ignores if exists the table already exists

cur.execute('''
CREATE TABLE Counts (email TEXT, count INTEGER)''')  #creates table counts with email(text) and count(int)

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,)) # ? = place holder will be replaced by(email,)
    row = cur.fetchone() #select one
    if row is None: #if there are no records do
        cur.execute('''INSERT INTO Counts (email, count)
                VALUES (?, 1)''', (email,)) #create row with email and count = 1
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',
                    (email,)) #if the email is appearing again, update the count value with +1
    conn.commit() #commit results to db / writes on disk 

sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10' #gets the top 10 counts(limit 10) from Counts table, and retrieves email and count to print

for row in cur.execute(sqlstr): #executes the command on sqlstr
    print(str(row[0]), row[1]) #prints the first and second row of the db

cur.close() #closes connection w/ db
