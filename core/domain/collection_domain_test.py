# coding: utf-8
#
# Copyright 2015 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for collection domain objects and methods defined on them."""

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime

from constants import constants
from core.domain import collection_domain
from core.domain import collection_services
from core.tests import test_utils
import feconf
import python_utils
import utils

# Dictionary-like data structures within sample YAML must be formatted
# alphabetically to match string equivalence with the YAML generation
# methods tested below.
#
# If evaluating differences in YAML, conversion to dict form via
# utils.dict_from_yaml can isolate differences quickly.

SAMPLE_YAML_CONTENT = (
    """category: A category
language_code: en
nodes:
- exploration_id: an_exploration_id
objective: An objective
schema_version: %d
tags: []
title: A title
""") % (feconf.CURRENT_COLLECTION_SCHEMA_VERSION)


class CollectionChangeTests(test_utils.GenericTestBase):

    def test_collection_change_object_with_missing_cmd(self):
        with self.assertRaisesRegexp(
            utils.ValidationError, 'Missing cmd key in change dict'):
            collection_domain.CollectionChange({'invalid': 'data'})

    def test_collection_change_object_with_invalid_cmd(self):
        with self.assertRaisesRegexp(
            utils.ValidationError, 'Command invalid is not allowed'):
            collection_domain.CollectionChange({'cmd': 'invalid'})

    def test_collection_change_object_with_missing_attribute_in_cmd(self):
        with self.assertRaisesRegexp(
            utils.ValidationError, (
                'The following required attributes are missing: '
                'exploration_id, new_value')):
            collection_domain.CollectionChange({
                'cmd': 'edit_collection_node_property',
                'property_name': 'category',
                'old_value': 'old_value'
            })

    def test_collection_change_object_with_extra_attribute_in_cmd(self):
        with self.assertRaisesRegexp(
            utils.ValidationError, (
                'The following extra attributes are present: invalid')):
            collection_domain.CollectionChange({
                'cmd': 'edit_collection_node_property',
                'exploration_id': 'exploration_id',
                'property_name': 'category',
                'old_value': 'old_value',
                'new_value': 'new_value',
                'invalid': 'invalid'
            })

    def test_collection_change_object_with_invalid_collection_property(self):
        with self.assertRaisesRegexp(
            utils.ValidationError, (
                'Value for property_name in cmd edit_collection_property: '
                'invalid is not allowed')):
            collection_domain.CollectionChange({
                'cmd': 'edit_collection_property',
                'property_name': 'invalid',
                'old_value': 'old_value',
                'new_value': 'new_value',
            })

    def test_collection_change_object_with_create_new(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'create_new',
            'category': 'category',
            'title': 'title'
        })

        self.assertEqual(col_change_object.cmd, 'create_new')
        self.assertEqual(col_change_object.category, 'category')
        self.assertEqual(col_change_object.title, 'title')

    def test_collection_change_object_with_add_collection_node(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'add_collection_node',
            'exploration_id': 'exploration_id',
        })

        self.assertEqual(col_change_object.cmd, 'add_collection_node')
        self.assertEqual(col_change_object.exploration_id, 'exploration_id')

    def test_collection_change_object_with_delete_collection_node(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'delete_collection_node',
            'exploration_id': 'exploration_id',
        })

        self.assertEqual(col_change_object.cmd, 'delete_collection_node')
        self.assertEqual(col_change_object.exploration_id, 'exploration_id')

    def test_collection_change_object_with_swap_nodes(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'swap_nodes',
            'first_index': 'first_index',
            'second_index': 'second_index'
        })

        self.assertEqual(col_change_object.cmd, 'swap_nodes')
        self.assertEqual(col_change_object.first_index, 'first_index')
        self.assertEqual(col_change_object.second_index, 'second_index')

    def test_collection_change_object_with_edit_collection_property(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'edit_collection_property',
            'property_name': 'category',
            'new_value': 'new_value',
            'old_value': 'old_value'
        })

        self.assertEqual(col_change_object.cmd, 'edit_collection_property')
        self.assertEqual(col_change_object.property_name, 'category')
        self.assertEqual(col_change_object.new_value, 'new_value')
        self.assertEqual(col_change_object.old_value, 'old_value')

    def test_collection_change_object_with_edit_collection_node_property(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'edit_collection_node_property',
            'exploration_id': 'exploration_id',
            'property_name': 'title',
            'new_value': 'new_value',
            'old_value': 'old_value'
        })

        self.assertEqual(col_change_object.cmd, 'edit_collection_node_property')
        self.assertEqual(col_change_object.exploration_id, 'exploration_id')
        self.assertEqual(col_change_object.property_name, 'title')
        self.assertEqual(col_change_object.new_value, 'new_value')
        self.assertEqual(col_change_object.old_value, 'old_value')

    def test_collection_change_object_with_migrate_schema_to_latest_version(
            self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'migrate_schema_to_latest_version',
            'from_version': 'from_version',
            'to_version': 'to_version',
        })

        self.assertEqual(
            col_change_object.cmd, 'migrate_schema_to_latest_version')
        self.assertEqual(col_change_object.from_version, 'from_version')
        self.assertEqual(col_change_object.to_version, 'to_version')

    def test_collection_change_object_with_add_collection_skill(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'add_collection_skill',
            'name': 'name'
        })

        self.assertEqual(col_change_object.cmd, 'add_collection_skill')
        self.assertEqual(col_change_object.name, 'name')

    def test_collection_change_object_with_delete_collection_skill(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'delete_collection_skill',
            'skill_id': 'skill_id'
        })

        self.assertEqual(col_change_object.cmd, 'delete_collection_skill')
        self.assertEqual(col_change_object.skill_id, 'skill_id')

    def test_collection_change_object_with_add_question_id_to_skill(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'add_question_id_to_skill',
            'skill_id': 'skill_id',
            'question_id': 'question_id'
        })

        self.assertEqual(col_change_object.cmd, 'add_question_id_to_skill')
        self.assertEqual(col_change_object.skill_id, 'skill_id')
        self.assertEqual(col_change_object.question_id, 'question_id')

    def test_collection_change_object_with_remove_question_id_from_skill(self):
        col_change_object = collection_domain.CollectionChange({
            'cmd': 'remove_question_id_from_skill',
            'skill_id': 'skill_id',
            'question_id': 'question_id'
        })

        self.assertEqual(col_change_object.cmd, 'remove_question_id_from_skill')
        self.assertEqual(col_change_object.skill_id, 'skill_id')
        self.assertEqual(col_change_object.question_id, 'question_id')

    def test_to_dict(self):
        col_change_dict = {
            'cmd': 'remove_question_id_from_skill',
            'skill_id': 'skill_id',
            'question_id': 'question_id'
        }
        col_change_object = collection_domain.CollectionChange(col_change_dict)
        self.assertEqual(col_change_object.to_dict(), col_change_dict)


