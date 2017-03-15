from model.typeaheadresponse import TypeAheadResponse, Suggestion


def get_type_ahead_response(data, result_holder, maxresults, weight):
    """
    Default type ahead response
    :param data:
    :param result_holder:
    :param maxresults:
    :param weight:
    :return:
    """
    _U = 'uri'
    _D = '_display'
    _C = 'content'

    for res in data:
        suggs = [Suggestion(sug[_U], sug[_D]) for sug in res[_C]][:maxresults]
        if len(suggs) > 0:
            result_holder.add_response(
                TypeAheadResponse(res['label'], suggs, weight))


def get_catalogus_type_ahead_response(data, result_holder, maxresults, weight):
    """
    type ahead response for Catalogus
    :param data:
    :param result_holder:
    :param maxresults:
    :param weight:
    :return:
    """
    _U = 'id'
    _D = 'title'
    _C = 'results'
    suggs = []
    for res in data['result'][_C][:maxresults]:
        suggs.append(
            Suggestion(f"catalogus/api/3/action/package_show?id={res[_U]}", res[_D])
        )
    if len(suggs) > 0:
        result_holder.add_response(
            TypeAheadResponse("Datasets", suggs, weight))
