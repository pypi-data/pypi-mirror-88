"""CLI 'profile' command test module"""

from mock import patch
from tests.cli.test_cli import TestCLI
from matatika.cli.commands.root import matatika


class TestCLIPublish(TestCLI):
    """Test class for CLI profile command"""

    @patch('catalog.requests.get')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    def test_profile(self, _mock_decoded_jwt, mock_get_request):
        """Test profile"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = TestCLI.MOCK_PROFILE_RESPONSE

        result = self.runner.invoke(matatika, ["profile"])

        self.assertIn(
            TestCLI.MOCK_PROFILE_RESPONSE['id'], result.output)
        self.assertIn(
            TestCLI.MOCK_PROFILE_RESPONSE['name'], result.output)
