#!/usr/bin/env python
import argparse
import json

from graphclone.parser.parser import from_json_file
from graphclone.graph.models import Graph


def clone_subgraph(input_file, entity_id):
  graph = Graph.from_dict(from_json_file(input_file))
  graph.clone(entity_id)
  print(json.dumps(graph.to_dict()))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Clone an entity in the entity graph.')
  parser.add_argument('input_file', help='input file containing valid json')
  parser.add_argument('entity_id', type=int, help='entity to be cloned with its related entities')
  args = parser.parse_args()

  clone_subgraph(args.input_file, args.entity_id)
