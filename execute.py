#!/usr/bin/env python
import argparse

from graphclone.main import process


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Clone an entity in the entity graph.')
  parser.add_argument('input_file', help='input file containing valid json')
  parser.add_argument('entity_id', type=int, help='entity to be cloned with its related entities')
  args = parser.parse_args()

  output = process(args.input_file, args.entity_id)
  print(output)