class CollectionDomainUnitTests(test_utils.GenericTestBase):
    """Test the collection domain object."""

    COLLECTION_ID = 'collection_id'
    EXPLORATION_ID = 'exp_id_0'

    def setUp(self):
        super(CollectionDomainUnitTests, self).setUp()
        self.save_new_valid_collection(
            self.COLLECTION_ID, 'user@example.com', title='Title',
            category='Category', objective='Objective',
            exploration_id=self.EXPLORATION_ID)
        self.collection = collection_services.get_collection_by_id(
            self.COLLECTION_ID)

    def _assert_validation_error(self, expected_error_substring):
        """Checks that the collection passes strict validation."""
        with self.assertRaisesRegexp(
            utils.ValidationError, expected_error_substring):
            self.collection.validate()

    def test_initial_validation(self):
        """Test validating a new, valid collection."""
        self.collection.validate()

    def test_title_validation(self):
        self.collection.title = 0
        self._assert_validation_error('Expected title to be a string')

    def test_category_validation(self):
        self.collection.category = 0
        self._assert_validation_error('Expected category to be a string')

    def test_objective_validation(self):
        self.collection.objective = ''
        self._assert_validation_error('objective must be specified')

        self.collection.objective = 0
        self._assert_validation_error('Expected objective to be a string')

    def test_language_code_validation(self):
        self.collection.language_code = ''
        self._assert_validation_error('language must be specified')

        self.collection.language_code = 0
        self._assert_validation_error('Expected language code to be a string')

        self.collection.language_code = 'xz'
        self._assert_validation_error('Invalid language code')

    def test_tags_validation(self):
        self.collection.tags = 'abc'
        self._assert_validation_error('Expected tags to be a list')

        self.collection.tags = [2, 3]
        self._assert_validation_error('Expected each tag to be a string')

        self.collection.tags = ['', 'tag']
        self._assert_validation_error('Tags should be non-empty')

        self.collection.tags = ['234']
        self._assert_validation_error(
            'Tags should only contain lowercase letters and spaces')

        self.collection.tags = ['   abc']
        self._assert_validation_error(
            'Tags should not start or end with whitespace')

        self.collection.tags = ['abc  def']
        self._assert_validation_error(
            'Adjacent whitespace in tags should be collapsed')

        self.collection.tags = ['abc', 'abc']
        self._assert_validation_error(
            'Expected tags to be unique, but found duplicates')

    def test_schema_version_validation(self):
        self.collection.schema_version = 'some_schema_version'
        self._assert_validation_error('Expected schema version to be an int')

        self.collection.schema_version = 100
        self._assert_validation_error(
            'Expected schema version to be %s' %
            feconf.CURRENT_COLLECTION_SCHEMA_VERSION)

    def test_nodes_validation(self):
        self.collection.nodes = {}
        self._assert_validation_error('Expected nodes to be a list')

        self.collection.nodes = [
            collection_domain.CollectionNode.from_dict({
                'exploration_id': '0'
            }),
            collection_domain.CollectionNode.from_dict({
                'exploration_id': '0'
            })
        ]

        self._assert_validation_error(
            'There are explorations referenced in the collection more than '
            'once.')

    def test_initial_explorations_validation(self):
        # Having no collection nodes is fine for non-strict validation.
        self.collection.nodes = []
        self.collection.validate(strict=False)

        # But it's not okay for strict validation.
        self._assert_validation_error(
            'Expected to have at least 1 exploration in the collection.')

    def test_metadata_validation(self):
        self.collection.title = ''
        self.collection.objective = ''
        self.collection.category = ''
        self.collection.nodes = []

        # Having no title is fine for non-strict validation.
        self.collection.validate(strict=False)
        # But it's not okay for strict validation.
        self._assert_validation_error(
            'A title must be specified for the collection.')
        self.collection.title = 'A title'

        # Having no objective is fine for non-strict validation.
        self.collection.validate(strict=False)
        # But it's not okay for strict validation.
        self._assert_validation_error(
            'An objective must be specified for the collection.')
        self.collection.objective = 'An objective'

        # Having no category is fine for non-strict validation.
        self.collection.validate(strict=False)
        # But it's not okay for strict validation.
        self._assert_validation_error(
            'A category must be specified for the collection.')
        self.collection.category = 'A category'

        # Having no exploration is fine for non-strict validation.
        self.collection.validate(strict=False)
        # But it's not okay for strict validation.
        self._assert_validation_error(
            'Expected to have at least 1 exploration in the collection.')
        self.collection.add_node('exp_id_1')

        # Now the collection passes both strict and non-strict validation.
        self.collection.validate(strict=False)
        self.collection.validate(strict=True)

    def test_collection_node_exploration_id_validation(self):
        # Validate CollectionNode's exploration_id.
        collection_node0 = self.collection.get_node('exp_id_0')
        collection_node0.exploration_id = 2
        self._assert_validation_error('Expected exploration ID to be a string')

    def test_is_demo_property(self):
        """Test the is_demo property."""
        demo = collection_domain.Collection.create_default_collection('0')
        self.assertEqual(demo.is_demo, True)

        notdemo1 = collection_domain.Collection.create_default_collection('a')
        self.assertEqual(notdemo1.is_demo, False)

        notdemo2 = collection_domain.Collection.create_default_collection(
            'abcd')
        self.assertEqual(notdemo2.is_demo, False)

    def test_collection_export_import(self):
        """Test that to_dict and from_dict preserve all data within an
        collection.
        """
        self.save_new_valid_exploration(
            '0', 'user@example.com', end_state_name='End')
        collection = collection_domain.Collection.create_default_collection(
            '0', title='title', category='category', objective='objective')
        collection_dict = collection.to_dict()
        collection_from_dict = collection_domain.Collection.from_dict(
            collection_dict)
        self.assertEqual(collection_from_dict.to_dict(), collection_dict)

    def test_add_delete_swap_nodes(self):
        """Test that add_node, delete_node and swap_nodes fail in the correct
        situations.
        """
        collection = collection_domain.Collection.create_default_collection(
            '0')
        self.assertEqual(len(collection.nodes), 0)

        collection.add_node('test_exp')
        self.assertEqual(len(collection.nodes), 1)

        with self.assertRaisesRegexp(
            ValueError,
            'Exploration is already part of this collection: test_exp'
            ):
            collection.add_node('test_exp')

        collection.add_node('another_exp')
        self.assertEqual(len(collection.nodes), 2)

        collection.swap_nodes(0, 1)
        self.assertEqual(collection.nodes[0].exploration_id, 'another_exp')
        self.assertEqual(collection.nodes[1].exploration_id, 'test_exp')
        with self.assertRaisesRegexp(
            ValueError,
            'Both indices point to the same collection node.'
            ):
            collection.swap_nodes(0, 0)

        collection.delete_node('another_exp')
        self.assertEqual(len(collection.nodes), 1)

        with self.assertRaisesRegexp(
            ValueError,
            'Exploration is not part of this collection: another_exp'
            ):
            collection.delete_node('another_exp')

        collection.delete_node('test_exp')
        self.assertEqual(len(collection.nodes), 0)

    def test_update_collection_contents_from_model(self):
        versioned_collection_contents = {
            'schema_version': 1,
            'collection_contents': {}
        }

        collection_domain.Collection.update_collection_contents_from_model(
            versioned_collection_contents, 1)

        self.assertEqual(versioned_collection_contents['schema_version'], 2)
        self.assertEqual(
            versioned_collection_contents['collection_contents'], {})

    def test_update_collection_contents_from_model_with_invalid_schema_version(
            self):
        versioned_collection_contents = {
            'schema_version': feconf.CURRENT_COLLECTION_SCHEMA_VERSION,
            'collection_contents': {}
        }

        with self.assertRaisesRegexp(
            Exception,
            'Collection is version .+ but current collection schema version '
            'is %d' % feconf.CURRENT_COLLECTION_SCHEMA_VERSION):
            collection_domain.Collection.update_collection_contents_from_model(
                versioned_collection_contents,
                feconf.CURRENT_COLLECTION_SCHEMA_VERSION)

    def test_serialize_and_deserialize_returns_unchanged_collection(self):
        """Checks that serializing and then deserializing a default collection
        works as intended by leaving the collection unchanged.
        """
        self.assertEqual(
            self.collection.to_dict(),
            collection_domain.Collection.deserialize(
                self.collection.serialize()).to_dict())


