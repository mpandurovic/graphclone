from unittest import TestCase

from graphclone.graph.models import Entity
from graphclone.graph.models import Graph

class AssertEntityMixin(object):
  def assert_links(self, entity, successors=None, predecessors=None):
    if successors is None:
      successors = set()
    if predecessors is None:
      predecessors = set()

    self.assertSetEqual(entity.successors, successors)
    self.assertSetEqual(entity.predecessors, predecessors)


class TestEntity(TestCase, AssertEntityMixin):

  def setUp(self):
    self.entity = Entity(1, 'entity')

  def test_add_successor_when_none_is_passed(self):
    self.assert_links(self.entity)

    self.entity.add_successor(None)

    self.assert_links(self.entity)
  
  def test_add_successor_when_new_entity_is_passed(self):
    self.assert_links(self.entity)

    succ = Entity(2, 'succ')
    self.entity.add_successor(succ)

    self.assert_links(self.entity, successors=set([succ]))

  def test_add_successor_when_existing_entity_is_passed(self):
    succ = Entity(2, 'succ')
    other_succ = Entity(3, 'other_succ')
    self.entity.successors = set([succ, other_succ])

    self.assert_links(self.entity, successors=set([succ, other_succ]))

    self.entity.add_successor(succ)

    self.assert_links(self.entity, successors=set([succ, other_succ]))

  def test_add_predecessor_when_none_is_passed(self):
    self.assert_links(self.entity)

    self.entity.add_predecessor(None)

    self.assert_links(self.entity)
  
  def test_add_predecessor_when_new_entity_is_passed(self):
    self.assert_links(self.entity)

    pred = Entity(2, 'pred')
    self.entity.add_predecessor(pred)

    self.assert_links(self.entity, predecessors=set([pred]))

  def test_add_predecessor_when_existing_entity_is_passed(self):
    pred = Entity(2, 'pred')
    other_pred = Entity(3, 'other_pred')
    self.entity.predecessors = set([pred, other_pred])

    self.assert_links(self.entity, predecessors=set([pred, other_pred]))

    self.entity.add_predecessor(pred)
    
    self.assert_links(self.entity, predecessors=set([pred, other_pred]))

  def test_copy(self):
    original = Entity(1, 'entity', 'description')

    copy = original.copy(2)

    self.assertNotEqual(original, copy)
    self.assertEqual(copy.id, 2)
    self.assertEqual(copy.name, 'entity')
    self.assertEqual(copy.description, 'description')


class TestGraphAddEntity(TestCase):

  def setUp(self):
    self.graph = Graph()

  def test_add_entity_when_none_is_passed(self):
    self.assertDictEqual(self.graph.entities, {})

    self.graph.add_entity(None)

    self.assertDictEqual(self.graph.entities, {})

  def test_add_entity_when_graph_contains_no_entities(self):
    self.assertDictEqual(self.graph.entities, {})

    new_entity = Entity(1, 'Entity_1')
    self.graph.add_entity(new_entity)

    self.assertDictEqual(self.graph.entities, { 1 : new_entity })
  
  def test_add_entity_when_graph_contains_another_entity(self):
    entity_1 = Entity(1, 'Entity_1')
    self.graph.entities = { 1 : entity_1 }
    self.assertDictEqual(self.graph.entities, { 1 : entity_1 })

    new_entity = Entity(2, 'Entity_2')
    self.graph.add_entity(new_entity)

    self.assertDictEqual(self.graph.entities, { 
      1 : entity_1,
      2 : new_entity
    })

  def test_add_entity_when_graph_contains_another_entity_with_same_id(self):
    old_entity = Entity(1, 'old')
    self.graph.entities = { 1 : old_entity }
    self.assertDictEqual(self.graph.entities, { 1 : old_entity })
    
    new_entity = Entity(1, 'new')
    self.graph.add_entity(new_entity)

    self.assertDictEqual(self.graph.entities, { 1 : new_entity })

  def test_add_entity_sets_next_entity_id(self):
    self.assertEqual(self.graph.next_entity_id, 1)
    new_entity = Entity(1, 'Entity_1')
    self.graph.add_entity(new_entity)

    self.assertEqual(self.graph.next_entity_id, 2)

  def test_add_entity_doesnt_set_next_entity_id_when_added_entity_has_smaller_value(self):
    self.graph.next_entity_id = 3
    self.assertEqual(self.graph.next_entity_id, 3)
    new_entity = Entity(1, 'Entity_1')
    self.graph.add_entity(new_entity)

    self.assertEqual(self.graph.next_entity_id, 3)

