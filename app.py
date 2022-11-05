from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ambra11erla'
app.config['MYSQL_DB'] = 'register'

mysql = MySQL(app)

SPORTS = [
    "Basketball",
    "Football",
    "Tenis",
    "Bilardo"
]


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/registrim", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name:
        return render_template("error.html", message="Missing Name")
    # validate sport
    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html", message="Missing Sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid Sport")

    name = request.form["name"]
    sport = request.form["sport"]
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(name, sport) VALUES (%s, %s)", (name, sport))
    mysql.connection.commit()

    # Confirm Register

    return redirect(url_for("registrim"))


@app.route("/registrim", methods=["GET"])
def registrim():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users ORDER BY name asc")
    registrim = cur.fetchall()
    return render_template("registrim.html", registrim=registrim)


@app.route("/registrim/<users_id>", methods=["Post"])
def deleteone(users_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE ID=%s", (users_id,))
    mysql.connection.commit()

    return redirect(url_for("delete"))

@app.route("/delete")
def delete():
    return render_template("delete.html")


app.run(debug=True)