class ExplorationGraphUnitTests(test_utils.GenericTestBase):
    """Test the general structure of explorations within a collection."""

    def test_initial_explorations(self):
        """Any exploration without prerequisites should be an initial
        exploration.
        """
        collection = collection_domain.Collection.create_default_collection(
            'collection_id')

        # If there are no explorations in the collection, there can be no
        # initial explorations.
        self.assertEqual(collection.nodes, [])
        self.assertEqual(collection.first_exploration_id, None)

        # A freshly added exploration will be an initial one.
        collection.add_node('exp_id_0')
        self.assertEqual(collection.first_exploration_id, 'exp_id_0')

        # Having prerequisites will make an exploration no longer initial.
        collection.add_node('exp_id_1')
        self.assertEqual(len(collection.nodes), 2)
        self.assertEqual(collection.first_exploration_id, 'exp_id_0')

    def test_next_explorations(self):
        """Explorations should be suggested based on their index in the node
           list.
        """
        collection = collection_domain.Collection.create_default_collection(
            'collection_id')

        # There should be no next explorations for an empty collection.
        self.assertEqual(collection.get_next_exploration_id([]), None)

        # If a new exploration is added, the next exploration IDs should be the
        # same as the initial exploration.
        collection.add_node('exp_id_0')
        self.assertEqual(collection.get_next_exploration_id([]), 'exp_id_0')
        self.assertEqual(
            collection.first_exploration_id,
            collection.get_next_exploration_id([]))

        # Completing the only exploration of the collection should lead to no
        # available explorations thereafter.
        self.assertEqual(
            collection.get_next_exploration_id(['exp_id_0']), None)

        # If another exploration has been added, then the first exploration
        # should be the next one to complete.
        collection.add_node('exp_id_1')
        self.assertEqual(collection.get_next_exploration_id(
            ['exp_id_0']), 'exp_id_1')

        # If another exploration is added, then based on explorations
        # completed, the correct exploration should be shown as the next one.
        collection.add_node('exp_id_2')
        self.assertEqual(
            collection.get_next_exploration_id([]), 'exp_id_0')
        self.assertEqual(
            collection.get_next_exploration_id(['exp_id_0']), 'exp_id_1')
        self.assertEqual(
            collection.get_next_exploration_id(['exp_id_0', 'exp_id_1']),
            'exp_id_2')

        # If all explorations have been completed, none should be suggested.
        self.assertEqual(
            collection.get_next_exploration_id(
                ['exp_id_0', 'exp_id_1', 'exp_id_2']), None)

    def test_next_explorations_in_sequence(self):
        collection = collection_domain.Collection.create_default_collection(
            'collection_id')
        exploration_id = 'exp_id_0'
        collection.add_node(exploration_id)

        # Completing the only exploration of the collection should lead to no
        # available explorations thereafter.
        self.assertEqual(
            collection.get_next_exploration_id_in_sequence(exploration_id),
            None)

        collection.add_node('exp_id_1')
        collection.add_node('exp_id_2')
        self.assertEqual(
            collection.get_next_exploration_id_in_sequence(exploration_id),
            'exp_id_1')

        self.assertEqual(
            collection.get_next_exploration_id_in_sequence('exp_id_1'),
            'exp_id_2')

    def test_nodes_are_in_playble_order(self):
        # Create collection.
        collection = collection_domain.Collection.create_default_collection(
            'collection_id')

        # There should be an empty node list in playable order for an empty
        # collection.
        self.assertEqual(collection.nodes, [])

        # Add nodes to collection.
        collection.add_node('exp_id_0')
        collection.add_node('exp_id_1')
        collection.add_node('exp_id_2')

        sorted_nodes = collection.nodes
        expected_explorations_ids = ['exp_id_0', 'exp_id_1', 'exp_id_2']
        observed_exploration_ids = [
            node.exploration_id for node in sorted_nodes]

        self.assertEqual(expected_explorations_ids, observed_exploration_ids)

    def test_next_explorations_with_invalid_exploration_ids(self):
        collection = collection_domain.Collection.create_default_collection(
            'collection_id')
        collection.add_node('exp_id_1')

        # There should be one suggested exploration to complete by default.
        self.assertEqual(collection.get_next_exploration_id([]), 'exp_id_1')

        # If an invalid exploration ID is passed to get_next_exploration_id(),
        # it should be ignored. This tests the situation where an exploration
        # is deleted from a collection after being completed by a user.
        self.assertEqual(
            collection.get_next_exploration_id(['fake_exp_id']), 'exp_id_1')


