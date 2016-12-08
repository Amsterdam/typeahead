# -*- coding: utf-8 -*-
import json
import unittest

from httmock import urlmatch, HTTMock

import conf
import server
from model.typeaheadresponse import TypeAheadResponse, Suggestion, \
    TypeAheadResponses


class TestTypeahead(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = server.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

        self.maxDiff = None

        self.bag_url = conf.UPSTREAM_CONFIG['bag']['endpoint']
        self.hr_url = conf.UPSTREAM_CONFIG['hr']['endpoint']

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200, 'index page not found')
        self.assertEqual(response.data, b'up and running',
                         'index page not quite as expected')

    @staticmethod
    def _get_content(filename, encoding='utf-8'):
        file = None
        content = None

        try:
            file = open(filename, encoding=encoding)
            content = file.read()
        finally:
            if file is not None:
                file.close()

        return content

    def get_mock_json_content(self):
        return bytes(self._get_content('fixtures/mockjsoncontent.json'), 'utf-8')

    def get_expected_response(self):
        return json.loads(self._get_content('fixtures/mockresponse.json'))

    @urlmatch(query='q=gibberish%20get')
    def response_mock(self, url, request):
        print(url)
        print(request)
        return {'status_code': 200,
                'Content-Type': 'application/json',
                'content': {'some', 'dta'}}

    def test_api_typahead_get(self):
        # mock_json_content = self.get_mock_json_content()
        expected_response = self.get_expected_response()

        with HTTMock(self.response_mock):
            response = self.app.get('/typeahead?q=gibberish%20get')

            self.assertEqual(response.status_code, 200, 'api not working')

            self.assertEqual(json.loads(response.data.decode('utf-8')),
                             expected_response,
                             'api response not quite as expected')
            self.assertEqual(response.content_type, 'application/json',
                             'Verkeerd response type')

    def test_api_typahead_post(self):
        response = self.app.post('/typeahead', data={'q': 'gibberish post'})
        self.assertEqual(response.status_code, 405, 'Post should be forbidden')

    def test_no_query(self):
        response = self.app.get('/typeahead')
        self.assertEqual(response.status_code, 400, 'Query should be provided')

    def test_empty_query(self):
        response = self.app.get('/typeahead', data={'q': ''})
        self.assertEqual(
            response.status_code, 200,
            'Empty query should work without trying to go upstream')

    def test_semi_empty_query(self):
        response = self.app.get('/typeahead', data={'q': '   '})
        self.assertEqual(
            response.status_code, 200,
            'Query with only spaces should work without trying to go upstream')

    def test_str(self):
        sut = TypeAheadResponses([
            TypeAheadResponse(
                'Awesome Section', [
                    Suggestion('urlA', 'displayA'),
                    Suggestion('urlB', 'displayB')],
                10
            )]
        )

        self.assertEqual(json.loads(sut.as_json()), [{
            "label": "Awesome Section",
            "content": [
                {"uri": "urlA", "_display": "displayA"},
                {"uri": "urlB", "_display": "displayB"}
            ]
        }])

    def test_typeaheadresult_sorting(self):
        sut = TypeAheadResponses([
            TypeAheadResponse('c', [], 222),
            TypeAheadResponse('a', [], 1000),
            TypeAheadResponse('d', [], 111),
            TypeAheadResponse('e', [], -5),
            TypeAheadResponse('b', [], 444),
        ])
        expected_result = [
            TypeAheadResponse('a', [], 1000),
            TypeAheadResponse('b', [], 444),
            TypeAheadResponse('c', [], 222),
            TypeAheadResponse('d', [], 111),
            TypeAheadResponse('e', [], -5),
        ]

        self.assertEqual(
            sut._responses_sorted(), expected_result, "Ordering is broken!")


if __name__ == '__main__':
    unittest.main()
