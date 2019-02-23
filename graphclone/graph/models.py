import numbers

class Entity(object):
  """
  Class that represents entities/vertices in the graph
  """

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
    """
    Creates a copy of itself using the 
    provided clone_id parameter. 
    """
    return Entity(
      id=cloned_id,
      name=self.name,
      description=self.description
    )

class Graph(object):
  """
  Graph representation. 
  Contains a map/dictionary of all entities 
  (stored as entity_id -> entity pairs).
  """

  def __init__(self, sort_links=False):
    """
    :param sort_links: 
      Sorts links (successors/predecessors) 
      by entity id when cloning or converting the graph
      to a dictionary.
    """
    self.entities = {}
    # used when copying/cloning entities into the graph
    self.next_entity_id = 1
    self.sort_links = True

  def add_entity(self, entity):
    """
    Adds entity to the graph. 
    Links should be created explicitly (by calling link_entities()).

    If the same id already exists, the old entity is replaced.
    """
    if entity is None:
      return
    
    self.entities[entity.id] = entity
    if entity.id >= self.next_entity_id:
        self.next_entity_id = entity.id + 1

  def copy_and_add_entity(self, original_entity):
    """
    Copies original_entity and adds the copy to the graph.
    """
    new_entity = original_entity.copy(self.next_entity_id)
    self.add_entity(new_entity)
    return new_entity

  def link_entities_by_id(self, from_id, to_id):
    from_entity = self.entities.get(from_id)
    to_entity = self.entities.get(to_id)
    self.link_entities(from_entity, to_entity)

  def link_entities(self, from_entity, to_entity):
    """
    Links entities within the graph. 
    """
    if from_entity is None or to_entity is None:
      return
    from_entity.add_successor(to_entity)
    to_entity.add_predecessor(from_entity)
  
  def clone(self, entity_id):
    """
    Clones an entity and all related entities (in place).
    """
    root_entity = self.entities.get(entity_id)
    if root_entity is None:
      return
    
    new_subgraph_root_entity = self.copy_subgraph(root_entity, {})
    
    for predecessor in self.get_predecessors_for(root_entity):
      predecessor.add_successor(new_subgraph_root_entity)

  def copy_subgraph(self, root_entity, visited_entities):

    if root_entity.id in visited_entities:
      # stop recursion and return cloned version of the entity
      return visited_entities[root_entity.id]
    
    new_entity = self.copy_and_add_entity(root_entity)
    visited_entities[root_entity.id] = new_entity

    for successor in self.get_successors_for(root_entity):
      # call recursively
      new_linked = self.copy_subgraph(successor, visited_entities)
      self.link_entities(new_entity, new_linked)
    
    # all successors have been visited,
    # stop recursion and return entity
    return new_entity

  def get_successors_for(self, entity):
    """
    Gets entity successors 
    (sorted or not, depending on sort_links flag)
    """
    return (entity.get_sorted_successors() 
            if self.sort_links 
            else entity.successors)

  def get_predecessors_for(self, entity):
    """
    Gets entity predecessors 
    (sorted or not, depending on sort_links flag)
    """
    return (entity.get_sorted_predecessors() 
            if self.sort_links 
            else entity.predecessors)
  
  @staticmethod
  def from_dict(json_dict={}, sort_links=False):
    """
    Parses dictionary containing entities and links,
    and creates a Graph object.
    """
    entities = json_dict.get('entities')
    links = json_dict.get('links')

    graph = Graph(sort_links)
    
    for e in entities if isinstance(entities, list) else []:
      entity = Entity(e['entity_id'], e['name'], e.get('description'))
      graph.add_entity(entity)
    
    for link in links if isinstance(links, list) else []:
      graph.link_entities_by_id(link['from'], link['to'])
    
    return graph

  def to_dict(self):
    """
    Creates a dictionary from Graph object
    """
    
    json_dict = {
      'entities': [],
      'links': [],
    }

    for entity_id in self.get_entity_ids():
      entity = self.entities[entity_id]
      entity_dict = {
        'entity_id': entity.id,
        'name': entity.name,
      }
      if entity.description is not None:
        entity_dict['description'] = entity.description
      
      json_dict['entities'].append(entity_dict)
      
      for successor in self.get_successors_for(entity):
        json_dict['links'].append({
          'from': entity.id,
          'to': successor.id
        })
    
    return json_dict
  
  def get_entity_ids(self):
    """
    Gets entity ids 
    (sorted or not, depending on sort_links flag)
    """
    return (sorted(self.entities.keys()) 
            if self.sort_links 
            else self.entities.keys())
