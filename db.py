import mysql.connector
from flask_bcrypt import generate_password_hash, check_password_hash
def connectDB(host='192.168.0.100',database='codejam',user='root',password='1234'):
    return mysql.connector.connect(host=host,database=database,user=user,password=password)

def disconnectDB(conn):
    conn.close()

def executeDB(conn,sql,values):
    cursor = conn.cursor()
    cursor.execute(sql,values)
    conn.commit()

def queryDB(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall() # fetchone() , fetchmany() , fetchall()
    cursor.close()
    return rows


def user_register(username,password,email,bio,dob,ieee_no,branch,sem):
    c = connectDB()
    password = generate_password_hash(password)
    executeDB(c,"insert into members values(0,%s,%s,%s,%s,%s,%s,%s,%s)",(username,password,email,bio,dob,ieee_no,branch,sem))
    disconnectDB(c)
    return True

def user_login(email,password):
    c = connectDB()
    result = queryDB(c,"select * from members where email='"+email+"'")
    disconnectDB(c)
    if check_password_hash(result[0][2], password):
        return result[0]
    else:
        return False
# Tests
# user_register("mridulganga","mridul1698","mridul.kepler@gmail.com","i am pro","1998-01-16","94082800","ise","6")
# user_login("mridul.kepler@gmail.com","i")

def like_post(user_id,post_id):
    c = connectDB()
    executeDB(c,"insert into likes values("+user_id+","+post_id+")",())
    disconnectDB(c)
    return True

# like_post('1','2')

def unlike_post(user_id,post_id):
    c = connectDB()
    executeDB(c,"delete from likes where user_id="+user_id+" and post_id="+post_id,())
    disconnectDB(c)
    return True

# unlike_post('1','2')

def add_post(user_id,post_data,group):
    c = connectDB()
    executeDB(c,"insert into posts values("+user_id+","+group+",0,%s,now())",(post_data,))
    disconnectDB(c)
    return True

# add_post('1','hello','0')

def remove_post(post_id):
    c = connectDB()
    executeDB(c,"delete from posts where post_id="+post_id,())
    disconnectDB(c)
    return True

# remove_post('1')

def edit_post(article, post_id):
    c = connectDB()
    executeDB(c,"update posts set article='"+article+"' where post_id="+post_id,())
    disconnectDB(c)
    return True

# edit_post('Hello!!!!!', '2')
def follow(from_id,to_id):
    c = connectDB()
    executeDB(c,"insert into follow values("+from_id+","+to_id+")",())
    disconnectDB(c)
    return True

# follow('1','2')
# follow('3', '2')
# follow('4', '2')

def unfollow(from_id,to_id):
    c = connectDB()
    executeDB(c,"delete from follow where from_id="+from_id + " and to_id="+to_id,())
    disconnectDB(c)
    return True

# unfollow('1','2')
# unfollow('3', '2')
# unfollow('4', '2')

def post_list():
    c = connectDB()
    result = queryDB(c,"select * from posts where group=0")
    disconnectDB(c)
    return result


def group_post_list(group):
    c = connectDB()
    result = queryDB(c,"select * from posts where group="+group)
    disconnectDB(c)
    return result

# print post_list()

def follower_list(user_id):
    c = connectDB()
    result = queryDB(c,"select username from members where id in (select from_id from follow where to_id="+user_id+")")
    disconnectDB(c)
    return result

def member_info(user_id):
    c = connectDB()
    result = queryDB(c,"select * from members where id="+user_id)
    disconnectDB(c)
    return result

def members_list():
    c = connectDB()
    result = queryDB(c,"select user_id,username,email,branch,sem from members")
    disconnectDB(c)
    return result

#print members_list()

# print follower_list('2')

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
