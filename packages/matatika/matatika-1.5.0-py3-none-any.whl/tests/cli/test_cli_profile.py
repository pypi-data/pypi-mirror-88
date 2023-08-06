"""CLI 'profile' command test module"""

from mock import patch
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI
from tests.unittest_base import MOCK_PROFILE_RESPONSE


class TestCLIPublish(TestCLI):
    """Test class for CLI profile command"""

    @patch('catalog.requests.get')
    def test_profile(self, mock_get_request):
        """Test profile"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = MOCK_PROFILE_RESPONSE

        result = self.runner.invoke(matatika, ["profile"])

        self.assertIn(MOCK_PROFILE_RESPONSE['id'], result.output)
        self.assertIn(MOCK_PROFILE_RESPONSE['name'], result.output)
