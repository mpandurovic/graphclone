import os
from unittest import TestCase

from graphclone.utils.parser import from_json_file

current_dir = os.path.dirname(__file__)

class TestFromJsonFile(TestCase):

  def test_from_json_file_when_file_does_not_exist(self):
    json_file = os.path.join(current_dir, 'fixtures/doesnt_exist.json')
    with self.assertRaises(IOError):
      from_json_file(json_file)

  def test_from_json_file_when_json_is_not_valid(self):
    json_file = os.path.join(current_dir, 'fixtures/invalid.json')
    with self.assertRaises(ValueError):
      from_json_file(json_file)

  def test_from_json_file_when_json_is_valid(self):
    json_file = os.path.join(current_dir, 'fixtures/valid.json')
    json_dict = from_json_file(json_file)
    self.assertTrue(json_dict['isValid'])
