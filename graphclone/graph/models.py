class Graph(object):

  def __init__(self):
    self.entities = {}
    self.next_entity_id = 1

  def add_entity(self, entity):
    self.entities[entity.id] = entity
    if entity.id >= self.next_entity_id:
        self.next_entity_id = entity.id + 1

  def copy_and_add_entity(self, original_entity):
    new_entity = original_entity.copy(self.next_entity_id)
    self.next_entity_id = self.next_entity_id + 1
    self.entities[new_entity.id] = new_entity
    return new_entity

  def link_entities_by_id(self, from_id, to_id):
    from_entity = self.entities[from_id]
    to_entity = self.entities[to_id]
    self.link_entities(from_entity, to_entity)

  def link_entities(self, from_entity, to_entity):
    from_entity.add_successor(to_entity)
    to_entity.add_predecessor(from_entity)
  
  def clone(self, entity_id):
    # TODO raise error if entity_id doesn't exist in graph
    root_entity = self.entities[entity_id]
    new_subgraph_root_entity = self.copy_subgraph(root_entity, {})
    
    for predecessor in root_entity.predecessors:
      predecessor.add_successor(new_subgraph_root_entity)

  def copy_subgraph(self, root_entity, visited_entities):

    if root_entity.id in visited_entities:
      # stop recursion
      # returns cloned version of the entity
      return visited_entities[root_entity.id]
    
    new_entity = self.copy_and_add_entity(root_entity)
    for successor in root_entity.successors:
      new_linked = self.copy_subgraph(successor, visited_entities)
      self.link_entities(new_entity, new_linked)
    
    visited_entities[root_entity.id] = new_entity
    return new_entity
  
  @staticmethod
  def from_dict(json_dict):
    entities = json_dict.get('entities')
    links = json_dict.get('links')

    graph = Graph()
    
    # TODO validate if entities is list
    for e in entities:
      # TODO validate if entity object has the correct structure
      entity = Entity(e.get('id'), e.get('name'), e.get('description'))
      graph.add_entity(entity)
    
    for link in links:
      graph.link_entities_by_id(link.get('from'), link.get('to'))
    
    return graph


class Entity(object):

  def __init__(self, id, name, description):
    self.id = id
    self.name = name
    self.description = description
    self.successors = []
    self.predecessors = []
  
  def add_successor(self, successor):
    # TODO check if it doesn't exist already
    self.successors.append(successor)
  
  def add_predecessor(self, predecessor):
    # TODO check if it doesn't exist already
    self.predecessors.append(predecessor)

  def copy(self, cloned_id):
    return Entity(
      id=cloned_id,
      name=self.name,
      description=self.description
    )
