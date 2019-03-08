from flask import Flask, current_app, g, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'data/data.db'


def connect_db():
    return sqlite3.connect(DATABASE)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/testdb')
def testdb():
    cur = g.db.execute('select * from exam_type')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return str(entries)


if __name__ == '__main__':
    app.run(debug=True)
