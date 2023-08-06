"""Library 'fetch' method test module"""

import copy
import json
from unittest.mock import Mock, patch
from uuid import uuid4
from matatika.types import DataFormat
from .test_library import TestLibrary

MOCK_DATASET_DATA_RESPONSE = [
    {
        'project_sla.report_year': 2020,
        'project_sla.total_projects': 66
    },
    {
        'project_sla.report_year': 2020,
        'project_sla.total_projects': 87
    },
    {
        'project_sla.report_year': 2020,
        'project_sla.total_projects': 149
    }
]

MOCK_DATASET_RESPONSE = {
    'id': 'b1d851b8-cd3c-4047-ad66-2821d7345315',
    'alias': 'w-o-overview-last-30-days',
    'workspaceId': 'a8f504c2-1d44-4d87-9687-5d70cdfce362',
    'title': 'W/O Overview Last 30 days',
    'visualisation': '{"chartjs-chart": {"chartType": "line"}}',
    'metadata': '{"name": "project_sla", "related_table": ' +
                '{"columns": [{"name": "report_year", "label": "Year"}], ' +
                '"aggregates": [{"name": "total_projects", "label": "Total Work Orders"}]}}'
}


class TestLibraryFetch(TestLibrary):
    """Test class for library 'fetch' method"""

    def setUp(self):

        super().setUp()

        mock_get = patch('matatika.catalog.requests.get')
        self.mock_get = mock_get.start()

        self.mock_get_data = Mock()
        self.mock_get_dataset = Mock()
        self.mock_get_data.text = json.dumps(MOCK_DATASET_DATA_RESPONSE)
        self.mock_get_dataset.json.return_value = MOCK_DATASET_RESPONSE

        self.mock_get.side_effect = (self.mock_get_data, self.mock_get_dataset)
        self.addCleanup(mock_get.stop)

    def test_invalid_arg_types(self):
        """Test provided built-in Python type object instances trigger TypeError"""

        for type_ in {int, float, str, tuple, set, list, dict}:
            type_instance = type_()

            with self.assertRaises(TypeError) as ctx:
                self.client.fetch(str(uuid4()), data_format=type_instance)

            error_msg = ctx.exception.__str__()
            print(error_msg)

            self.assertEqual(error_msg,
                             f'Resource argument expected, got {type(type_instance).__name__}')

    def test_chartjs(self):
        """Test fetch to Chart.js specification"""

        chartjs_spec = self.client.fetch(
            str(uuid4()), data_format=DataFormat.CHARTJS)

        visualisation = json.loads(MOCK_DATASET_RESPONSE['visualisation'])
        metadata = json.loads(MOCK_DATASET_RESPONSE['metadata'])

        # check the chart type is resolved
        self.assertEqual(chartjs_spec['chart_type'],
                         visualisation['chartjs-chart']['chartType'])

        # check there is a label for every dataset
        for dataset in chartjs_spec['data']['datasets']:
            self.assertEqual(len(chartjs_spec['data']['labels']),
                             len(dataset['data']))

        # check the metadata columns are parsed as labels
        for col in metadata['related_table']['columns']:
            key = f"{metadata['name']}.{col['name']}"
            data = [data[key] for data in MOCK_DATASET_DATA_RESPONSE]
            self.assertEqual(chartjs_spec['data']['labels'], [
                             str(d) for d in data])

        # check the metadata aggregates are parsed as data
        for col in metadata['related_table']['aggregates']:
            key = f"{metadata['name']}.{col['name']}"
            data = [data[key] for data in MOCK_DATASET_DATA_RESPONSE]

            for dataset in chartjs_spec['data']['datasets']:
                self.assertEqual(dataset['data'], data)

    def test_chartjs_no_metadata(self):
        """Test fetch to Chart.js specification with no metadata"""

        mock_dataset_response_copy = copy.deepcopy(MOCK_DATASET_RESPONSE)
        mock_dataset_response_copy['metadata'] = None
        self.mock_get_dataset.json.return_value = mock_dataset_response_copy
        self.mock_get.side_effect = (self.mock_get_data, self.mock_get_dataset)

        chartjs_spec = self.client.fetch(
            str(uuid4()), data_format=DataFormat.CHARTJS)

        self.assertIsNone(chartjs_spec)

    def test_chartjs_no_data(self):
        """Test fetch to Chart.js specification with no metadata"""

        self.mock_get_data.text = ''
        self.mock_get.side_effect = (self.mock_get_data, self.mock_get_dataset)

        chartjs_spec = self.client.fetch(
            str(uuid4()), data_format=DataFormat.CHARTJS)

        self.assertIsNone(chartjs_spec)
