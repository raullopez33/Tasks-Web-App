from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Task
from config import Config
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Create database tables using alembic (updates schema)
with app.app_context():
    target_metadata = db.metadata


# Routes
@app.route("/")
def home():
    return render_template("index.html")

# Route to add a task
@app.route("/tasks", methods=["POST"])
def add_task():
    
    data = request.json
    due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

    username = data.get("username")
    title = data.get("title")
    description = data.get("description")
    due_date = due_date

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_task = Task(title=title, description=description, due_date=due_date, owner=user)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task added successfully"}), 200

# Route to get all tasks for a user
@app.route("/tasks", methods=["GET"])
def get_tasks():
    username = request.args.get("username")

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    tasks = [{"id": task.id, "title": task.title, "description": task.description, "due_date": task.due_date} for task in user.tasks]
    return jsonify(tasks), 200

# Route to delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": f"Task {task_id} deleted successfully"}), 200

# Route to add a new user
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 200

@app.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # Ensure passwords are hashed in production!
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"error": "Invalid username or password"}), 401

if __name__ == "__main__":
    app.run(debug=True)
