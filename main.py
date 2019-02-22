#!/usr/bin/env python
import argparse

from graphclone.parser.parser import to_dict

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Clone an entity in the entity graph.')
  parser.add_argument('input_file', help='input file containing valid json')
  parser.add_argument('entity_id', type=int, help='entity to be cloned with its related entities')
  args = parser.parse_args()

  to_dict(args.input_file)
