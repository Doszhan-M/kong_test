from os import getenv
from requests import request

from filters.gos_zakup_filter import participant_filter, unrelaible_filter


def parse_participant(bin, try_counts=2):
    ''' https://ows.goszakup.gov.kz 
    '''
    url = f'https://ows.goszakup.gov.kz/v3/subject/biin/{bin}'
    headers = {'Authorization': 'Bearer ' + getenv("GOSZAKUP_API")}
    response = request("GET", url, headers=headers, data={}, verify=False)
    counts = 0
    if response.status_code != 200 and counts < try_counts:
        try_counts -= 1
        return parse_participant(bin, try_counts)
    return participant_filter(response.json(), bin)


def parse_unrelaible_participant(bin, try_counts=2):
    ''' https://ows.goszakup.gov.kz
    '''
    url = f'http://ows.goszakup.gov.kz/v3/rnu/{bin}'
    headers = {'Authorization': 'Bearer ' + getenv("GOSZAKUP_API")}
    response = request("GET", url, headers=headers, data={}, verify=False)
    counts = 0
    if response.status_code != 200 and counts < try_counts:
        try_counts -= 1
        return parse_unrelaible_participant(bin, try_counts)
    return unrelaible_filter(response.json(), bin)
