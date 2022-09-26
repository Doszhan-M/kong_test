from os import getenv
from requests import request


def participant_filter(response, bin):
    try:
        response['iin_bin'] = bin
        response['is_participant'] = True
    except TypeError:
        response = {
            'iin_bin': bin,
            'is_participant': False
        }
    finally:
        return response


def parse_ref_reasons(try_counts=2):
    ''' Список причин включения в реестр
    '''
    url = 'https://ows.goszakup.gov.kz/v3/refs/ref_reason'
    headers = {'Authorization': 'Bearer ' + getenv("GOSZAKUP_API")}
    response = request("GET", url, headers=headers, data={}, verify=False)
    counts = 0
    if response.status_code != 200 and counts < try_counts:
        try_counts -= 1
        return parse_ref_reasons(bin, try_counts)
    return response.json()['items']


def unrelaible_filter(response, bin):
    try:
        result = response['items'][0]
        result['iin_bin'] = bin
        result.pop('id')
        ref_reasons = parse_ref_reasons()
        for reason in ref_reasons:
            if reason.get('id') == result['ref_reason_id']:
                result['ref_reason'] = reason['name_ru']
                break
        result['is_unrelaible'] = True
    except KeyError:
        result = {
            'iin_bin': bin,
            'is_unrelaible': False
        }
    finally:
        return result
