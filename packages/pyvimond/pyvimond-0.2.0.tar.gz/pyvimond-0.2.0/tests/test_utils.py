import unittest
import pyvimond.utils as utils


class UtilsTest(unittest.TestCase):

    def test_create_api_metadata(self):
        metadata = {
            'foo': True,
            'bar': 'very bar',
            'baz': 42
        }

        self.assertEqual({
            'entries': {
                'foo': [{'value': True, 'lang': '*'}],
                'bar': [{'value': 'very bar', 'lang': '*'}],
                'baz': [{'value': 42, 'lang': '*'}],
            },
            'empty': True
        }, utils.create_api_metadata(metadata))

    def test_create_sumo_signature(self):
        method = 'GET'
        path = '/api/web/asset/1334686?expand=metadata&showHiddenMetadata=true'
        secret = 'secret'
        timestamp = 'Wed, 09 Dec 2020 09:48:44 +0200'

        self.assertEqual('Xm2Kr+xdb4uEp3F7COA+oj8EOpg=', utils.create_sumo_signature(method, path, secret, timestamp))

    def test_create_basic_auth_token(self):
        token = utils.create_basic_auth_token("username", "password")

        self.assertEqual('dXNlcm5hbWU6cGFzc3dvcmQ=', token)


if __name__ == '__main__':
    unittest.main()
