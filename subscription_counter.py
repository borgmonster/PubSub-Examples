# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Get number of PubSub subscriptions and write to StackDriver."""

from googleapiclient import discovery
import google.auth
from google.cloud import logging
from google.cloud.logging.resource import Resource


class PubSubSubscriptionCounter(object):

  """TODO(johngao): add doc.
  """

  def __init__(self, project_id, credentials):
    """Different credentials have different inherited accesses.

    Args:
        project_id: GCP project id
        credentials: credential object

    Returns: None
    """
    self._project_id = 'projects/' + project_id
    self._credentials = credentials

  def get_subscriptions(self):
    """Gets PubSub subscriptions by project.

    Yields: a subscription name
    """
    service = discovery.build('pubsub', 'v1', credentials=self._credentials)
    request = service.projects().subscriptions().list(
        project=self._project_id)
    while request is not None:
      response = request.execute()
      # TODO(johngao): check the response status
      if response:
        for sub in response['subscriptions']:
          yield sub['name']
      request = service.projects().subscriptions().list_next(
          previous_request=request, previous_response=response)

  def write_to_stackdriver(self, subs):
    """Writes an entry to Stackdriver log.

    Args:
        subs: number of subscriptions

    Returns: None
    """
    log_client = logging.Client()
    logger = log_client.logger('quota-watcher')
    res = Resource(type='pubsub_subscription',
                   labels={'usage': 'quota_watcher',},)
    logger.log_struct({'total_subscriptions': subs}, resource=res)


if __name__ == '__main__':
  credentials, project_id = google.auth.default()
  counter = PubSubSubscriptionCounter(project_id, credentials)
  subs_count = sum(1 for i in counter.get_subscriptions())
  counter.write_to_stackdriver(subs_count)
