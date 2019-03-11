from flask import Flask, current_app, g, render_template,jsonify
import sqlite3,json

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


@app.route('/testdb', methods=['post'])
def testdb():
    cur = g.db.execute('select * from student_info')
    entries = [dict(bf_StudentID=row[0], bf_NativePlace=row[6]) for row in cur.fetchall()]
    return json.dumps(entries)


if __name__ == '__main__':
    app.run(debug=True)
