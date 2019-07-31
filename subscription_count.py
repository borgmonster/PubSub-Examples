# Copyright 2018 Google LLC


from googleapiclient import discovery
from google.oauth2 import service_account


class SubscriptionQuotaCheck(object):
  """
  TODO(johngao): add docs 
  """

  def __init__(self, credentials, project_id, alert_threshold):
    """Different credentials have different inherited accesses.
    """
    self.credentials = credentials
    self.project = 'projects/' + project_id
    self.alert_threshold = int(alert_threshold)

  def get_subscriptions(self):
    """Gets subscripitions of the project 

       Yields:
         subscription names.
    """
    service = discovery.build('pubsub', 'v1', credentials=self.credentials)
    request = service.projects().subscriptions().list(project=self.project)
    
    while request is not None:
      response = request.execute()
      # TODO(johngao): check the response status
      if response:
        for sub in response['subscriptions']:
          yield sub['name']
      request = service.projects().subscriptions().list_next(previous_request=request, previous_response=response)

  def check_quota(self):
    total_subs = len([i for i in self.get_subscriptions()])
    if total_subs > self.alert_threshold:
      print "ALERT", self.alert_threshold, total_subs


if __name__ == '__main__':
  
  credentials = service_account.Credentials.from_service_account_file('log-pubsub-sa.json')
  checker = SubscriptionQuotaCheck(credentials, 20*0.50)
  checker.get_subscriptions()
  checker.check_quota()

