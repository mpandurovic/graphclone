# Overview

Python script that accepts an input json containing a graph and entity ID, clones the requested entity and all its related entities, and writes the result to standard output.

# Prerequisites

* Python version 2.7.* or 3.5.* (tested with these versions, but likely to work with other builds)

# Running the script
Clone this repository and from the root directory of the project execute a command with the following format:
```sh
$ ./execute.py <input_file_path> <entity_id>
```

`input_file_path` should contain a json object with `entities` and `links` (check [Input format](#input-format) for concrete example). `entity_id` should be an integer ID of an entity contained in the graph. 

Concrete example:
```sh
$ ./execute.py graphclone/fixtures/input.json 5
```
For more information, run the following:
```sh
$ ./execute.py -h
```

# Input format
Input file needs to be in the following format for script to execute correctly:
```json
{
  "entities": [
    {
      "entity_id": 3,
      "name": "EntityA"
    },
    {
      "entity_id": 5,
      "name": "EntityB"
    },
    {
      "entity_id": 7,
      "name": "EntityC",
      "description": "More details about entity C"
    },
    {
      "entity_id": 11,
      "name": "EntityD"
    }
  ],
  "links": [
    {
      "from": 3,
      "to": 5
    },
    {
      "from": 3,
      "to": 7
    },
    {
      "from": 5,
      "to": 7
    },
    {
      "from": 7,
      "to": 11
    }
  ]
}
```
Where links contain `from` and `to` keys that represent ids of the entities that they connect. The links are directional which means the following two objects are NOT the same and therefore valid as an input:
```json
{
      "from": 3,
      "to": 5
}
...
{
      "from": 5,
      "to": 3
}
```
# Running tests

Tests can be executed with the following command:
```sh
$ python -m unittest discover graphclone
```