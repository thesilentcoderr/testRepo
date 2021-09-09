from os import name
from flask import Flask,request,Response,json,render_template,flash,redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

with open('vars.json','r') as v:
    variable = json.load(v)
    
db_keeps = variable["sql_conf"]


mysql = MySQL(app)
# MySQL Configuration
app.config['MYSQL_HOST'] = db_keeps["mysql_host"]
app.config['MYSQL_USER'] = db_keeps["mysql_user"]
app.config['MYSQL_PASSWORD'] = db_keeps["mysql_password"]
app.config['MYSQL_DB'] = db_keeps["mysql_db"]
app.config['MYSQL_PORT'] = db_keeps['mysql_port']

@app.route("/",methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form = request.form
        phone = form['phone']
        cur = mysql.connection.cursor()
        users = cur.execute("SELECT * FROM user WHERE phone=%s;", ([phone]))
        if users != ():
            user = cur.fetchone()
            user_id = user[0]
        else:
            cur.close()
            return redirect('/')
        cur.close()
        return redirect('/cards/{}'.format(user_id))
    return render_template("index.html")

@app.route("/profile/<id>",methods=['GET', 'POST'])
def profile(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE id=%s;", ([id]))
    profiles = cur.fetchall()
    return render_template('profile.html',profiles = profiles)

@app.route("/cards/<id>",methods=['GET', 'POST'])
def cards(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user;")
    cards = cur.fetchall()
    return render_template('card.html',cards = cards)


if __name__ == "__main__":
    app.run(debug=True)