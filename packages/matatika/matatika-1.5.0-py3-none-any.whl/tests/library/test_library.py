"""Base library test module"""

from matatika.library import MatatikaClient
from tests.unittest_base import UnittestBase


class TestLibrary(UnittestBase):
    """Test class for library"""

    def setUp(self):

        super().setUp()

        auth_token = 'auth-token'
        endpoint_url = 'endpoint_url'
        workspace_id = None
        self.client = MatatikaClient(auth_token, endpoint_url, workspace_id)
