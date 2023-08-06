class SonarAPIGroup(object):
    #Endpoint for security
    GROUP_CREATE_ENDPOINT = '/api/user_groups/create'
    GROUP_LIST_ENDPOINT = '/api/user_groups/search'
    GROUP_DELETE_ENDPOINT = '/api/user_groups/delete'
    GROUP_UPDATE_ENDPOINT = '/api/user_groups/update'

    def __init__(self, api=None):
        self._api = api

    def create_group(self, group_name, group_description):
        """
        Create group.

        :param group_name: name of the group
        :param group_description: description of the group
        :return: request response
        """
        # Build main data to post
        data = {
            'name': group_name,
            'description': group_description
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.GROUP_CREATE_ENDPOINT, **data)
        return res

    def search_group(self, group_name):
        """
        Search group with specified name.

        :param group_name: name of the group
        :return: request response
        """
        # Build main data to post
        data = {
            'q': group_name
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.GROUP_LIST_ENDPOINT, **data)
        return res

    def delete_group(self, group_id):
        """
        Delete group id.

        :param group_id: id of the group
        :return: request response
        """
        # Build main data to post
        data = {
            'id': group_id
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.GROUP_DELETE_ENDPOINT_ENDPOINT, **data)
        return res

    def update_group(self, group_id, group_name, group_description):
        """
        Delete group id.

        :param group_id: id of the group to update
        :param group_name: new name
        :param group_description: new description
        :return: request response
        """
        # Build main data to post
        data = {
            'id': group_id,
            'name': group_name,
            'description': group_description
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.GROUP_UPDATE_ENDPOINT, **data)
        return res