class YamlCreationUnitTests(test_utils.GenericTestBase):
    """Test creation of collections from YAML files."""

    COLLECTION_ID = 'a_collection_id'
    EXPLORATION_ID = 'an_exploration_id'

    def test_yaml_import_and_export(self):
        """Test the from_yaml() and to_yaml() methods."""
        self.save_new_valid_exploration(
            self.EXPLORATION_ID, 'user@example.com', end_state_name='End')

        collection = collection_domain.Collection.create_default_collection(
            self.COLLECTION_ID, title='A title', category='A category',
            objective='An objective')
        collection.add_node(self.EXPLORATION_ID)
        self.assertEqual(len(collection.nodes), 1)

        collection.validate()

        yaml_content = collection.to_yaml()
        self.assertEqual(yaml_content, SAMPLE_YAML_CONTENT)

        collection2 = collection_domain.Collection.from_yaml(
            'collection2', yaml_content)
        self.assertEqual(len(collection2.nodes), 1)
        yaml_content_2 = collection2.to_yaml()
        self.assertEqual(yaml_content_2, yaml_content)

        # Should not be able to create a collection from no YAML content.
        with self.assertRaisesRegexp(
            utils.InvalidInputException,
            'Please ensure that you are uploading a YAML text file, '
            'not a zip file. The YAML parser returned the following error: '
        ):
            collection_domain.Collection.from_yaml('collection3', '')

    def test_from_yaml_with_no_schema_version_specified_raises_error(self):
        collection = collection_domain.Collection(
            self.COLLECTION_ID, 'title', 'category', 'objective', 'en', [],
            None, [], 0)

        yaml_content = collection.to_yaml()

        with self.assertRaisesRegexp(
            Exception, 'Invalid YAML file: no schema version specified.'):
            collection_domain.Collection.from_yaml(
                self.COLLECTION_ID, yaml_content)

    def test_from_yaml_with_invalid_schema_version_raises_error(self):
        collection = collection_domain.Collection(
            self.COLLECTION_ID, 'title', 'category', 'objective', 'en', [],
            0, [], 0)

        yaml_content = collection.to_yaml()

        with self.assertRaisesRegexp(
            Exception,
            'Sorry, we can only process v1 to .+ collection YAML files at '
            'present.'):
            collection_domain.Collection.from_yaml(
                self.COLLECTION_ID, yaml_content)