class TestGraphCopyAndAddEntity(TestCase):

  def setUp(self):
    self.graph = Graph()
    self.entity_1 = Entity(1, 'E1')
    self.graph.add_entity(self.entity_1)

  def test_copy_and_add_entity(self):
    self.assertDictEqual(self.graph.entities, { 1 : self.entity_1 })
    self.assertEqual(self.graph.next_entity_id, 2)

    self.graph.copy_and_add_entity(self.entity_1)

    self.assertEqual(len(self.graph.entities), 2)
    self.assertEqual(self.graph.entities[2].id, 2)
    self.assertEqual(self.graph.entities[2].name, 'E1')
    self.assertEqual(self.graph.next_entity_id, 3)


class TestGraphLinkEntities(TestCase, AssertEntityMixin):

  def setUp(self):
    self.graph = Graph()
    self.entity_1 = Entity(1, 'E1')
    self.entity_2 = Entity(2, 'E2')
    self.graph.add_entity(self.entity_1)
    self.graph.add_entity(self.entity_2)

  def test_link_entities_when_arguments_are_none(self):
    
    self.graph.link_entities(self.entity_1, None)
    self.graph.link_entities(None, self.entity_2)
    self.graph.link_entities(None, None)

    self.assert_links(self.entity_1)
    self.assert_links(self.entity_2)

  def test_link_entities(self):
    self.graph.link_entities(self.entity_1, self.entity_2)

    self.assert_links(self.entity_1, successors=set([self.entity_2]))
    self.assert_links(self.entity_2, predecessors=set([self.entity_1]))

  def test_link_entities_by_id(self):
    self.graph.link_entities_by_id(1, 2)

    self.assert_links(self.entity_1, successors=set([self.entity_2]))
    self.assert_links(self.entity_2, predecessors=set([self.entity_1]))


class TestGraphFromDict(TestCase, AssertEntityMixin):

  def test_from_dict_when_entities_does_not_exist_in_dict(self):
    graph = Graph.from_dict({
      'links': [{ 'from': 1, 'to': 2 }]
    })
    self.assertDictEqual(graph.entities, {})

  def test_from_dict_when_links_does_not_exist_in_dict(self):
    graph = Graph.from_dict({
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' }
      ]
    })

    self.assertEqual(len(graph.entities), 2)
    self.assertListEqual(list(graph.entities.keys()), [1, 2])
    self.assert_links(graph.entities[1])
    self.assert_links(graph.entities[2])

  def test_from_dict_when_entities_are_linked(self):
    graph = Graph.from_dict({
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' }
      ],
      'links': [
        { 'from': 1, 'to': 2 }
      ]
    })
    e1 = graph.entities[1]
    e2 = graph.entities[2]

    self.assert_links(e1, successors=set([e2]))
    self.assert_links(e2, predecessors=set([e1]))

  def test_from_dict_when_entities_are_linked_in_loop(self):
    graph = Graph.from_dict({
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' },
        { 'entity_id': 3, 'name': 'E3' }
      ],
      'links': [
        { 'from': 1, 'to': 2 },
        { 'from': 2, 'to': 3 },
        { 'from': 3, 'to': 1 }
      ]
    })
    e1 = graph.entities[1]
    e2 = graph.entities[2]
    e3 = graph.entities[3]

    self.assert_links(e1, successors=set([e2]), predecessors=set([e3]))
    self.assert_links(e2, successors=set([e3]), predecessors=set([e1]))
    self.assert_links(e3, successors=set([e1]), predecessors=set([e2]))

  def test_from_dict_when_two_groups_exist(self):
    graph = Graph.from_dict({
      'entities': [
        # Group 1
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' },
        # Group 2
        { 'entity_id': 3, 'name': 'E3' },
        { 'entity_id': 4, 'name': 'E4' },
      ],
      'links': [
        # Group 1
        { 'from': 1, 'to': 2 },
        # Group 2
        { 'from': 3, 'to': 4 },
      ]
    })
    e1 = graph.entities[1]
    e2 = graph.entities[2]
    e3 = graph.entities[3]
    e4 = graph.entities[4]

    self.assert_links(e1, successors=set([e2]))
    self.assert_links(e2, predecessors=set([e1]))
    self.assert_links(e3, successors=set([e4]))
    self.assert_links(e4, predecessors=set([e3]))

def test_from_dict_when_entity_has_multiple_links(self):
    graph = Graph.from_dict({
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' },
        { 'entity_id': 3, 'name': 'E3' }
      ],
      'links': [
        { 'from': 1, 'to': 3 },
        { 'from': 2, 'to': 3 },
      ]
    })
    e1 = graph.entities[1]
    e2 = graph.entities[2]
    e3 = graph.entities[3]

    self.assert_links(e1, successors=set([e3]))
    self.assert_links(e2, successors=set([e3]))
    self.assert_links(e3, predecessors=set([e1, e2]))


