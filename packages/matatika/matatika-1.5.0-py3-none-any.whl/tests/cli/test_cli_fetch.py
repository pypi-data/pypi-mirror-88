"""CLI 'fetch' command test module"""

# standard
import unittest
from unittest.mock import patch
import uuid
# local
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI
from tests.unittest_base import MOCK_DATA


class TestCLIFetch(TestCLI):
    """Test class for CLI fetch command"""

    def test_fetch_without_argument(self):
        """Test fetch without argument"""

        result = self.runner.invoke(matatika, ["fetch"])
        self.assertIn(
            "Error: Missing argument 'DATASET_ID'.", result.output)
        self.assertIs(result.exit_code, 2)

    def test_fetch_with_invalid_dataset_id(self):
        """Test fetch with invalid auth token"""

        # not a valid UUID
        invalid_uuid = "invalid-uuid"
        result = self.runner.invoke(matatika, ["fetch",
                                               invalid_uuid])
        self.assertIn(
            f"{invalid_uuid} is not a valid UUID value", result.output)

    @patch('catalog.requests.get')
    def test_fetch(self, mock_get_request):
        """Test fetch"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.text = str(MOCK_DATA)

        result = self.runner.invoke(matatika, ["fetch",
                                               str(uuid.uuid4())])
        self.assertIn(str(MOCK_DATA), result.output)

    @unittest.skip
    @patch('cli.commands.fetch.open')
    @patch('catalog.requests.get')
    def test_fetch_with_output_file_opt(self, mock_get_request, _mock_open):
        """Test fetch with output file option"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.text = str(MOCK_DATA)

        dataset_id = str(uuid.uuid4())

        file_ = "test.txt"
        result = self.runner.invoke(matatika, ["fetch",
                                               dataset_id,
                                               "-f", file_])
        self.assertIn(f"Dataset {dataset_id} data successfully written to {file_}",
                      result.output)
