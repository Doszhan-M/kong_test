from ast import Return
from os import getenv
from requests import request

from filters.accurals_filter import accurals_filter


def accruals_parser(bin, try_counts=2):
    ''' https://kgd.gov.kz/ru/content/salyk-toleushi-esepteu-kyzmeti-zher-mulik-kolik-api-servisi-1
    '''
    url=f'http://open.egov.kz/proxy2/culs_accruals?token={getenv("DATA_EGOV_API")}'
    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<sign:Request xmlns:sign=\"http://xmlns.kztc-cits/sign\" xmlns:ds=\"http://www.w3.org/2000/09/xmldsig#\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n<sign:IIN_BIN>" + bin + "</sign:IIN_BIN>\n</sign:Request>"
    headers = {
        'User-Agent': 'CUPA-uchet',
        'Content-Type': 'application/xml'
    }
    response = request("POST", url, headers=headers, data=payload)
    counts = 0
    if response.status_code != 200 and counts < try_counts:
        try_counts -= 1
        return accruals_parser(bin, try_counts)
    data = accurals_filter(response.text)
    return data
