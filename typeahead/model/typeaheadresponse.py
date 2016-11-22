import json
from typing import List, Dict, Any


class Suggestion:
    def __init__(self, url: str, display: str):
        self.url = url
        self.display = display

    def __repr__(self):
        return "Suggestion(url={url}, display={display}".format(
            url=self.url, display=self.display)

    def __hash__(self):
        return hash((self.url, self.display))

    def __eq__(self, other):
        if not isinstance(other, Suggestion):
            return False
        return self.display == other.display and self.url == other.url


class TypeAheadResponse:
    def __init__(self, label: str, suggestions: List[Suggestion], weight):
        self.weight = weight
        self.label = label
        self.suggestions = suggestions

    def as_python(self) -> Dict[str, Any]:
        return {
            'label': self.label,
            'content': [{'_display': s.display,
                         'uri': s.url} for s in self.suggestions]}

    def as_json(self) -> str:
        return json.dumps(self.as_python())

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        return "TypeAheadResponse(label={label}, weight={weight}, " \
               "suggestions={suggestions})" \
            .format(label=self.label,
                    weight=self.weight,
                    suggestions=repr(self.suggestions))

    def __hash__(self):
        return hash((self.label, self.weight, tuple(self.suggestions)))

    def __eq__(self, other):
        if not isinstance(other, TypeAheadResponse):
            return False

        return self.weight == other.weight and self.label == other.label and self.suggestions == other.suggestions


class TypeAheadResponses:
    def __init__(self, responses: List[TypeAheadResponse] = None):
        self.responses = [] if responses is None else responses

    def add_response(self, response: TypeAheadResponse) -> None:
        self.responses += [response]

    def _responses_sorted(self) -> List[TypeAheadResponse]:
        """
        Get all responses sorted by weight. Hight weight means higher in the
        result so order is reverse.
        :return: List[TypeAheadResponse]
        """
        return sorted(self.responses, reverse=True)

    def json_serializable(self) -> Dict[str, Any]:
        return [resp.as_python() for resp in self._responses_sorted()]

    def as_json(self) -> str:
        return json.dumps(self.json_serializable())
