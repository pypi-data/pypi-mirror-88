class SonarAPIUser(object):
    #Endpoint for permission templates
    USER_CURRENT_ENDPOINT = '/api/users/current'

    def __init__(self, api=None):
        self._api = api

    def current(self):
        """
        Create template.
        """

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.USER_CURRENT_ENDPOINT)
        return res
    

