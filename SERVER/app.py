from flask import Flask, request, make_response
import json
from serverlib import *



app = Flask(__name__)   #when Flasks runs program 

#Init Data
Task.load()
User.load()

#Decorators
@app.route("/tasks", methods = ["GET", "POST"])
def tasks_router():
    if request.method == "POST":

        data = request.json
        print(data)
        username = data["username"]
        password = data["password"]

        if User.authenticate(username, password):
            new_task = Task(data)
            Task.add(new_task)
            Task.save()
            return make_response(("Task created", 200))
        else:
            return make_response("Authentication failed", 401)
    else:
        username = request.args.get("u")
        password = request.args.get("p")
        if User.authenticate(username, password):
            user_tasks = Task.get_user_tasks(username)
            return make_response(json.dumps(user_tasks), 200)
        
        return make_response("Authentication failed", 401)


        
@app.route("/users", methods =["GET", "POST"])
def user_router():
    if request.method == "POST":
        data = request.json
        try:
            new_user = User(data)
            User.add(new_user)
            User.save()
            return make_response("User created", 200)
        except:
            return make_response("Creation failed", 500)
        

    

