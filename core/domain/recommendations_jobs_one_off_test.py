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

"""Tests for recommendations_jobs_one_off."""

from __future__ import absolute_import
from __future__ import unicode_literals

from core import jobs_registry
from core.domain import exp_services
from core.domain import recommendations_jobs_one_off
from core.domain import recommendations_services
from core.domain import recommendations_services_test
from core.domain import rights_manager
from core.domain import taskqueue_services
from core.domain import user_services


class ExplorationRecommendationsOneOffJobUnitTests(
        recommendations_services_test.RecommendationsServicesUnitTests):
    """Test exploration recommendations one-off job."""

    ONE_OFF_JOB_MANAGERS_FOR_TESTS = [
        recommendations_jobs_one_off.ExplorationRecommendationsOneOffJob]

    def setUp(self):
        super(ExplorationRecommendationsOneOffJobUnitTests, self).setUp()
        self.job_class = (
            recommendations_jobs_one_off.ExplorationRecommendationsOneOffJob)

    def test_basic_computation(self):
        recommendations_services.update_topic_similarities(
            'Art,Biology,Chemistry\n'
            '1.0,0.2,0.1\n'
            '0.2,1.0,0.8\n'
            '0.1,0.8,1.0')

        with self.swap(
            jobs_registry, 'ONE_OFF_JOB_MANAGERS',
            self.ONE_OFF_JOB_MANAGERS_FOR_TESTS
            ):
            self.job_class.enqueue(self.job_class.create_new())
            self.assertEqual(
                self.count_jobs_in_mapreduce_taskqueue(
                    taskqueue_services.QUEUE_NAME_ONE_OFF_JOBS), 1)
            self.process_and_flush_pending_mapreduce_tasks()

            recommendations = (
                recommendations_services.get_exploration_recommendations(
                    'exp_id_1'))
            self.assertEqual(
                recommendations, ['exp_id_4', 'exp_id_2', 'exp_id_3'])
            recommendations = (
                recommendations_services.get_exploration_recommendations(
                    'exp_id_4'))
            self.assertEqual(
                recommendations, ['exp_id_1', 'exp_id_2', 'exp_id_3'])

    def test_recommendations_after_changes_in_rights(self):
        with self.swap(
            jobs_registry, 'ONE_OFF_JOB_MANAGERS',
            self.ONE_OFF_JOB_MANAGERS_FOR_TESTS
            ):
            self.job_class.enqueue(self.job_class.create_new())
            self.assertEqual(
                self.count_jobs_in_mapreduce_taskqueue(
                    taskqueue_services.QUEUE_NAME_ONE_OFF_JOBS), 1)
            self.process_and_flush_pending_mapreduce_tasks()

            recommendations = (
                recommendations_services.get_exploration_recommendations(
                    'exp_id_1'))
            self.assertEqual(
                recommendations, ['exp_id_4', 'exp_id_2', 'exp_id_3'])

            system_user = user_services.get_system_user()
            rights_manager.unpublish_exploration(system_user, 'exp_id_4')

            self.job_class.enqueue(self.job_class.create_new())
            self.assertEqual(
                self.count_jobs_in_mapreduce_taskqueue(
                    taskqueue_services.QUEUE_NAME_ONE_OFF_JOBS), 1)
            self.process_and_flush_pending_mapreduce_tasks()
            recommendations = (
                recommendations_services.get_exploration_recommendations(
                    'exp_id_1'))
            self.assertEqual(recommendations, ['exp_id_2', 'exp_id_3'])

    def test_recommendations_with_invalid_exploration_summaries_would_be_empty(
            self):
        def _mock_get_non_private_exploration_summaries():
            """Return an invalid exploration summary dict."""
            return {'new_exp_id': 'new_exploration_summary'}

        with self.swap(
            jobs_registry, 'ONE_OFF_JOB_MANAGERS',
            self.ONE_OFF_JOB_MANAGERS_FOR_TESTS
            ):
            # We need to swap here to make the recommendations an empty list
            # (since 'get_exploration_recommendations()' returns a list of ids
            # of at most 10 recommended explorations to play after completing
            # the exploration).
            with self.swap(
                exp_services, 'get_non_private_exploration_summaries',
                _mock_get_non_private_exploration_summaries):
                self.job_class.enqueue(self.job_class.create_new())
                self.assertEqual(
                    self.count_jobs_in_mapreduce_taskqueue(
                        taskqueue_services.QUEUE_NAME_ONE_OFF_JOBS), 1)
                self.process_and_flush_pending_mapreduce_tasks()

                recommendations = (
                    recommendations_services.get_exploration_recommendations(
                        'exp_id_1'))
                self.assertEqual(
                    recommendations, [])
