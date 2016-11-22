# -*- coding: utf-8 -*-
import json
import unittest

from mockito import *
from requests import sessions

import conf
import server
from model.typeaheadresponse import TypeAheadResponse, Suggestion, \
    TypeAheadResponses
from tests.mocks import MockResponse


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
    def get_mock_json_content():
        return bytes("""[
  {
    "content": [
      {
        "_display": "Yottabyte Solutions",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/61130354\/"
      },
      {
        "_display": "Lotta",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/34341717\/"
      },
      {
        "_display": "Koninklijke Fabrieken Posthumus B.V.",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/33013145\/"
      },
      {
        "_display": "DOETA",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/65592719\/"
      },
      {
        "_display": "yolga",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/65431200\/"
      }
    ],
    "label": "Maatschappelijke activiteiten"
  },
  {
    "content": [
      {
        "_display": "Yottabyte Solutions - Van Spilbergenstraat 95",
        "uri": "handelsregister\/vestiging\/000030256488\/"
      },
      {
        "_display": "Lotta - Zamenhofstraat 110",
        "uri": "handelsregister\/vestiging\/000008813965\/"
      },
      {
        "_display": "Yokata - Vrolikstraat 238",
        "uri": "handelsregister\/vestiging\/000007095988\/"
      },
      {
        "_display": "Yogya - Johan Huizingalaan 142",
        "uri": "handelsregister\/vestiging\/000007582978\/"
      },
      {
        "_display": "DOETA - Kampina 9",
        "uri": "handelsregister\/vestiging\/000034303162\/"
      },
      {
        "_display": "Yokata - Lutmastraat 182",
        "uri": "handelsregister\/vestiging\/000033381151\/"
      },
      {
        "_display": "Volta - Houtmankade 336",
        "uri": "handelsregister\/vestiging\/000029763665\/"
      },
      {
        "_display": "yolga - Bernard Shawsingel 284",
        "uri": "handelsregister\/vestiging\/000034156488\/"
      },
      {
        "_display": "ATTA - Von Zesenstraat 179",
        "uri": "handelsregister\/vestiging\/000000343528\/"
      },
      {
        "_display": "Totta Research N.V. - Burgemeester Stramanweg 105",
        "uri": "handelsregister\/vestiging\/000026200902\/"
      }
    ],
    "label": "Vestigingen"
  }
]
""", 'utf-8')

    @staticmethod
    def get_expected_response():
        return json.loads("""
[
  {
    "content": [
      {
        "_display": "Yottabyte Solutions",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/61130354\/"
      },
      {
        "_display": "Lotta",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/34341717\/"
      },
      {
        "_display": "Koninklijke Fabrieken Posthumus B.V.",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/33013145\/"
      },
      {
        "_display": "DOETA",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/65592719\/"
      },
      {
        "_display": "yolga",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/65431200\/"
      }
    ],
    "label": "Maatschappelijke activiteiten"
  },
  {
    "content": [
      {
        "_display": "Yottabyte Solutions - Van Spilbergenstraat 95",
        "uri": "handelsregister\/vestiging\/000030256488\/"
      },
      {
        "_display": "Lotta - Zamenhofstraat 110",
        "uri": "handelsregister\/vestiging\/000008813965\/"
      },
      {
        "_display": "Yokata - Vrolikstraat 238",
        "uri": "handelsregister\/vestiging\/000007095988\/"
      },
      {
        "_display": "Yogya - Johan Huizingalaan 142",
        "uri": "handelsregister\/vestiging\/000007582978\/"
      },
      {
        "_display": "DOETA - Kampina 9",
        "uri": "handelsregister\/vestiging\/000034303162\/"
      },
      {
        "_display": "Yokata - Lutmastraat 182",
        "uri": "handelsregister\/vestiging\/000033381151\/"
      },
      {
        "_display": "Volta - Houtmankade 336",
        "uri": "handelsregister\/vestiging\/000029763665\/"
      },
      {
        "_display": "yolga - Bernard Shawsingel 284",
        "uri": "handelsregister\/vestiging\/000034156488\/"
      },
      {
        "_display": "ATTA - Von Zesenstraat 179",
        "uri": "handelsregister\/vestiging\/000000343528\/"
      },
      {
        "_display": "Totta Research N.V. - Burgemeester Stramanweg 105",
        "uri": "handelsregister\/vestiging\/000026200902\/"
      }
    ],
    "label": "Vestigingen"
  },
  {
    "content": [
      {
        "_display": "Yottabyte Solutions",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/61130354\/"
      },
      {
        "_display": "Lotta",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/34341717\/"
      },
      {
        "_display": "Koninklijke Fabrieken Posthumus B.V.",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/33013145\/"
      },
      {
        "_display": "DOETA",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/65592719\/"
      },
      {
        "_display": "yolga",
        "uri": "handelsregister\/maatschappelijkeactiviteit\/65431200\/"
      }
    ],
    "label": "Maatschappelijke activiteiten"
  },
  {
    "content": [
      {
        "_display": "Yottabyte Solutions - Van Spilbergenstraat 95",
        "uri": "handelsregister\/vestiging\/000030256488\/"
      },
      {
        "_display": "Lotta - Zamenhofstraat 110",
        "uri": "handelsregister\/vestiging\/000008813965\/"
      },
      {
        "_display": "Yokata - Vrolikstraat 238",
        "uri": "handelsregister\/vestiging\/000007095988\/"
      },
      {
        "_display": "Yogya - Johan Huizingalaan 142",
        "uri": "handelsregister\/vestiging\/000007582978\/"
      },
      {
        "_display": "DOETA - Kampina 9",
        "uri": "handelsregister\/vestiging\/000034303162\/"
      },
      {
        "_display": "Yokata - Lutmastraat 182",
        "uri": "handelsregister\/vestiging\/000033381151\/"
      },
      {
        "_display": "Volta - Houtmankade 336",
        "uri": "handelsregister\/vestiging\/000029763665\/"
      },
      {
        "_display": "yolga - Bernard Shawsingel 284",
        "uri": "handelsregister\/vestiging\/000034156488\/"
      },
      {
        "_display": "ATTA - Von Zesenstraat 179",
        "uri": "handelsregister\/vestiging\/000000343528\/"
      },
      {
        "_display": "Totta Research N.V. - Burgemeester Stramanweg 105",
        "uri": "handelsregister\/vestiging\/000026200902\/"
      }
    ],
    "label": "Vestigingen"
  }
]
""")

    @unittest.skip("Needs deeper mocking")
    def test_api_typahead_get(self):
        mock_json_content = self.get_mock_json_content()
        expected_response = self.get_expected_response()

        mock_hr_response = MockResponse(
            encoding='utf-8',
            status_code=200,
            ok=True,
            url='http://hr.endpoint.internal',
            _content=mock_json_content)

        try:
            when(sessions.Session).request(
                'GET',
                self.hr_url + '?q={q}'.format(q='gibberish get'),
                timeout=0.5,
                headers={'Accept': 'application/json',
                         'Content-Type': 'application/json'},
                stream=False).thenReturn(mock_hr_response)

            when(sessions.Session).request(
                'GET',
                self.bag_url + '?q={q}'.format(q='gibberish get'),
                timeout=0.5,
                headers={'Accept': 'application/json',
                         'Content-Type': 'application/json'},
                stream=False).thenReturn(mock_hr_response)

            response = self.app.get('/typeahead?q=gibberish%20get')

            self.assertEqual(response.status_code, 200, 'api not working')

            self.assertEqual(json.loads(response.data.decode('utf-8')),
                             expected_response,
                             'api response not quite as expected')
            self.assertEqual(response.content_type, 'application/json',
                             'Verkeerd response type')
        finally:
            unstub()

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
