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

        for name, endpoint_info in self.upstream_info.items():
            requests.append(
                grequests.get(
                    self.get_endpoint(endpoint_info),
                    timeout=endpoint_info['timeout'],
                    session=self.session,
                )
            )

        results = grequests.map(
            requests,
            exception_handler=self._handler,
            gtimeout=self.overall_timeout)

        for result in results:
            if result is not None and result.ok:
                self.logger.debug(result.text)
                for res in result.get_json():
                    suggs = [Suggestion(sug[_U], sug[_D]) for sug in res[_C]]
                    response.add_response(
                        TypeAheadResponse(res['label'], suggs))

        return response

    def get_endpoint(self, endpoint_info):
        q_url = endpoint_info['endpoint'] + '?q={q}'.format(q=self.query)
        self.logger.debug('Query url: {u}'.format(u=q_url))
        return q_url

    def _handler(self, request: grequests.AsyncRequest,
                 exception: Exception) -> None:
        self.logger.exception(
            "Problem getting upstream typeahead info {url}".format(
                url=request.url),
            exc_info=exception
        )

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