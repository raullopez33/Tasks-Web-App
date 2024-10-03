import json
import requests
import getpass

CONFIG_FILE = "config.json"


def print_usage():
  print("USAGE: python taskclient.py [init|add|tasks|delete]")

def load_config():
  #Application state (whats going on at any given point)
  try:
    with open(CONFIG_FILE, "r") as f:
      return json.load(f)
  
  except:
    return None
  


def get_pass():
  return getpass.getpass("Password: ")


def init():
  first_name = input("First Name: ")
  last_name = input("Last Name: ")
  username = input("username: ")
  password = input("password: ")
  server_url = input("server url: ")


  config_data = {
    "first_name": first_name,
    "last_name": last_name,
    "username": username,
    "password": password,
    "server_url": server_url
}

  with open(CONFIG_FILE, "w") as f:
    json.dump(config_data, f, indent=4)
  
  print("Registering with server")
  register()

def register():
  config = load_config()
  if config:
    data = {

      "first_name" : config["first_name"],
      "last_name" : config["last_name"],
      "username" : config["username"],
      "password" : config["password"]
    }
    url = config["server_url"] + "/users"
    r = requests.post(url, json=data)
    if r.status_code == 200:
      print("User registered!")
    else:
      r.text
  else:
    print("No config found! Run taskclient init")
  

def add():
  config = load_config()
  if config:
    title = input("Title: ")
    description = input("Description: ")
    due_date = input("Due Date YYYY-MM-DD: ")

    data = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "username": config["username"],
        "password": get_pass()

    }
    url = config["server_url"] + "/tasks" #server URL
    r = requests.post(url, json=data)
    print(r.text)

  else:
    print("No Config found! Run taskclient.py Init")

def tasks():
  config = load_config()
  url = config["server_url"] + "/tasks?u={}&p={}".format(config["username"], config["password"])
  r = requests.get(url)
  print_tasks(r.json())


def print_tasks(tasks):
  
  for i, t in enumerate(tasks):
    print("{}: {} ({})".format(i+1, t["title"], t["due_date"]))
    