class SchemaMigrationMethodsUnitTests(test_utils.GenericTestBase):
    """Tests the presence of appropriate schema migration methods in the
    Collection domain object class.
    """

    def test_correct_collection_contents_schema_conversion_methods_exist(self):
        """Test that the right collection_contents schema conversion methods
        exist.
        """
        current_collection_schema_version = (
            feconf.CURRENT_COLLECTION_SCHEMA_VERSION)
        for version_num in python_utils.RANGE(
                1, current_collection_schema_version):
            self.assertTrue(hasattr(
                collection_domain.Collection,
                '_convert_collection_contents_v%s_dict_to_v%s_dict' % (
                    version_num, version_num + 1)))

        self.assertFalse(hasattr(
            collection_domain.Collection,
            '_convert_collection_contents_v%s_dict_to_v%s_dict' % (
                current_collection_schema_version,
                current_collection_schema_version + 1)))

    def test_correct_collection_schema_conversion_methods_exist(self):
        """Test that the right collection schema conversion methods exist."""
        current_collection_schema_version = (
            feconf.CURRENT_COLLECTION_SCHEMA_VERSION)

        for version_num in python_utils.RANGE(
                1, current_collection_schema_version):
            self.assertTrue(hasattr(
                collection_domain.Collection,
                '_convert_v%s_dict_to_v%s_dict' % (
                    version_num, version_num + 1)))

        self.assertFalse(hasattr(
            collection_domain.Collection,
            '_convert_v%s_dict_to_v%s_dict' % (
                current_collection_schema_version,
                current_collection_schema_version + 1)))


