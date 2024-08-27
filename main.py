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


# ADD Todo Function
@app.route('/api/Todo/add', methods=['POST'])
def AddTodo():

    # Get Body
    data = flask.request.json

    if (data.get('title') == None or data.get('description') == None ):
        flask.request.status_code = 400
        return flask.jsonify({"message": "Missing data","statusCode":400})
    else:

        title = data.get('title')
        description = data.get('description')

        # Add Todo In Database
        cursor.execute("INSERT INTO todos (title, description) VALUES (%s, %s)", (title, description))

        return flask.jsonify({"message": "Todo Successfully Added","statusCode":200})



if (__name__ == '__main__'):
    app.run(port=8080)