import json

def to_dict(file_name):
  json_string = ''
  with open(file_name) as file:
    json_string = file.read()
  
  graph_dict = json.loads(json_string)