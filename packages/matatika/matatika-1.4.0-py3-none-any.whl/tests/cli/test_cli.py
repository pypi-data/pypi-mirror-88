"""Base CLI test module"""

# standard
import copy
import unittest
from unittest.mock import patch
# external
from click.testing import CliRunner
# local
from matatika.context import DEFAULT, CONTEXTS


class TestCLI(unittest.TestCase):
    """Test class for CLI"""

    MOCK_DECODED_JWT = {
        'sub': 'provider|profile-id'
    }

    MOCK_PROFILE_RESPONSE = {
        'id': MOCK_DECODED_JWT['sub'],
        'name': 'profile name'
    }

    MOCK_WORKSPACES_RESPONSE = {
        '_embedded': {
            'workspaces': [
                {
                    'id': '89969253-723d-415d-b199-bcac2aaa4cde',
                    'name': 'workspace 1'
                },
                {
                    'id': '9f47ec52-41da-46eb-be7e-f7ef65490081',
                    'name': 'workspace 2'
                }
            ]
        },
        'page': {
            'totalElements': 2
        }
    }

    MOCK_DATASET_RESPONSE = {
        'id': 'b944735d-cb69-49a2-b871-3ced1fed5b02',
        'published': '2020-12-09T16:48:10.132',
        'alias': 'test1',
        'workspaceId': '8566fe13-f30b-4536-aecf-b3879bd0910f',
        'source': 'Reuben F Channel',
        'title': 'test1',
        'description': None,
        'questions': None,
        'rawData': None,
        'visualisation': None,
        'metadata': None,
        'query': None,
        'likeCount': 0,
        'likedByProfiles': [],
        'commentCount': 0,
        'viewCount': 0,
        'created': '2020-12-09T14:42:20.82',
        'score': 1.0
    }

    MOCK_DATASETS_RESPONSE = {
        '_embedded': {
            'datasets': [
                {
                    'id': '280a2ab2-f30e-4200-b765-ed73af3d63db',
                    'alias': 'dataset-1',
                    'title': 'dataset 1'
                },
                {
                    'id': 'c50d444f-a71d-4f29-a2cc-ee905ddc1e15',
                    'alias': 'dataset-2',
                    'title': 'dataset 2'
                }
            ]
        },
        'page': {
            'totalElements': 2
        }
    }

    MOCK_DATA = {
        'google_analytics_active_user_stats.total_daily_active_users': 9,
        'google_analytics_active_user_stats.total_weekly_active_users': 26,
        'google_analytics_active_user_stats.total_14d_active_users': 75,
        'google_analytics_active_user_stats.total_28d_active_users': 201,
    }

    MOCK_CONTEXTS = (
        'context1',
        'context2',
        'context3'
    )

    MOCK_CONTEXTS_JSON = {
        DEFAULT: MOCK_CONTEXTS[0],
        CONTEXTS: {
            MOCK_CONTEXTS[0]: {
                'auth_token': MOCK_CONTEXTS[0] + '_auth_token',
                'endpoint_url': MOCK_CONTEXTS[0] + '_endpoint_url',
                'workspace_id': MOCK_CONTEXTS[0] + '_workspace_id'
            },
            MOCK_CONTEXTS[1]: {
                'auth_token': MOCK_CONTEXTS[1] + '_auth_token',
                'endpoint_url': MOCK_CONTEXTS[1] + '_endpoint_url',
                'workspace_id': MOCK_CONTEXTS[1] + '_workspace_id'
            },
            MOCK_CONTEXTS[2]: {
                'auth_token': MOCK_CONTEXTS[2] + '_auth_token',
                'endpoint_url': MOCK_CONTEXTS[2] + '_endpoint_url',
                'workspace_id': MOCK_CONTEXTS[2] + '_workspace_id'
            }
        }
    }

    def setUp(self):

        mock__read_json = patch(
            'matatika.context.MatatikaContext._read_json')
        self.mock__read_json = mock__read_json.start()
        self.mock__read_json.return_value = copy.deepcopy(
            TestCLI.MOCK_CONTEXTS_JSON)
        self.addCleanup(mock__read_json.stop)

        mock__write_json = patch(
            'matatika.context.MatatikaContext._write_json')
        self.mock__write_json = mock__write_json.start()
        self.addCleanup(mock__write_json.stop)

        # instantiate a cli runner
        self.runner = CliRunner()
