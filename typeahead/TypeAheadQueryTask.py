import logging
from typing import Dict, List, Any

import grequests
from gevent import monkey
from grequests import AsyncRequest

import conf
from model.typeaheadresponse import TypeAheadResponse, Suggestion, \
    TypeAheadResponses

monkey.patch_all(thread=False, select=False)

_U = 'uri'
_D = '_display'
_C = 'content'


class TypeAheadQueryTask:
    def __init__(self, query: str, overall_timeout: float) -> None:
        self.overall_timeout = overall_timeout
        self.query = query
        self.logger = logging.getLogger(__name__)
        self.session = grequests.Session()
        self.upstream_info = self.get_internal_typeahead_endpoints()

    def work(self) -> TypeAheadResponses:
        requests = []  # type: List[AsyncRequest]
        response = TypeAheadResponses()

        # Don't relay empty queries
        if not self.query or len(self.query.strip()) < conf.MIN_CHARACTERS:
            return response

        for name, endpoint_info in self.upstream_info.items():
            requests.append(
                grequests.get(
                    self.get_endpoint(endpoint_info),
                    timeout=endpoint_info['timeout'],
                    session=self.session,
                    hooks={
                        'response': self._get_response_handler(name, response)
                    },
                    headers={
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                )
            )

        grequests.map(
            requests,
            exception_handler=self._err_handler,
            gtimeout=self.overall_timeout)

        return response

    def get_endpoint(self, endpoint_info):
        q_url = endpoint_info['endpoint'] + '?q={q}'.format(q=self.query)
        self.logger.debug('Query url: {u}'.format(u=q_url))
        return q_url

    def _err_handler(self, request: grequests.AsyncRequest,
                     exception: Exception) -> None:
        self.logger.exception(
            "Problem getting upstream typeahead info {url}".format(
                url=request.url),
            exc_info=exception
        )

    def _get_response_handler(self, key, result_holder, *args, **kwargs):
        def _response_handler(response, *args, **kwargs):
            if response is not None and response.ok and response.status_code == 200:
                settings = self.upstream_info[key]
                maxresults = settings['maxresults']
                weight = settings['weight']
                for res in response.json():
                    suggs = [Suggestion(sug[_U], sug[_D]) for sug in res[_C]][:maxresults]
                    result_holder.add_response(
                        TypeAheadResponse(res['label'], suggs, weight))

        return _response_handler

    @staticmethod
    def get_internal_typeahead_endpoints() -> Dict[str, Dict[str, Any]]:
        """
        For simplicity these urls are now hardcoded. However the should be
        pulled from consul and services providing typeahead should register with
        consul. This will allow for graceful degradation of services if one or
        more endpoints are down.

        :return: A dict: name -> endpoint containing all available endpoints.
        """

        return conf.UPSTREAM_CONFIG