class SchemaMigrationUnitTests(test_utils.GenericTestBase):
    """Test migration methods for yaml content."""

    YAML_CONTENT_V1 = (
        """category: A category
nodes:
- acquired_skills:
  - Skill1
  - Skill2
  exploration_id: Exp1
  prerequisite_skills: []
- acquired_skills: []
  exploration_id: Exp2
  prerequisite_skills:
  - Skill1
objective: ''
schema_version: 1
title: A title
""")
    YAML_CONTENT_V2 = (
        """category: A category
language_code: en
nodes:
- acquired_skills:
  - Skill1
  - Skill2
  exploration_id: Exp1
  prerequisite_skills: []
- acquired_skills: []
  exploration_id: Exp2
  prerequisite_skills:
  - Skill1
objective: ''
schema_version: 2
tags: []
title: A title
""")
    YAML_CONTENT_V3 = (
        """category: A category
language_code: en
nodes:
- acquired_skills:
  - Skill1
  - Skill2
  exploration_id: Exp1
  prerequisite_skills: []
- acquired_skills: []
  exploration_id: Exp2
  prerequisite_skills:
  - Skill1
objective: ''
schema_version: 2
tags: []
title: A title
""")
    YAML_CONTENT_V4 = (
        """category: A category
language_code: en
next_skill_id: 2
nodes:
- acquired_skill_ids:
  - skill0
  - skill1
  exploration_id: Exp1
  prerequisite_skill_ids: []
- acquired_skill_ids: []
  exploration_id: Exp2
  prerequisite_skill_ids:
  - skill0
objective: ''
schema_version: 4
skills:
  skill0:
    name: Skill1
    question_ids: []
  skill1:
    name: Skill2
    question_ids: []
tags: []
title: A title
""")
    YAML_CONTENT_V5 = (
        """category: A category
language_code: en
next_skill_index: 2
nodes:
- acquired_skill_ids:
  - skill0
  - skill1
  exploration_id: Exp1
  prerequisite_skill_ids: []
- acquired_skill_ids: []
  exploration_id: Exp2
  prerequisite_skill_ids:
  - skill0
objective: ''
schema_version: 5
skills:
  skill0:
    name: Skill1
    question_ids: []
  skill1:
    name: Skill2
    question_ids: []
tags: []
title: A title
""")
    YAML_CONTENT_V6 = (
        """category: A category
language_code: en
nodes:
- exploration_id: Exp1
- exploration_id: Exp2
objective: ''
schema_version: 6
tags: []
title: A title
""")

    _LATEST_YAML_CONTENT = YAML_CONTENT_V6

    def test_load_from_v1(self):
        """Test direct loading from a v1 yaml file."""
        self.save_new_valid_exploration(
            'Exp1', 'user@example.com', end_state_name='End')
        collection = collection_domain.Collection.from_yaml(
            'cid', self.YAML_CONTENT_V1)
        self.assertEqual(collection.to_yaml(), self._LATEST_YAML_CONTENT)

    def test_load_from_v2(self):
        """Test direct loading from a v2 yaml file."""
        self.save_new_valid_exploration(
            'Exp1', 'user@example.com', end_state_name='End')
        collection = collection_domain.Collection.from_yaml(
            'cid', self.YAML_CONTENT_V2)
        self.assertEqual(collection.to_yaml(), self._LATEST_YAML_CONTENT)

    def test_load_from_v3(self):
        """Test direct loading from a v3 yaml file."""
        self.save_new_valid_exploration(
            'Exp1', 'user@example.com', end_state_name='End')
        collection = collection_domain.Collection.from_yaml(
            'cid', self.YAML_CONTENT_V3)
        self.assertEqual(collection.to_yaml(), self._LATEST_YAML_CONTENT)

    def test_load_from_v4(self):
        """Test direct loading from a v4 yaml file."""
        self.save_new_valid_exploration(
            'Exp1', 'user@example.com', end_state_name='End')
        collection = collection_domain.Collection.from_yaml(
            'cid', self.YAML_CONTENT_V4)
        self.assertEqual(collection.to_yaml(), self._LATEST_YAML_CONTENT)

    def test_load_from_v5(self):
        """Test direct loading from a v5 yaml file."""
        self.save_new_valid_exploration(
            'Exp1', 'user@example.com', end_state_name='End')
        collection = collection_domain.Collection.from_yaml(
            'cid', self.YAML_CONTENT_V5)
        self.assertEqual(collection.to_yaml(), self._LATEST_YAML_CONTENT)

    def test_load_from_v6(self):
        """Test direct loading from a v6 yaml file."""
        self.save_new_valid_exploration(
            'Exp1', 'user@example.com', end_state_name='End')
        collection = collection_domain.Collection.from_yaml(
            'cid', self.YAML_CONTENT_V6)
        self.assertEqual(collection.to_yaml(), self._LATEST_YAML_CONTENT)


