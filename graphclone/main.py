import json

from graphclone.utils.parser import from_json_file
from graphclone.graph.models import Graph


def process(input_file, entity_id, sort_keys_and_objects=False):
  """
  Function that processes input and returns string to be written 
  in stdout.
  
  :param input_file: 
    input file
  :param entity_id: 
    root entity id to start cloning from
  :param sort_keys_and_objects: 
    if set to True, enables sorting of keys and objects in output json
  """
  graph = Graph.from_dict(from_json_file(input_file), sort_links=sort_keys_and_objects)
  graph.clone(entity_id)
  return json.dumps(graph.to_dict(), indent=4, sort_keys=sort_keys_and_objects)