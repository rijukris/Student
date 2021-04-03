from flask import Flask, render_template, json, jsonify, request
import mysql.connector

import sys

app = Flask(__name__)

students = None
db = None
cursor = None


def get_students_data():
    sql_str = "SELECT * FROM STUDENT"
    cursor.execute(sql_str)
    result = []
    columns = tuple([d[0] for d in cursor.description])
    for row in cursor:
        result.append(dict(zip(columns, row)))
    return result


def get_student_data(mobile):
    sql_str = f"SELECT * FROM STUDENT WHERE mobile={mobile}"
    cursor.execute(sql_str)
    rows = cursor.fetchall()
    d = {
        "first_name": rows[0][0],
        "last_name": rows[0][1],
        "age": rows[0][2],
        "gender": rows[0][3]
    }
    return d


@app.route('/students')
def get_students():
    global students
    students = get_students_data()
    return render_template("students.html", data=students)


@app.route('/student/<mobile>')
def get_student(mobile):
    global students
    s = get_student_data(mobile)
    return jsonify(s)


@app.route('/student')
def get_a_student():
    global students
    s = get_student_data(request.args.get("mobile"))
    return jsonify(s)


@app.route('/student/<mobile>', methods=['POST'])
def create_student(mobile):
    try:
        sql_str = f"INSERT INTO STUDENT VALUES ('{request.json['first_name']}', '{request.json['last_name']}', {int(request.json['age'])}, '{request.json['gender']}', '{mobile}')"
        print(sql_str)
        cursor.execute(sql_str)
        db.commit()
        return f"Created student for {mobile}"
    except mysql.connector.Error as e:
        return f"ERROR: {e} while creating student for {mobile}"


@app.route('/students', methods=['POST'])
def create_students():
    try:
        for student in request.json:
            sql_str = f"INSERT INTO STUDENT VALUES ('{student['first_name']}', '{student['last_name']}', {int(student['age'])}, '{student['gender']}', '{student['mobile']}')"
            print(sql_str)
            cursor.execute(sql_str)
            db.commit()
        return f"Created students"
    except mysql.connector.Error as e:
        return f"ERROR: {e} while creating students"



@app.route('/student/<mobile>', methods=['PUT'])
def update_student(mobile):
    try:
        sql_str = f"UPDATE STUDENT SET "
        for k in request.json.keys():
            if k == "age":
                sql_str += f"{k}={int(request.json[k])}, "
            else:
                sql_str += f"{k}='{request.json[k]}', "
        sql_str = sql_str.rstrip(", ")
        sql_str += f" WHERE mobile='{mobile}'"
        print(sql_str)
        cursor.execute(sql_str)
        db.commit()
        return f"Updated student for {mobile}"
    except mysql.connector.Error as e:
        return f"ERROR: {e} while updating student for {mobile}"


@app.route('/student/<mobile>', methods=['DELETE'])
def delete_student(mobile):
    try:
        sql_str = f"DELETE FROM STUDENT WHERE mobile='{mobile}'"
        cursor.execute(sql_str)
        db.commit()
        return f"Deleted student for {mobile}"
    except mysql.connector.Error as e:
        return f"ERROR: {e} while deleting student for {mobile}"


@app.route('/students', methods=['DELETE'])
def delete_students():
    try:
        sql_str = "DELETE FROM STUDENT"
        cursor.execute(sql_str)
        db.commit()
        return f"Deleted all students"
    except mysql.connector.Error as e:
        return f"ERROR: {e} while deleting students"


def main():
    global db, cursor
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Disney!23",
        database="testdb"
    )

    cursor = db.cursor()

    app.run(debug=True)


if __name__ == "__main__":
    main()
