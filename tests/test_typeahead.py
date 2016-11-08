# -*- coding: utf-8 -*-
import unittest

from typeahead import typeahead


class TestTypeahead(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = typeahead.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200, 'index page not found')
        self.assertEqual(response.data, b'up and running',
                         'index page not quite as expected')

    def test_api_typahead_get(self):
        response = self.app.get('/tr')
        self.assertEqual(response.status_code, 200, 'api not working')
        self.assertEqual(response.data, b'{"get": "response"}\n',
                         'api response not quite as expected')
        self.assertEqual(response.content_type, 'application/json',
                         'Verkeerd response type')

    def test_api_typahead_post(self):
        response = self.app.post('/tr')
        self.assertEqual(response.status_code, 200, 'api not working')
        self.assertEqual(response.data, b'{"post": "response"}\n',
                         'api response not quite as expected')
        self.assertEqual(response.content_type, 'application/json',
                         'Verkeerd response type')


if __name__ == '__main__':
    unittest.main()
