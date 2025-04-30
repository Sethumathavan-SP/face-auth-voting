import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="voterlist"
)
ID = "ABC1234567"
cur = con.cursor()

def mark_notVoted(ID):
    cur.execute("update voters set voted = 0 where VoterId = %s;",(ID,))
    con.commit()
def mark_voted(ID):
    cur.execute("update voters set voted = 1 where VoterId = %s;",(ID,))
    con.commit()
def write_data(ID,img_loc,voted = 0):
    with open(img_loc,'rb') as fh:
        img_blob = fh.read()
    cur.execute("insert into voters (VoterID, VoterImage, Voted) values (%s,%s,%s)",(ID,img_blob,voted))
    con.commit()
def find_data(ID):
    cur.execute(f"select * from voters where VoterID = '{ID}';")
    data = cur.fetchall()
    if len(data) == 0:
        return -1
    elif data[0][2] == 1:
        return -2
    else:
        return data[0][1]
def vote_candidate(indx):
    print(indx)
    l = ['party1','party2','party3','party4','party5']
    name = l[indx]
    co = mysql.connector.connect(
        host = 'localhost',
        database = 'candidatelist',
        password = '1234',
        user = 'root'
    )
    cr = co.cursor()
    cr.execute("update candidates set votes = votes+1 where name = %s;",(name,))
    co.commit()
    co.close()