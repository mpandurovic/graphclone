import numbers

class Entity(object):

  def __init__(self, id, name, description=None):
    self.id = id
    self.name = name
    self.description = description
    self.successors = set()
    self.predecessors = set()

  def __repr__(self):
    return "Entity[{}, {}]".format(self.id, self.name)

  def get_sorted_successors(self, get_sorted=False):
    return sorted(self.successors, key=lambda e: e.id)
  
  def add_successor(self, successor):
    if successor is None:
      return
    self.successors.add(successor)

  def get_sorted_predecessors(self, get_sorted=False):
    return sorted(self.predecessors, key=lambda e: e.id)
  
  def add_predecessor(self, predecessor):
    if predecessor is None:
      return
    self.predecessors.add(predecessor)

  def copy(self, cloned_id):
    return Entity(
      id=cloned_id,
      name=self.name,
      description=self.description
    )

class Graph(object):

  def __init__(self, sort_links=False):
    self.entities = {}
    self.next_entity_id = 1
    self.sort_links = True

  def add_entity(self, entity):
    if entity is None:
      return
    
    self.entities[entity.id] = entity
    if entity.id >= self.next_entity_id:
        self.next_entity_id = entity.id + 1

  def copy_and_add_entity(self, original_entity):
    new_entity = original_entity.copy(self.next_entity_id)
    self.next_entity_id = self.next_entity_id + 1
    self.entities[new_entity.id] = new_entity
    return new_entity

  def link_entities_by_id(self, from_id, to_id):
    from_entity = self.entities.get(from_id)
    to_entity = self.entities.get(to_id)
    self.link_entities(from_entity, to_entity)

  def link_entities(self, from_entity, to_entity):
    if from_entity is None or to_entity is None:
      return
    from_entity.add_successor(to_entity)
    to_entity.add_predecessor(from_entity)
  
  def clone(self, entity_id):
    # TODO raise error if entity_id doesn't exist in graph
    root_entity = self.entities.get(entity_id)
    if root_entity is None:
      return
    
    new_subgraph_root_entity = self.copy_subgraph(root_entity, {})
    
    predecessors = (root_entity.get_sorted_predecessors() 
                  if self.sort_links 
                  else root_entity.predecessors)
    for predecessor in predecessors:
      predecessor.add_successor(new_subgraph_root_entity)

  def copy_subgraph(self, root_entity, visited_entities):

    if root_entity.id in visited_entities:
      # stop recursion and return cloned version of the entity
      return visited_entities[root_entity.id]
    
    new_entity = self.copy_and_add_entity(root_entity)
    visited_entities[root_entity.id] = new_entity

    successors = (root_entity.get_sorted_successors() 
                  if self.sort_links 
                  else root_entity.successors)
    for successor in successors:
      new_linked = self.copy_subgraph(successor, visited_entities)
      self.link_entities(new_entity, new_linked)
    
    return new_entity
  
  @staticmethod
  def from_dict(json_dict={}, sort_links=False):
    entities = json_dict.get('entities', {})
    links = json_dict.get('links', {})

    graph = Graph(sort_links)
    
    # TODO validate if entities is list
    for e in entities:
      # TODO validate if entity object has the correct structure
      entity = Entity(e.get('entity_id'), e.get('name'), e.get('description'))
      graph.add_entity(entity)
    
    for link in links:
      graph.link_entities_by_id(link.get('from'), link.get('to'))
    
    return graph

  def to_dict(self):
    
    json_dict = {
      'entities': [],
      'links': [],
    }

    for entity_id in self.entities:
      entity = self.entities[entity_id]
      entity_dict = {
        'entity_id': entity.id,
        'name': entity.name,
      }
      if entity.description is not None:
        entity_dict['description'] = entity.description
      
      json_dict['entities'].append(entity_dict)
      

      successors = (entity.get_sorted_successors() 
                  if self.sort_links 
                  else entity.successors)
      for successor in successors:
        json_dict['links'].append({
          'from': entity.id,
          'to': successor.id
        })
    
    return json_dict
