import json

#Task for USERS Class 
class Task:

  
  TASKS_FILE = "tasks.json"
  tasks = []

  @classmethod
  def load(cls):

    try:
      with open(cls.TASKS_FILE) as file:
        task_data = json.load(file)
        cls.tasks = list(map(Task, task_data)) #
    
    except:
      tasks = []  #if fails to load just an empty list

  #save the task onto JSON file u
  @classmethod
  def save(cls):
     with open(cls.TASKS_FILE, "w") as f:
      try:
        dict_tasks = list(map(vars, cls.tasks))
        json.dump(dict_tasks, f, indent=4)
        return True
      except:
         return False
  

  #add Task object
  @classmethod
  def add(cls, task):
    try:
       cls.tasks.append(task)
       return True
    except:
       return False
  @classmethod
  def get_user_tasks(cls, username):
     #user_tasks = filter(lambda t: t.username == username, cls.tasks)
     #return list(map(vars, user_tasks)
      user_tasks = []
      for t in cls.tasks:
        if t.username == username:
           user_tasks.append(vars(t)) # send info back to the client
      return user_tasks
     
  def __init__(self, data):
     self.username = data["username"]
     self.title = data["title"]
     self.description = data["description"]
     self.due_date = data["due_date"]

     #more control of data using dict
     self.__dict__ = {
        "username": self.username,
        "title" : self.title,
        "description" : self.description,
        "due_date" : self.due_date
     }

class User:

  USERS_FILE = "users.json"
  users = []

  def __init__(self, data):
    self.username = data["username"]
    self.first_name = data ["first_name"]
    self.last_name = data["last_name"]
    self.password = data["password"]
    self.__dict__ = {
      "username" : self.username,
      "first_name" : self.first_name,
      "last_name" : self.last_name,
      "password" : self.password
    }

  @classmethod
  def load(cls):

    try:
      with open(cls.USERS_FILE) as file:
        user_data = json.load(file)
        cls.users = list(map(User, user_data)) 
    
    except:
      users = []  #if fails to load just an empty list

  #save the USER onto JSON file 
  @classmethod
  def save(cls):
     with open(cls.USERS_FILE, "w") as f:
      try:
        dict_users = list(map(vars, cls.users))
        json.dump(dict_users, f, indent=4)
        return True
      except:
         return False
  

  #add Task object
  @classmethod
  def add(cls, user):
    try:
       cls.users.append(user)
       return True
    except:
       return False
    
  @classmethod
  def get_user(cls, username):
     
    for u in cls.users:
       if u.username == username:
         return u 
    return None 
     
    
  @classmethod 
  def authenticate(cls, username, password):
    found_user = cls.get_user(username)
    if found_user:
      return found_user.password == password
