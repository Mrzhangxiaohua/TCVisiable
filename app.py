from flask import Flask, current_app, g, render_template, jsonify, request
import sqlite3, json

app = Flask(__name__)
app.config.from_object('config')
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
    seven_select_three = [["政治", "历史", "地理"],
                          ["政治", "历史", "物理"],
                          ["政治", "历史", "化学"],
                          ["政治", "历史", "通用技术"],
                          ["政治", "地理", "物理"],
                          ["政治", "地理", "化学"],
                          ["政治", "地理", "生物"],
                          ["政治", "地理", "通用技术"],
                          ["政治", "物理", "化学"],
                          ["政治", "物理", "生物"],
                          ["政治", "物理", "通用技术"],
                          ["政治", "化学", "生物"],
                          ["政治", "化学", "通用技术"],
                          ["政治", "生物", "通用技术"],
                          ["历史", "地理", "物理"],
                          ["历史", "地理", "化学"],
                          ["历史", "地理", "生物"],
                          ["历史", "地理", "通用技术"],
                          ["历史", "物理", "化学"],
                          ["历史", "物理", "生物"],
                          ["历史", "物理", "通用技术"],
                          ["历史", "化学", "生物"],
                          ["历史", "化学", "通用技术"],
                          ["历史", "生物", "通用技术"],
                          ["地理", "物理", "化学"],
                          ["地理", "物理", "生物"],
                          ["地理", "物理", "通用技术"],
                          ["地理", "化学", "生物"],
                          ["地理", "化学", "通用技术"],
                          ["地理", "生物", "通用技术"],
                          ["物理", "化学", "生物"],
                          ["物理", "化学", "通用技术"],
                          ["物理", "生物", "通用技术"],
                          ["化学", "生物", "通用技术"]]
    cur = g.db.execute('')

    return render_template('course.html')


@app.route('/groupdata')
def groupData():
    # 找到高三的班级id，一共10个班级
    sql_findClassId = " select distinct cla_id, cla_Name from student_info where cla_Name like '%高三%' order by cla_id asc "
    cur = g.db.execute(sql_findClassId)
    fetchData = [[row[0], row[1]] for row in cur.fetchall()[2:-2]]
    entries = [k[0] for k in fetchData]
    className = [k[1] for k in fetchData]
    print(entries)
    print(className)
    # 对每个班级进行成绩的统计,每个人考七门
    sql_findClassStuInf = " select a.bf_StudentID, a.cla_Name, a.cla_id, a.cla_term, b.exam_numname,b.mes_sub_id, " \
                          " b.mes_sub_name,b.exam_term,b.mes_Score, b.mes_Z_Score,b.mes_T_Score, mes_dengdi " \
                          " from student_info a left join chengji b on bf_StudentID=mes_StudentID " \
                          " where cla_Name like '%高三%' AND mes_Z_Score!='' and mes_T_Score!='' and mes_dengdi!='' " \
                          " and cla_term='2018-2019-1' and exam_numname='2017学年第二学期高一二平时成绩1' and cla_id="
    kemu = ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '技术']
    sumscore = []
    for i in entries:
        cur1 = g.db.execute(sql_findClassStuInf + str(i))
        entries = [dict(bf_StudentID=row[0], cla_Name=row[1], cla_id=row[2], cla_term=row[3],
                        exam_numname=row[4], mes_sub_id=row[5], mes_sub_name=row[6], exam_term=row[7],
                        mes_Score=row[8], mes_Z_Score=row[9], mes_T_Score=row[10], mes_dengdi=row[11])
                   for row in cur1.fetchall()]
        classGrade = [[] for i in range(10)]
        for entrie in entries:
            if entrie['mes_sub_name'] == '语文':
                classGrade[0].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '数学':
                classGrade[1].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '英语':
                classGrade[2].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '物理':
                classGrade[3].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '化学':
                classGrade[4].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '生物':
                classGrade[5].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '政治':
                classGrade[6].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '历史':
                classGrade[7].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '地理':
                classGrade[8].append(entrie['mes_Score'])
            elif entrie['mes_sub_name'] == '技术':
                classGrade[9].append(entrie['mes_Score'])
        sumscore.append(classGrade)
    print(sumscore)
    d = {'data': sumscore, 'classId': entries, 'kind': kemu, 'className':className}
    return jsonify(d)


@app.route('/group')
def group():
    return render_template('group.html')

@app.route('/testdb')
def testdb():
    sql_test = "select distinct exam_numname from chengji where exam_term='2017-2018-1'AND mes_Z_Score!='' and mes_T_Score!='' and mes_dengdi!=''"
    cur = g.db.execute(sql_test)
    entries = [row[0] for row in cur.fetchall()]
    print(entries)
    return jsonify(entries)


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
        entries1 = [dict(mes_sub_name=row[0]) for row in cur1.fetchall()]
        # 找出学生的考试时间
        sql2 = " select distinct a.exam_numname from chengji a left join exam_type b on a.exam_type=b.EXAM_KIND_ID " \
               " where mes_StudentID= " + data + " and mes_sub_id !='' and mes_Z_Score!='' "
        cur2 = g.db.execute(sql2)
        entries2 = [dict(exam_numname=row[0]) for row in cur2.fetchall()]
        d = {"data": entries, "examType": entries1, "examTime": entries2}
        return jsonify(d)
    return jsonify('fail')


if __name__ == '__main__':
    app.run()
