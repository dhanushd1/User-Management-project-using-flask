from flask import Flask, render_template ,url_for,redirect,request,flash
from flask_mysqldb import MySQL
app = Flask(__name__)
#mysql connection
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="dhanushds"
app.config["MYSQL_DB"]="crud"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)
#loading home page
@app.route("/")
def home():
    con=mysql.connection.cursor()
    sql="select * from users"
    con.execute(sql)
    res=con.fetchall()
    
    return render_template("home.html",datas=res)
#new user
@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        city=request.form['city']
        con=mysql.connection.cursor()
        sql="insert into users(Name,Age,City) value (%s,%s,%s)"
        con.execute(sql,[name,age,city])
        mysql.connection.commit()
        con.close()
        flash('USER DETAILS ADDED')
        return redirect(url_for("home"))

    return render_template("addUsers.html")
#update users
@app.route("/editUsers/<int:id>", methods=['GET','POST'])
def editUser(id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        sql = "UPDATE users SET Name=%s, Age=%s, City=%s WHERE ID=%s"
        con.execute(sql, [name, age, city, id])
        mysql.connection.commit()
        con.close()
        flash('USER DETAILS UPDATED')
        return redirect(url_for("home"))
    else:
        sql = "SELECT * FROM users WHERE ID=%s"
        con.execute(sql, [id])
        res = con.fetchone()
        con.close()
        return render_template("editUser.html", datas=res)
@app.route("/deleteUsers/<int:id>", methods=['GET'])
#delete users
def deleteUser(id):
    con = mysql.connection.cursor()
    sql=f"delete from users where ID='{id}'"
    con.execute(sql)
    mysql.connection.commit()
    con.close()
    flash('USER DETAILS DELETED')
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.secret_key="abc123"
    app.run(debug=True)

