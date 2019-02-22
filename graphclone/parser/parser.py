import json

def from_json_file(file_name):
  json_string = ''
  with open(file_name) as file:
    json_string = file.read()
  
  return json.loads(json_string)
