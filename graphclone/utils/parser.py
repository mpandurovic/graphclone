import json

def from_json_file(file_name):
  """ Reads and parses the file as json. """
  with open(file_name) as file:
    json_string = file.read()
  
  return json.loads(json_string)
