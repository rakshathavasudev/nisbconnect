import mysql.connector

def connectDB(host='localhost',database='codejam',user='root',password='1234'):
    return mysql.connector.connect(host=host,database=database,user=user,password=password)

def disconnectDB(conn):
    conn.close()

def executeDB(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def queryDB(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall() # fetchone() , fetchmany() , fetchall()
    cursor.close()
    return rows

# Tables
# members
#     id	int(11) Auto Increment
#     username	text
#     password	text
#     email	text
#     bio	text
#     dob	date
#     ieee_no	int(11)
#     branch	text
#     sem	int(11)

# likes
    # user_id	int(11) Auto Increment
    # post_id	int(11)

# Post
    # user_id	int(11)	 
    # post_id	int(11) Auto Increment
    # post_title	text
    # article	mediumtext
    # date_time	timestamp [CURRENT_TIMESTAMP]


#USAGE
# c = connectDB()
# executeDB(c,"insert into memebers values(a,b,c)")
# disconnectDB(c)


# c = connectDB()
# result = queryDB(c,"select * from memebers")
# disconnectDB(c)
