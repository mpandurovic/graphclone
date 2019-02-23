import os
from unittest import TestCase

from graphclone.main import process

current_dir = os.path.dirname(__file__)

class TestProcess(TestCase):

  def test_process(self):
    file_name = os.path.join(current_dir, 'fixtures/input.json')
    output_string = process(file_name, 5, sort_keys_and_objects=True)
    
    with open(os.path.join(current_dir, 'fixtures/output.json')) as file:
      expected_output = file.read()
      self.assertEqual(expected_output.replace(' ', ''), output_string.replace(' ', ''))
