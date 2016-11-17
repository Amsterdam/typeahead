import json
from typing import List, ByteString, Dict, Any


class Suggestion:
    def __init__(self, url: str, display: str):
        self.url = url
        self.display = display


class TypeAheadResponse:
    def __init__(self, label: str, suggestions: List[Suggestion]):
        self.label = label
        self.suggestions = suggestions

    def as_python(self):
        return {
            'label': self.label,
            'content': [{'_display': s.display,
                         'uri': s.url} for s in self.suggestions]}

    def as_json(self) -> str:
        return json.dumps(self.as_python())


class TypeAheadResponses:
    def __init__(self, responses: List[TypeAheadResponse] = None):
        self.responses = [] if responses is None else responses

    def add_response(self, response: TypeAheadResponse):
        self.responses += [response]

    def json_serializable(self)->Dict[str, Any]:
        return [resp.as_python() for resp in self.responses]

    def as_json(self) -> str:
        return json.dumps(self.json_serializable())
