# Hello
import flask
import config
import mysql.connector

runWithPort = config.config.get("runWithPort");


class Todo:
    def __init__(self,id,title,description):
        self.id = id
        self.title = title
        self.description = description



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
    return flask.jsonify({"message": "Hello User"})

@app.route('/**')
def start():
    return flask.jsonify({"message": "Hello User"})
# SHOW TODOS
@app.route(rule=config.config['todoListROUTE'], methods=config.config.get("todoListMETHOD"))
def Todoslist():
    cursor.execute("SELECT * FROM todos");
    result = cursor.fetchall()
    todos = []

    for x in result:
        todo = Todo(x[0],x[1],x[2])
        todos.append( {"title":todo.title,"description":todo.description,"id":todo.id})

    return flask.jsonify(todos)

# ADD Todo Function
@app.route(rule=config.config['todoAddROUTE'], methods=config.config.get("todoAddMETHOD"))

def AddTodo():

    # Get Body
    data = flask.request.json

    if (data.get('title') == None and config.config['titleIsRequired'] == True or data.get('description') == None ) and config.config['descriptionIsRequired'] == True:
        flask.request.status_code = 400
        return flask.jsonify({"message": "Missing data","statusCode":400})
    else:

        if config.config['titleIsRequired'] == False :
            todo = Todo(0, 'title' , data['description'])
        elif config.config['descriptionIsRequired'] == True :
            todo = Todo(0, data['title'], 'description')
        else :
            todo = Todo(0, data['title'], data['description'])

        # Add Todo In Database
        cursor.execute("INSERT INTO todos (title, description) VALUES (%s, %s)", (todo.title, todo.description))
        mydb.commit()

        return flask.jsonify({"message": "Todo Successfully Added","statusCode":200})


# Read Todo By ID
@app.route(rule=config.config['todoReadROUTE'], methods=config.config.get("todoReadByIDMETHOD"))

def ReadTodoById(id) :
    cursor.execute("SELECT * FROM todos ")
    result = cursor.fetchall()

    finded = False
    # Find Todo By ID
    for x in result:
        if x[0] == id:
            finded = True
            todo = Todo(x[0],x[1],x[2])
            return flask.jsonify({"title":todo.title,"description":todo.description,"id":todo.title})

    # if not id in database
    if not finded:
        return flask.jsonify({"message": "No todo was found with the "+str(id)+" id","statusCode":404})



# Update Todo With ID
@app.route(rule=config.config['todoUpdateROUTE'], methods=config.config.get("todoUpdateMETHOD"))

def UpdateTodo(id):
    data = flask.request.json
    cursor.execute("SELECT * FROM todos ")
    result = cursor.fetchall()

    finded = False
    # Find Todo By ID
    for x in result:
        if x[0] == id:
            finded = True
            if (data.get('title') == None and config.config.get("titleIsRequired") == True or data.get('description') == None and config.config.get("descriptionIsRequired") == True):
                flask.request.status_code = 400
                return flask.jsonify({"message": "Missing data", "statusCode": 400})
            else:
                title = data.get('title')

                description = data.get('description')

                cursor.execute("SELECT * FROM todos ")
                result = cursor.fetchall()

                if (config.config.get("titleIsRequired") == False):
                    for x in result:
                        if x[0] == id:
                            title = x[1]
                elif (config.config.get("descriptionIsRequired") == False):
                    for x in result:
                        if x[0] == id:
                            description = x[2]



                # Update Todo In DataBase
                cursor.execute("UPDATE todos SET title=%s, description=%s WHERE todoID=%s", (title, description, id))
                mydb.commit()

                # Return Response
                return flask.jsonify({"message": "Todo Updated", "statusCode": 200})

    # if not id in database
    if not finded:
        return flask.jsonify({"message": "No todo was found with the "+str(id)+" id","statusCode":404})


# Delete Todo With ID
@app.route(rule=config.config['todoDeleteROUTE'], methods=config.config.get("todoDeleteMETHOD"))

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
            mydb.commit()

            return flask.jsonify({"message": "Todo Deleted With Id : " + str(id), "statusCode": 200})

    if not finded:
        return flask.jsonify({"message": "No todo was found with the "+str(id)+" id","statusCode":404})

if (__name__ == '__main__'):
    if (config.config.get("titleIsRequired") == False and config.config.get("descriptionIsRequired") == False):
        print("Error !!!")
    else :
        print(config.config['runMessage'])
        app.run(port=runWithPort)