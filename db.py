import mysql.connector
from werkzeug.security import check_password_hash

cnx=mysql.connector.connect(user='root', password='root',
                                        host='127.0.0.1',
                                        database='BLOG')



def check_email(email_id):
    result=False
    my_cursor=cnx.cursor()
    sqlquery = "select * from blog.users where email_id = %s"
    my_cursor.execute(sqlquery, (f"{email_id}",))
    if my_cursor.fetchall():  # or cursor.fetchone() if you expect only one row
        result = True
        print("result is",result)
    else:
        result = False
    return result

def user_insert(first_name,last_name,email_id,password):
    my_cursor=cnx.cursor()
    query = "insert into blog.users (first_name, last_name, email_id,password) values(%s,%s,%s,%s)"
    data = (first_name,last_name,email_id,password)
    my_cursor.execute(query, data)
    cnx.commit()


def get_all_users():
    users={}
    my_cursor=cnx.cursor()
    query = "SELECT user_id,first_name,last_name,email_id from blog.users"    
    my_cursor.execute(query)
    for id, first_name, last_name, email_id in my_cursor.fetchall():
        users[str(id)] = {
            "first_name": first_name,
            "last_name": last_name,
            "email_id": email_id
        }
  #  print(users)
    return users
    

def check_password(email_id,password1):
    correct_password=False
    my_cursor=cnx.cursor()
    query = "SELECT * FROM blog.users WHERE email_id = %s"
    my_cursor.execute(query,(email_id,))
    user_id,first_name,last_name,email_id,password_in_db=my_cursor.fetchone()
    print(user_id," ",first_name," ",last_name," ",email_id," ",password_in_db)
    
    print(password_in_db)
    if check_password_hash(pwhash=password_in_db,password=password1):
        correct_password=True
        print(correct_password)
    else:
        print(correct_password)
        correct_password=False            
    return correct_password,user_id,first_name,last_name,email_id

def getlastpost():
    my_cursor=cnx.cursor()
    query = "SELECT MAX(post_id) from blog.posts"    
    my_cursor.execute(query)
    maxvalue=my_cursor.fetchone()
    print(maxvalue)
    if maxvalue[0] is None:
        sendpostnumber=0
    else:
        sendpostnumber=int(maxvalue[0])
    return sendpostnumber

def add_post_to_db(user_id,post_id,post_title,post_content,date_added):
    my_cursor=cnx.cursor()
    query = "insert into blog.posts (user_id,post_id,post_title,post_content,date_added) values(%s,%s,%s,%s,%s)"
    data = (user_id,post_id,post_title,post_content,date_added)
    my_cursor.execute(query, data)
    cnx.commit()

def get_all_user_posts(user_id):
    user_specific_posts={}
    my_cursor=cnx.cursor()
    sqlquery = "select * from blog.posts where user_id=%s"
    my_cursor.execute(sqlquery, (user_id,))
    for user_id, post_id,post_title,post_content,date_added in my_cursor.fetchall():
        user_specific_posts[str(post_id)] = {
            "post_title":post_title,
            "post_content":post_content,
            "date_added":date_added
        }

    
    
    return user_specific_posts


if __name__=="__main__":
    check_password("eluriabhinav@gmail.com","Abhinav@95")
 #   print(getlastpost())