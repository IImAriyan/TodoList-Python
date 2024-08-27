# Hello
import flask

import mysql.connector
app = flask.Flask(__name__)

# Connecting To Database

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="todolist"
)

cursor = mydb.cursor();



@app.route('/')
def index():
    return flask.jsonify({"message": "Hello World"})



# SHOW TODOS
@app.route('/api/Todo/list')
def Todoslist():
    cursor.execute("SELECT * FROM todos");
    result = cursor.fetchall()
    todos = []
    for x in result:
         todos.append( {"title":x[1],"description":x[2],"id":x[0]})
    return flask.jsonify(todos)


if (__name__ == '__main__'):
    app.run(port=8080)