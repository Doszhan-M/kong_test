from requests import request


def egov_iin_parser(iin, try_counts=2):
    url = f"https://egov.kz/services/P20.45/rest/gbdfl/persons/{iin}?infotype=short"
    payload={}
    headers = {
        'User-Agent': 'PostmanRuntime/7.28.4',
        'Cookie': 'cookiesession1=678B76BDCDEFGHJKLMNOPQSTUVWX08ED; egov-client-type=PORTAL'
    }
    response = request("GET", url, headers=headers, data=payload)
    counts = 0
    if response.status_code != 200 and counts < try_counts:
        try_counts -= 1
        return egov_iin_parser(iin, try_counts)
    return response.json()
