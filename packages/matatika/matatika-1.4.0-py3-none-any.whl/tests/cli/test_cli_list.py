"""CLI 'list' command test module"""

# standard
from unittest.mock import patch
import uuid
# local
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI


class TestCLIList(TestCLI):
    """Test class for CLI list command"""

    def test_list_no_subcommmand(self):
        """Test list with no subcommand"""

        result = self.runner.invoke(matatika, ["list"])
        self.assertIn(
            "Usage: matatika list [OPTIONS] COMMAND [ARGS]...", result.output)
        self.assertIs(result.exit_code, 0)

    def test_list_invalid_subcommand(self):
        """Test list with an invalid subcommand"""

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["list", resource_type])
        self.assertIn(
            f"Error: No such command '{resource_type}'.", result.output)
        self.assertIs(result.exit_code, 2)

    @patch('catalog.requests.get')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    def test_list_workspaces(self, _mock_decoded_jwt, mock_get_request):
        """Test list workspaces"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = TestCLI.MOCK_WORKSPACES_RESPONSE

        result = self.runner.invoke(matatika, ["list",
                                               "workspaces"])

        workspaces = TestCLI.MOCK_WORKSPACES_RESPONSE['_embedded']['workspaces']
        for workspace in workspaces:
            self.assertIn(workspace['id'], result.output)
            self.assertIn(workspace['name'], result.output)

        self.assertIn(f"Total workspaces: {len(workspaces)}",
                      result.output)

    @patch('catalog.requests.get')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    def test_list_datasets(self, _mock_decoded_jwt, mock_get_request):
        """Test list datasets"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = TestCLI.MOCK_DATASETS_RESPONSE

        result = self.runner.invoke(matatika, ["list",
                                               "datasets",
                                               "-w",
                                               str(uuid.uuid4())])

        datasets = TestCLI.MOCK_DATASETS_RESPONSE['_embedded']['datasets']
        for dataset in datasets:
            self.assertIn(dataset['id'], result.output)
            self.assertIn(dataset['title'], result.output)

        self.assertIn(f"Total datasets: {len(datasets)}",
                      result.output)
