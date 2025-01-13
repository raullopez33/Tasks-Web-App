import sys
import json 
from clientlib import *

COMMANDS = ["init", "add", "tasks", "delete"]

def main():

  #Get Subcommand
  try:
    cmd = sys.argv[1]
  except IndexError:
    print("No command provided")
    print_usage()


  #Validate Subcommand
  if cmd not in COMMANDS:
    print("Invalid command")
    print_usage()
    sys.exit(-1)


  if cmd == "init":
    init()
    

  if cmd == "add":
    add()
    
  if cmd == "tasks":
    tasks()
    
  
main()