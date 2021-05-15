from flask import Flask, render_template,request,redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)

@app.route("/")
def index():
    mysql = connectToMySQL('users')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users;')  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("index.html",users=users)

@app.route("/save",methods=["POST"])
def create():
    mysql = connectToMySQL('users')
    query = "INSERT INTO users (first_name, last_name, email) VALUES (%(fn)s,%(ln)s,%(email)s);"
    data = {
        "fn":request.form["first_name"],
        "ln":request.form["last_name"],
        "email":request.form["email"],

    }
    mysql.query_db(query,data)
    return redirect("/")

@app.route("/create")
def show():    
    return render_template("create.html") 

@app.route("/show/<id>")
def show_user_id(id):
    mysql = connectToMySQL('users')	        # call the function, passing in the name of our db
    query = 'SELECT * FROM users WHERE id = %(users_id)s;'  # call the query_db function, pass in the query as a string
    data = {
            "users_id":id
    } 
    user = mysql.query_db(query,data)
    
    return render_template("show.html",user=user[0])



@app.route("/edit/<id>")
def edit_user_id(id):
    mysql = connectToMySQL('users')
    query = 'SELECT * FROM users WHERE id = %(users_id)s;'  # call the query_db function, pass in the query as a string
    data = {
            "users_id":id
    } 
    user = mysql.query_db(query,data)
    
    return render_template("edit.html",user=user[0])
	
    
@app.route("/update/<id>",methods=["POST"])
def update(id):
    mysql = connectToMySQL('users')
    query = 'UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s WHERE id=%(id)s'
    data = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "id":id
    }
    mysql.query_db(query,data)
    return redirect("/")

@app.route("/delete/<id>")
def delete_user(id):
    mysql = connectToMySQL('users')
    query = 'DELETE FROM users WHERE id=%(id)s'
    data = {
        "id":id
    }
    mysql.query_db(query,data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)