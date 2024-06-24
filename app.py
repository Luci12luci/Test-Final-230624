from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Pripojenie k databáze
conn = psycopg2.connect(
    dbname='b1mxnbtfaytwhs4af34m',
    user='uwj8p4v8zuoeyv3iqlxg',
    password='Kh3N5D3JtxcCyJeXuUeeZVNCROL6Jo',
    host="b1mxnbtfaytwhs4af34m-postgresql.services.clever-cloud.com",
    port=50013
)

users = {
    'john': 'password123',
    'jane': 'mypassword'
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('welcome', username=username))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

@app.route("/")
def search():
    # Získanie údajov o cestách z databázy
    cur = conn.cursor()
    cur.execute("SELECT * FROM route")
    route = cur.fetchall()
    cur.close()
    return render_template("search.html", route=route)

@app.route("/new_ride", methods=["POST"])
def offer():
    # Spracovanie formulára na vytvorenie novej cesty
    route = request.form.get("route")
    date = request.form.get("date")
    notes = request.form.get("notes")

    cur = conn.cursor()
    cur.execute("INSERT INTO route (route, date, notes) VALUES (%s, %s, %s)",
                (route, date, notes))
    conn.commit()
    cur.close()

    return redirect(url_for("offer"))


if __name__ == "__main__":
    app.run(debug=True)
