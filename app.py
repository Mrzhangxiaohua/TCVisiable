from flask import Flask, current_app, g, render_template, jsonify, request
import sqlite3, json

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

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/testdb', methods=['post'])
def testdb():
    cur = g.db.execute('select * from student_info')
    entries = [dict(bf_StudentID=row[0], bf_NativePlace=row[6]) for row in cur.fetchall()]
    return json.dumps(entries)


@app.route('/getStuId', methods=['GET', 'POST'])
def getStuId():
    a = request.args
    if a:
        data = a['data']
        print(data)
        # 找出学生考试完全信息
        sql = "select a.*,b.EXAM_KIND_NAME from chengji a left join exam_type b on a.exam_type=b.EXAM_KIND_ID where mes_StudentID= " + data + " and mes_sub_id !='' and mes_Z_Score!=''"
        cur = g.db.execute(sql)
        entries = [dict(mes_TestID=row[0], exam_number=row[1], exam_numname=row[2], mes_sub_id=row[3],
                        mes_sub_name=row[4], exam_term=row[5], exam_type=row[6], mes_StudentID=row[8],
                        mes_Score=row[9], mes_Z_Score=row[10], mes_T_Score=row[11], mes_dengdi=row[12],
                        EXAM_KIND_ID=row[13])
                   for row in cur.fetchall()]
        # 找出学生考试时间类别,语文数学。。。
        sql1 = " select a.mes_sub_name from chengji a left join exam_type b on a.exam_type=b.EXAM_KIND_ID " \
                   " where mes_StudentID= " + data + " and mes_sub_id !='' and mes_Z_Score!='' group by mes_sub_name "
        cur1 = g.db.execute(sql1)
        entries1 = [dict(mes_sub_name = row[0]) for row in cur1.fetchall()]
        # 找出学生的考试时间
        sql2 = " select distinct a.exam_numname from chengji a left join exam_type b on a.exam_type=b.EXAM_KIND_ID " \
                   " where mes_StudentID= " + data + " and mes_sub_id !='' and mes_Z_Score!='' "
        cur2 = g.db.execute(sql2)
        entries2 = [dict(exam_numname=row[0]) for row in cur2.fetchall()]
        d = {"data": entries, "examType": entries1, "examTime":entries2}
        return jsonify(d)
    return jsonify('fail')


if __name__ == '__main__':
    app.run(debug=True)
