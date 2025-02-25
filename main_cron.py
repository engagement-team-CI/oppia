# Copyright 2014 The Oppia Authors. All Rights Reserved.
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

"""Main package for URL routing and the index page."""

from __future__ import absolute_import
from __future__ import unicode_literals

from core.controllers import cron
from core.platform import models
import feconf
import main

import webapp2


transaction_services = models.Registry.import_transaction_services() # type: ignore[no-untyped-call]

# Register the URLs with the classes responsible for handling them.
URLS = [
    main.get_redirect_route(
        r'/cron/mail/admin/job_status', cron.JobStatusMailerHandler),
    main.get_redirect_route(
        r'/cron/users/dashboard_stats', cron.CronDashboardStatsHandler),
    main.get_redirect_route(
        r'/cron/users/user_deletion', cron.CronUserDeletionHandler),
    main.get_redirect_route(
        r'/cron/users/fully_complete_user_deletion',
        cron.CronFullyCompleteUserDeletionHandler),
    main.get_redirect_route(
        r'/cron/explorations/recommendations',
        cron.CronExplorationRecommendationsHandler),
    main.get_redirect_route(
        r'/cron/explorations/search_rank',
        cron.CronActivitySearchRankHandler),
    main.get_redirect_route(
        r'/cron/jobs/cleanup', cron.CronMapreduceCleanupHandler),
    main.get_redirect_route(
        r'/cron/models/cleanup', cron.CronModelsCleanupHandler),
    main.get_redirect_route(
        r'/cron/mail/admins/contributor_dashboard_bottlenecks',
        cron.CronMailAdminContributorDashboardBottlenecksHandler),
    main.get_redirect_route(
        r'/cron/mail/reviewers/contributor_dashboard_suggestions',
        cron.CronMailReviewersContributorDashboardSuggestionsHandler),
    main.get_redirect_route(
        r'/cron/suggestions/translation_contribution_stats',
        cron.CronTranslationContributionStatsHandler),
]

app = transaction_services.toplevel_wrapper(  # pylint: disable=invalid-name
    webapp2.WSGIApplication(URLS, debug=feconf.DEBUG))
