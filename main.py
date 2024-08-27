# Hello
import flask
import mysql.connector

runWithPort = 8080

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
@app.route('/api/Todo/list', methods=['GET'])

def Todoslist():
    cursor.execute("SELECT * FROM todos");
    result = cursor.fetchall()
    todos = []

    for x in result:
         todos.append( {"title":x[1],"description":x[2],"id":x[0]})

    return flask.jsonify(todos)


# ADD Todo Function
@app.route('/api/Todo/add ', methods=['POST'])

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


# Read Todo By ID
@app.route('/api/Todo/<int:id>', methods=['GET'])

def ReadTodoById(id) :
    cursor.execute("SELECT * FROM todos ")
    result = cursor.fetchall()

    finded = False
    # Find Todo By ID
    for x in result:
        if x[0] == id:
            finded = True
            return flask.jsonify({"title":x[1],"description":x[2],"id":x[0]})

    # if not id in database
    if not finded:
        return flask.jsonify({"message": "No todo was found with the "+str(id)+" id","statusCode":404})



# Update Todo With ID
@app.route("/api/Todo/update/<int:id>", methods=['POST'])

def UpdateTodo(id):
    data = flask.request.json
    cursor.execute("SELECT * FROM todos ")
    result = cursor.fetchall()

    finded = False
    # Find Todo By ID
    for x in result:
        if x[0] == id:
            finded = True
            if (data.get('title') == None or data.get('description') == None):
                flask.request.status_code = 400
                return flask.jsonify({"message": "Missing data", "statusCode": 400})
            else:
                title = data.get('title')

                description = data.get('description')

                # Update Todo In DataBase
                cursor.execute("UPDATE todos SET title=%s, description=%s WHERE todoID=%s", (title, description, id))

                # Return Response
                return flask.jsonify({"message": "Todo Updated", "statusCode": 200})

    # if not id in database
    if not finded:
        return flask.jsonify({"message": "No todo was found with the "+str(id)+" id","statusCode":404})


# Delete Todo With ID
@app.route("/api/Todo/delete/<int:id>", methods=['POST'])

def DeleteTodo(id):
    # Getting All Todos
    cursor.execute("SELECT * FROM todos")

    result = cursor.fetchall()

    finded = False

    for x in result:
        if x[0] == id:
            finded = True

            # Delete Todo In Database

            cursor.execute("DELETE FROM `todos` WHERE todoID = '%s'" % (id,))


            return flask.jsonify({"message": "Todo Deleted With Id : " + str(id), "statusCode": 200})

    if not finded:
        return flask.jsonify({"message": "No todo was found with the "+str(id)+" id","statusCode":404})

if (__name__ == '__main__'):
    app.run(port=runWithPort)