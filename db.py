import mysql.connector
from flask_bcrypt import generate_password_hash, check_password_hash
def connectDB(host='localhost',database='codejam',user='root',password='1234'):
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


# User Functions

def user_register(username,password,email,bio,dob,ieee_no,branch,sem):
    c = connectDB()
    password = generate_password_hash(password)
    executeDB(c,"insert into members values(0,%s,%s,%s,%s,%s,%s,%s,%s)",(username,password,email,bio,dob,ieee_no,branch,sem))
    disconnectDB(c)
    return True

def user_update(username,email,bio,dob,ieee_no,branch,sem):
    c = connectDB()
    executeDB(c,"update members set \
                username=%s, \
                email=%s, \
                bio=%s, \
                dob=%s, \
                ieee_no=%s, \
                branch=%s, \
                sem=%s \
                where email=%s",(username,email,bio,dob,ieee_no,branch,sem,email))
    disconnectDB(c)
    return True

def user_unregister(user_id):
    c = connectDB()
    executeDB(c,"delete from members where user_id="+str(user_id),())
    disconnectDB(c)
    flush_posts(user_id)
    flush_follow(user_id)
    flush_user_likes(user_id)
    return True

def user_login(email,password):
    c = connectDB()
    result = queryDB(c,"select * from members where email='"+email+"'")
    disconnectDB(c)
    if check_password_hash(result[0][2], password):
        return result[0]
    else:
        return False

def member_info(user_id):
    c = connectDB()
    result = queryDB(c,"select * from members where user_id="+str(user_id))
    disconnectDB(c)
    return result[0]

def members_list():
    c = connectDB()
    result = queryDB(c,"select user_id,username,email,branch,sem from members")
    disconnectDB(c)
    return result



# Like Unlike lists

def like_post(user_id,post_id):
    c = connectDB()
    executeDB(c,"insert into likes values("+str(user_id)+","+str(post_id)+")",())
    disconnectDB(c)
    return True

def unlike_post(user_id,post_id):
    c = connectDB()
    executeDB(c,"delete from likes where user_id="+str(user_id)+" and post_id="+str(post_id),())
    disconnectDB(c)
    return True

def is_liked(user_id,post_id):
    c = connectDB()
    result = queryDB(c,"select * from likes where user_id="+str(user_id)+" and post_id="+str(post_id))
    disconnectDB(c)
    return len(result)

def get_likes(post_id):
    c = connectDB()
    result = queryDB(c,"select count(*) from likes where post_id="+str(post_id))
    disconnectDB(c)
    return result[0][0]





# Follow unfollow and lists

def is_following(from_id,to_id):
    c = connectDB()
    result = queryDB(c,"select * from follow where from_id="+str(from_id)+" and to_id="+str(to_id))
    disconnectDB(c)
    return len(result)

def follow(from_id,to_id):
    c = connectDB()
    executeDB(c,"insert into follow values("+str(from_id)+","+str(to_id)+")",())
    disconnectDB(c)
    return True

def unfollow(from_id,to_id):
    c = connectDB()
    executeDB(c,"delete from follow where from_id="+str(from_id) + " and to_id="+str(to_id),())
    disconnectDB(c)
    return True

def follower_list(user_id):
    c = connectDB()
    result = queryDB(c,"select user_id,username,email,branch,sem from members where user_id in (select from_id from follow where to_id="+str(user_id)+")")
    disconnectDB(c)
    return result

def following_list(user_id):
    c = connectDB()
    result = queryDB(c,"select user_id,username,email,branch,sem from members where user_id in (select to_id from follow where from_id="+str(user_id)+")")
    disconnectDB(c)
    return result



# Posts info and single post

def add_post(user_id,post_data,group):
    c = connectDB()
    executeDB(c,"insert into posts values("+user_id+","+group+",0,%s,now())",(post_data,))
    disconnectDB(c)
    return True

def remove_post(post_id):
    c = connectDB()
    executeDB(c,"delete from posts where post_id="+post_id,())
    flush_likes(post_id)
    disconnectDB(c)
    return True

def edit_post(article, post_id):
    c = connectDB()
    executeDB(c,"update posts set article=%s where post_id="+post_id,(article,))
    disconnectDB(c)
    return True

def get_post(post_id):
    c = connectDB()
    result = queryDB(c,"select post_id, posts.user_id,username,article,date_time from posts,members where wgroup=0 and post_id="+post_id+" and posts.user_id=members.user_id order by date_time desc")
    disconnectDB(c)
    return result

def post_list():
    c = connectDB()
    result = queryDB(c,"select post_id, posts.user_id,username,article,date_time from posts,members where wgroup=0 and posts.user_id=members.user_id order by date_time desc")
    disconnectDB(c)
    return result

def post_list_follow(user_id):
    c = connectDB()
    result = queryDB(c,"select post_id, posts.user_id,username,article,date_time from posts,members where  wgroup=0 and posts.user_id=members.user_id and posts.user_id in (select to_id from follow where from_id="+user_id+") order by date_time desc")
    disconnectDB(c)
    return result

def post_list_user(user_id):
    c = connectDB()
    result = queryDB(c,"select post_id, posts.user_id,username,article,date_time from posts,members where  wgroup=0 and posts.user_id=members.user_id and posts.user_id="+user_id);
    disconnectDB(c)
    return result

def group_post_list(group):
    c = connectDB()
    result = queryDB(c,"select post_id, posts.user_id,username,article,date_time from posts,members where posts.user_id=members.user_id and wgroup="+group)
    disconnectDB(c)
    return result


# messaging

def send_message(from_id,to_id,message):
    c = connectDB()
    executeDB(c,"insert into messages values(0,%s,%s,%s,now())",(from_id,to_id,message))
    disconnectDB(c)
    return True

def get_messages(from_id,to_id):
    c = connectDB()
    result = queryDB(c,"select user_id,username,message_data,date_time from messages,members where members.user_id=messages.from_id and ((messages.from_id=%s and messages.to_id=%s) or (messages.from_id=%s and messages.to_id=%s))"%(from_id,to_id,to_id,from_id))
    print result
    disconnectDB(c)
    return result

def clear_messages(from_id,to_id):
    c = connectDB()
    executeDB(c,"delete from messages where (from_id=%s and to_id=%s) or (from_id=%s and to_id=%s)",(from_id,to_id,to_id,from_id))
    disconnectDB(c)
    return True

# Cleanup Tasks

def flush_likes(post_id):
    c = connectDB()
    executeDB(c,"delete from likes where post_id="+str(post_id),())
    disconnectDB(c)
    return True

def flush_posts(user_id):
    c = connectDB()
    executeDB(c,"delete from posts where user_id="+str(user_id),())
    disconnectDB(c)
    return True

def flush_follow(user_id):
    c = connectDB()
    executeDB(c,"delete from follow where from_id="+str(user_id)+" or to_id="+str(user_id),())
    disconnectDB(c)
    return True

def flush_user_likes(user_id):
    c = connectDB()
    executeDB(c,"delete from likes where user_id="+str(user_id),())
    disconnectDB(c)
    return True

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
