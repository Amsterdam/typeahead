# -*- coding: utf-8 -*-
import json
import unittest

from mockito import *
from requests import sessions

import typeahead
from mocks import MockResponse
from model.typeaheadresponse import TypeAheadResponse, Suggestion, \
    TypeAheadResponses


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
        mock_json_content = \
            b'[' \
            b'{"content":[' \
            b'{"_display":"Yottabyte Solutions",' \
            b'"uri":"handelsregister/maatschappelijkeactiviteit/61130354/"},' \
            b'{"_display":"Lotta",' \
            b'"uri":"handelsregister/maatschappelijkeactiviteit/34341717/"},' \
            b'{"_display":"Koninklijke Fabrieken Posthumus B.V.",' \
            b'"uri":"handelsregister/maatschappelijkeactiviteit/33013145/"},' \
            b'{"_display":"DOETA",' \
            b'"uri":"handelsregister/maatschappelijkeactiviteit/65592719/"},' \
            b'{"_display":"yolga",' \
            b'"uri":"handelsregister/maatschappelijkeactiviteit/65431200/"}],' \
            b'"label":"Maatschappelijke activiteiten"},' \
            b'{"content":[' \
            b'{"_display":"Yottabyte Solutions - Van Spilbergenstraat 95",' \
            b'"uri":"handelsregister/vestiging/000030256488/"},' \
            b'{"_display":"Lotta - Zamenhofstraat 110",' \
            b' "uri":"handelsregister/vestiging/000008813965/"},' \
            b'{"_display":"Yokata - Vrolikstraat 238",' \
            b'"uri":"handelsregister/vestiging/000007095988/"},' \
            b'{"_display":"Yogya - Johan Huizingalaan 142",' \
            b'"uri":"handelsregister/vestiging/000007582978/"},' \
            b'{"_display":"DOETA - Kampina 9",' \
            b'"uri":"handelsregister/vestiging/000034303162/"},' \
            b'{"_display":"Yokata - Lutmastraat 182",' \
            b'"uri":"handelsregister/vestiging/000033381151/"},' \
            b'{"_display":"Volta - Houtmankade 336",' \
            b'"uri":"handelsregister/vestiging/000029763665/"},' \
            b'{"_display":"yolga - Bernard Shawsingel 284",' \
            b'"uri":"handelsregister/vestiging/000034156488/"},' \
            b'{"_display":"ATTA - Von Zesenstraat 179",' \
            b'"uri":"handelsregister/vestiging/000000343528/"},' \
            b'{"_display":"Totta Research N.V. - Burgemeester Stramanweg 105",' \
            b'"uri":"handelsregister/vestiging/000026200902/"}' \
            b'],' \
            b'"label":"Vestigingen"}' \
            b']'

        expected_response = \
            b'[' \
            b'{"content": [' \
            b'{"_display": "Yottabyte Solutions", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/61130354/"}, ' \
            b'{"_display": "Lotta", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/34341717/"}, ' \
            b'{"_display": "Koninklijke Fabrieken Posthumus B.V.", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/33013145/"}, ' \
            b'{"_display": "DOETA", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/65592719/"}, ' \
            b'{"_display": "yolga", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/65431200/"}' \
            b'], ' \
            b'"label": "Maatschappelijke activiteiten"}, ' \
            b'{"content": [' \
            b'{"_display": "Yottabyte Solutions - Van Spilbergenstraat 95", ' \
            b'"uri": "handelsregister/vestiging/000030256488/"}, ' \
            b'{"_display": "Lotta - Zamenhofstraat 110", ' \
            b'"uri": "handelsregister/vestiging/000008813965/"}, ' \
            b'{"_display": "Yokata - Vrolikstraat 238", ' \
            b'"uri": "handelsregister/vestiging/000007095988/"}, ' \
            b'{"_display": "Yogya - Johan Huizingalaan 142", ' \
            b'"uri": "handelsregister/vestiging/000007582978/"}, ' \
            b'{"_display": "DOETA - Kampina 9", ' \
            b'"uri": "handelsregister/vestiging/000034303162/"}, ' \
            b'{"_display": "Yokata - Lutmastraat 182", ' \
            b'"uri": "handelsregister/vestiging/000033381151/"}, ' \
            b'{"_display": "Volta - Houtmankade 336", ' \
            b'"uri": "handelsregister/vestiging/000029763665/"}, ' \
            b'{"_display": "yolga - Bernard Shawsingel 284", ' \
            b'"uri": "handelsregister/vestiging/000034156488/"}, ' \
            b'{"_display": "ATTA - Von Zesenstraat 179", ' \
            b'"uri": "handelsregister/vestiging/000000343528/"}, ' \
            b'{"_display": "Totta Research N.V. - Burgemeester Stramanweg 105", ' \
            b'"uri": "handelsregister/vestiging/000026200902/"}], ' \
            b'"label": "Vestigingen"}, ' \
            b'{"content": [' \
            b'{"_display": "Yottabyte Solutions", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/61130354/"}, ' \
            b'{"_display": "Lotta", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/34341717/"}, ' \
            b'{"_display": "Koninklijke Fabrieken Posthumus B.V.", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/33013145/"}, ' \
            b'{"_display": "DOETA", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/65592719/"},' \
            b' {"_display": "yolga", ' \
            b'"uri": "handelsregister/maatschappelijkeactiviteit/65431200/"}' \
            b'], ' \
            b'"label": "Maatschappelijke activiteiten"}, ' \
            b'{"content": [' \
            b'{"_display": "Yottabyte Solutions - Van Spilbergenstraat 95", ' \
            b'"uri": "handelsregister/vestiging/000030256488/"}, ' \
            b'{"_display": "Lotta - Zamenhofstraat 110", ' \
            b'"uri": "handelsregister/vestiging/000008813965/"}, ' \
            b'{"_display": "Yokata - Vrolikstraat 238", ' \
            b'"uri": "handelsregister/vestiging/000007095988/"}, ' \
            b'{"_display": "Yogya - Johan Huizingalaan 142", ' \
            b'"uri": "handelsregister/vestiging/000007582978/"}, ' \
            b'{"_display": "DOETA - Kampina 9", ' \
            b'"uri": "handelsregister/vestiging/000034303162/"}, ' \
            b'{"_display": "Yokata - Lutmastraat 182", ' \
            b'"uri": "handelsregister/vestiging/000033381151/"}, ' \
            b'{"_display": "Volta - Houtmankade 336", ' \
            b'"uri": "handelsregister/vestiging/000029763665/"}, ' \
            b'{"_display": "yolga - Bernard Shawsingel 284", ' \
            b'"uri": "handelsregister/vestiging/000034156488/"}, ' \
            b'{"_display": "ATTA - Von Zesenstraat 179", ' \
            b'"uri": "handelsregister/vestiging/000000343528/"}, ' \
            b'{"_display": "Totta Research N.V. - Burgemeester Stramanweg 105", ' \
            b'"uri": "handelsregister/vestiging/000026200902/"}' \
            b'], ' \
            b'"label": "Vestigingen"}' \
            b']\n'

        mock_hr_response = MockResponse(
            encoding='utf-8',
            status_code=200,
            ok=True,
            url='http://hr.endpoint.internal',
            json_data=mock_json_content)

        when(sessions.Session).request(
            'GET',
            'http://hr.endpoint.internal',
            timeout=0.5,
            stream=False,
            parameters={'q': 'gibberish get'}).thenReturn(mock_hr_response)

        when(sessions.Session).request(
            'GET',
            'http://nap.endpoint.internal',
            timeout=0.5,
            stream=False,
            parameters={'q': 'gibberish get'}).thenReturn(mock_hr_response)

        response = self.app.get('/tr?q=gibberish%20get')

        self.assertEqual(response.status_code, 200, 'api not working')

        self.assertEqual(response.data, expected_response,
                         'api response not quite as expected')
        self.assertEqual(response.content_type, 'application/json',
                         'Verkeerd response type')

    def test_api_typahead_post(self):
        response = self.app.post('/tr', data={'q': 'gibberish post'})
        self.assertEqual(response.status_code, 200, 'api status: OK')
        self.assertEqual(response.data,
                         b'{"get": "you send: gibberish post"}\n',
                         'api response not quite as expected')
        self.assertEqual(response.content_type, 'application/json',
                         'Verkeerd response type')

    def test_str(self):
        sut = TypeAheadResponses([
            TypeAheadResponse(
                'Awesome Section', [
                    Suggestion('urlA', 'displayA'),
                    Suggestion('urlB', 'displayB')]
            )]
        )

        self.assertEqual(json.loads(sut.as_json()), [{
            "label": "Awesome Section",
            "content": [
                {"uri": "urlA", "_display": "displayA"},
                {"uri": "urlB", "_display": "displayB"}
            ]
        }])


if __name__ == '__main__':
    unittest.main()