class CollectionSummaryTests(test_utils.GenericTestBase):

    def setUp(self):
        super(CollectionSummaryTests, self).setUp()
        current_time = datetime.datetime.utcnow()
        self.collection_summary_dict = {
            'category': 'category',
            'status': constants.ACTIVITY_STATUS_PRIVATE,
            'community_owned': True,
            'viewer_ids': ['viewer_id'],
            'version': 1,
            'editor_ids': ['editor_id'],
            'title': 'title',
            'collection_model_created_on': current_time,
            'tags': [],
            'collection_model_last_updated': current_time,
            'contributor_ids': ['contributor_id'],
            'language_code': 'en',
            'objective': 'objective',
            'contributors_summary': {},
            'id': 'col_id',
            'owner_ids': ['owner_id']
        }

        self.collection_summary = collection_domain.CollectionSummary(
            'col_id', 'title', 'category', 'objective', 'en', [],
            constants.ACTIVITY_STATUS_PRIVATE, True, ['owner_id'],
            ['editor_id'], ['viewer_id'], ['contributor_id'], {}, 1, 1,
            current_time, current_time)

    def test_collection_summary_gets_created(self):
        self.assertEqual(
            self.collection_summary.to_dict(), self.collection_summary_dict)

    def test_validation_passes_with_valid_properties(self):
        self.collection_summary.validate()

    def test_validation_fails_with_invalid_title(self):
        self.collection_summary.title = 0
        with self.assertRaisesRegexp(
            utils.ValidationError, 'Expected title to be a string, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_category(self):
        self.collection_summary.category = 0
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected category to be a string, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_objective(self):
        self.collection_summary.objective = 0
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected objective to be a string, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_missing_language_code(self):
        self.collection_summary.language_code = None
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'A language must be specified \\(in the \'Settings\' tab\\).'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_language_code(self):
        self.collection_summary.language_code = 1
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected language code to be a string, received 1'):
            self.collection_summary.validate()

    def test_validation_fails_with_unallowed_language_code(self):
        self.collection_summary.language_code = 'invalid'
        with self.assertRaisesRegexp(
            utils.ValidationError, 'Invalid language code: invalid'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_tags(self):
        self.collection_summary.tags = 'tags'
        with self.assertRaisesRegexp(
            utils.ValidationError, 'Expected tags to be a list, received tags'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_tag_in_tags(self):
        self.collection_summary.tags = ['tag', 2]
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected each tag to be a string, received \'2\''):
            self.collection_summary.validate()

    def test_validation_fails_with_empty_tag_in_tags(self):
        self.collection_summary.tags = ['', 'abc']
        with self.assertRaisesRegexp(
            utils.ValidationError, 'Tags should be non-empty'):
            self.collection_summary.validate()

    def test_validation_fails_with_unallowed_characters_in_tag(self):
        self.collection_summary.tags = ['123', 'abc']
        with self.assertRaisesRegexp(
            utils.ValidationError, (
                'Tags should only contain lowercase '
                'letters and spaces, received \'123\'')):
            self.collection_summary.validate()

    def test_validation_fails_with_whitespace_in_tag_start(self):
        self.collection_summary.tags = [' ab', 'abc']
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Tags should not start or end with whitespace, received \' ab\''):
            self.collection_summary.validate()

    def test_validation_fails_with_whitespace_in_tag_end(self):
        self.collection_summary.tags = ['ab ', 'abc']
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Tags should not start or end with whitespace, received \'ab \''):
            self.collection_summary.validate()

    def test_validation_fails_with_adjacent_whitespace_in_tag(self):
        self.collection_summary.tags = ['a   b', 'abc']
        with self.assertRaisesRegexp(
            utils.ValidationError, (
                'Adjacent whitespace in tags should '
                'be collapsed, received \'a   b\'')):
            self.collection_summary.validate()

    def test_validation_fails_with_duplicate_tags(self):
        self.collection_summary.tags = ['abc', 'abc', 'ab']
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected tags to be unique, but found duplicates'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_status(self):
        self.collection_summary.status = 0
        with self.assertRaisesRegexp(
            utils.ValidationError, 'Expected status to be string, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_community_owned(self):
        self.collection_summary.community_owned = 0
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected community_owned to be bool, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_contributors_summary(self):
        self.collection_summary.contributors_summary = 0
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected contributors_summary to be dict, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_owner_ids_type(self):
        self.collection_summary.owner_ids = 0
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected owner_ids to be list, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_owner_id_in_owner_ids(self):
        self.collection_summary.owner_ids = ['1', 2, '3']
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected each id in owner_ids to be string, received 2'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_editor_ids_type(self):
        self.collection_summary.editor_ids = 0
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected editor_ids to be list, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_editor_id_in_editor_ids(self):
        self.collection_summary.editor_ids = ['1', 2, '3']
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected each id in editor_ids to be string, received 2'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_viewer_ids_type(self):
        self.collection_summary.viewer_ids = 0
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected viewer_ids to be list, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_viewer_id_in_viewer_ids(self):
        self.collection_summary.viewer_ids = ['1', 2, '3']
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected each id in viewer_ids to be string, received 2'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_contributor_ids_type(self):
        self.collection_summary.contributor_ids = 0
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected contributor_ids to be list, received 0'):
            self.collection_summary.validate()

    def test_validation_fails_with_invalid_contributor_id_in_contributor_ids(
            self):
        self.collection_summary.contributor_ids = ['1', 2, '3']
        with self.assertRaisesRegexp(
            utils.ValidationError,
            'Expected each id in contributor_ids to be string, received 2'):
            self.collection_summary.validate()

    def test_is_private(self):
        self.assertTrue(self.collection_summary.is_private())
        self.collection_summary = collection_domain.CollectionSummary(
            'col_id', 'title', 'category', 'objective', 'en', [],
            constants.ACTIVITY_STATUS_PUBLIC, True, ['owner_id'],
            ['editor_id'], ['viewer_id'], ['contributor_id'], {}, 1, 1,
            datetime.datetime.utcnow(), datetime.datetime.utcnow())
        self.assertFalse(self.collection_summary.is_private())

    def test_is_solely_owned_by_user_one_owner(self):
        self.assertTrue(
            self.collection_summary.is_solely_owned_by_user('owner_id'))
        self.assertFalse(
            self.collection_summary.is_solely_owned_by_user('other_id'))
        self.collection_summary = collection_domain.CollectionSummary(
            'col_id', 'title', 'category', 'objective', 'en', [],
            constants.ACTIVITY_STATUS_PUBLIC, True, ['other_id'],
            ['editor_id'], ['viewer_id'], ['contributor_id'], {}, 1, 1,
            datetime.datetime.utcnow(), datetime.datetime.utcnow())
        self.assertFalse(
            self.collection_summary.is_solely_owned_by_user('owner_id'))
        self.assertTrue(
            self.collection_summary.is_solely_owned_by_user('other_id'))

    def test_is_solely_owned_by_user_multiple_owners(self):
        self.assertTrue(
            self.collection_summary.is_solely_owned_by_user('owner_id'))
        self.assertFalse(
            self.collection_summary.is_solely_owned_by_user('other_id'))
        self.collection_summary = collection_domain.CollectionSummary(
            'col_id', 'title', 'category', 'objective', 'en', [],
            constants.ACTIVITY_STATUS_PUBLIC, True, ['owner_id', 'other_id'],
            ['editor_id'], ['viewer_id'], ['contributor_id'], {}, 1, 1,
            datetime.datetime.utcnow(), datetime.datetime.utcnow())
        self.assertFalse(
            self.collection_summary.is_solely_owned_by_user('owner_id'))
        self.assertFalse(
            self.collection_summary.is_solely_owned_by_user('other_id'))

    def test_is_solely_owned_by_user_other_users(self):
        self.assertFalse(
            self.collection_summary.is_solely_owned_by_user('editor_id'))
        self.assertFalse(
            self.collection_summary.is_solely_owned_by_user('viewer_id'))
        self.assertFalse(
            self.collection_summary.is_solely_owned_by_user('contributor_id'))

    def test_add_new_contribution_for_user_adds_user_to_contributors(self):
        self.collection_summary.add_contribution_by_user('user_id')
        self.assertIn('user_id', self.collection_summary.contributors_summary)
        self.assertEqual(
            self.collection_summary.contributors_summary['user_id'], 1)
        self.assertIn('user_id', self.collection_summary.contributor_ids)

    def test_add_new_contribution_for_user_increases_score_in_contributors(
            self):
        self.collection_summary.add_contribution_by_user('user_id')
        self.collection_summary.add_contribution_by_user('user_id')
        self.assertIn('user_id', self.collection_summary.contributors_summary)
        self.assertEqual(
            self.collection_summary.contributors_summary['user_id'], 2)

    def test_add_new_contribution_for_user_does_not_add_system_user(self):
        self.collection_summary.add_contribution_by_user(
            feconf.SYSTEM_COMMITTER_ID)
        self.assertNotIn(
            feconf.SYSTEM_COMMITTER_ID,
            self.collection_summary.contributors_summary)
        self.assertNotIn(
            feconf.SYSTEM_COMMITTER_ID, self.collection_summary.contributor_ids)
