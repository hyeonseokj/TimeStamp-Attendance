from flask import Flask, render_template, request, url_for, redirect, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)
app.secret_key = "ABCD"

client = MongoClient('localhost', 27017)  #ip 주소,...

db_2 = client.flask_manager
manager =db_2.manager

db = client.flask_user
user = db.user


@app.route('/', methods=('GET', 'POST'))
def index():
    if session.get('logged_in') :
        return render_template('loggedin.html')
    else:
        return render_template('index.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        all_user = list(user.find())
        existing_user = user.find_one({"email":email})


        if existing_user:
            flash("Email already exists")
            return render_template('signup.html')

        else:
            user.insert_one({'name' : name,'email': email, 'password': password})
            flash("회원가입 성공")
            return redirect(url_for('signup'))

        # try:
        #     if {'email':email} in all_user:
        #         flash("이미 존재하는 이메일입니다.")     
        # except: 
        #     user.insert_one({'name' : name,'email': email, 'password': password})
        # return redirect(url_for('index'))

    return render_template('signup.html')



@app.route('/login//dailylogin/', methods=['GET', 'POST'])
def daily_login():
    daily_user = manager.find_one({})


    return render_template("daily_login.html", daily_user = daily_user)

@app.route('/login/userlogin/', methods=['GET', 'POST'])
def user_login():
    #all_managers = list(manager.find())

    return render_template("user_login.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return render_template('index.html')





@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_user = user.find_one({"email":email})
        #print(login_user)
        if login_user["email"] == 'manager' and login_user['password'] == password:
            flash("관리자 페이지")
            return render_template("manager.html")

        elif login_user and login_user["password"] == password:
            login_time = str(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M %p"))
            update = {"$push": {"login times": login_time}}
            query = {"email": email,"password": password}
            user.update_one(query, update)

            # user_name = login_user['name']
            # time_key = str(datetime.datetime.now().strftime(" %Y %B %d"))
            # simple_login_time = str(datetime.datetime.now().strftime("%I:%M %p"))
            # update_2 = {"$push": {time_key: {user_name: simple_login_time}}}
            # query_2 = {"email": email}
            # manager.update_one(query_2, update_2)
            

            time_key = str(datetime.datetime.now().strftime("%Y %B %d"))
            simple_login_time = str(datetime.datetime.now().strftime("%I:%M %p"))
            update_2 = {"$push": {time_key: {login_user['name']: simple_login_time}}}
            query_2 = {"email": "manager"}
            try:
                manager.update_one(query_2, update_2)
            except Exception as e:
                print('Error updating manager collection', str(e))

            print(list(manager.find()))

            login_times = login_user.get("login times", [])
            return render_template("logged.html", name=login_user["name"], login_time=login_time, login_times=login_times)
        

        else:
            flash("로그인 실패")
            return render_template("login.html")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4500)                                                                                                                                                       




# @app.route("/login/daily_login", methods=['GET', 'post'])
# def manager_daily():

#     return render_template('daily_login.html')

# @app.route("/login/user_login", methods=['GET', 'POST'])
# def manager_user():
#     return render_template('user_login.html')
