"""Base unittest module"""

from unittest import TestCase
from unittest.mock import patch

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


class UnittestBase(TestCase):
    """Class to instantiate, initialise and run common mocks"""

    def setUp(self):

        # jwt decode
        mock_jwt_decode = patch('matatika.catalog.jwt.decode')
        self.mock_jwt_decode = mock_jwt_decode.start()
        self.mock_jwt_decode.return_value = MOCK_DECODED_JWT
        self.addCleanup(mock_jwt_decode.stop)