class TestGraphToDict(TestCase):

  def test_to_dict_when_no_entities_exist(self):
    graph = Graph()
    json_dict = graph.to_dict()

    self.assertDictEqual(json_dict, {
      'entities': [],
      'links': [],
    })

  def test_to_dict_when_no_links_exist(self):
    graph = Graph()
    e1 = Entity(1, 'E1', 'D1')
    e2 = Entity(2, 'E2')
    graph.add_entity(e1)
    graph.add_entity(e2)
    self.assertDictEqual(graph.entities, { 1: e1, 2: e2 })

    json_dict = graph.to_dict()

    self.assertDictEqual(json_dict, {
      'entities': [
        { 'entity_id': 1, 'name': 'E1', 'description': 'D1' },
        { 'entity_id': 2, 'name': 'E2' }
      ],
      'links': [],
    })
  
  def test_to_dict_when_entities_are_linked(self):
    graph = Graph()
    e1 = Entity(1, 'E1')
    e2 = Entity(2, 'E2')
    graph.add_entity(e1)
    graph.add_entity(e2)
    graph.link_entities(e1, e2)
    self.assertDictEqual(graph.entities, { 1: e1, 2: e2 })

    json_dict = graph.to_dict()

    self.assertDictEqual(json_dict, {
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' }
      ],
      'links': [
        { 'from': 1, 'to': 2 }
      ],
    })

  def test_to_dict_when_entities_are_linked_in_loop(self):
    graph = Graph()
    e1 = Entity(1, 'E1')
    e2 = Entity(2, 'E2')
    graph.add_entity(e1)
    graph.add_entity(e2)
    graph.link_entities(e1, e2)
    graph.link_entities(e2, e1)
    self.assertDictEqual(graph.entities, { 1: e1, 2: e2 })

    json_dict = graph.to_dict()

    self.assertDictEqual(json_dict, {
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' }
      ],
      'links': [
        { 'from': 1, 'to': 2 },
        { 'from': 2, 'to': 1 }
      ],
    })

  def test_to_dict_when_entity_has_multiple_links(self):
    graph = Graph()
    e1 = Entity(1, 'E1')
    e2 = Entity(2, 'E2')
    e3 = Entity(3, 'E3')
    graph.add_entity(e1)
    graph.add_entity(e2)
    graph.add_entity(e3)
    graph.link_entities(e1, e3)
    graph.link_entities(e2, e3)
    self.assertDictEqual(graph.entities, { 1: e1, 2: e2, 3: e3 })

    json_dict = graph.to_dict()

    self.assertDictEqual(json_dict, {
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' },
        { 'entity_id': 3, 'name': 'E3' }
      ],
      'links': [
        { 'from': 1, 'to': 3 },
        { 'from': 2, 'to': 3 }
      ],
    })


class TestGraphClone(TestCase):

  def test_graph_clone_when_graph_is_empty(self):
    graph = Graph.from_dict({})
    graph.clone(1)
    self.assertDictEqual(graph.to_dict(), {
      'entities': [],
      'links': []
    })

  def test_graph_clone_when_provided_id_doesnt_exist_in_graph(self):
    input_dict = {
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' }
      ],
      'links': [
        { 'from': 1, 'to': 2 }
      ]
    }
    graph = Graph.from_dict(input_dict)
    graph.clone(3)
    self.assertDictEqual(graph.to_dict(), input_dict)

  def test_graph_clone_when_provided_id_exists_in_graph(self):
    graph = Graph.from_dict({
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2', 'description': 'test' }
      ],
      'links': [
        { 'from': 1, 'to': 2 }
      ]
    })
    graph.clone(2)

    self.assertDictEqual(graph.to_dict(), {
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2', 'description': 'test' },
        { 'entity_id': 3, 'name': 'E2', 'description': 'test' },
      ],
      'links': [
        { 'from': 1, 'to': 2 },
        { 'from': 1, 'to': 3 },
      ]
    })

  def test_graph_clone_when_provided_entity_is_isolated(self):
    graph = Graph.from_dict({
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' },
        { 'entity_id': 3, 'name': 'E3' },
      ],
      'links': [
        { 'from': 1, 'to': 2 }
      ]
    })
    graph.clone(3)

    self.assertDictEqual(graph.to_dict(), {
      'entities': [
        { 'entity_id': 1, 'name': 'E1' },
        { 'entity_id': 2, 'name': 'E2' },
        { 'entity_id': 3, 'name': 'E3' },
        { 'entity_id': 4, 'name': 'E3' },
      ],
      'links': [
        { 'from': 1, 'to': 2 },
      ]
    })
