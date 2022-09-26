import xmltodict
from os import getenv
from requests import request

from filters.tax_debt_agreement_filter import tax_debt_agreement_filter



def tax_debt_agreement_parser(iin_bin, try_counts=2):
    ''' https://data.egov.kz/datasets/view?index=tax_debt_agreement
    '''
    url = f'http://open.egov.kz/proxy2/tax_debt_agreement?token={getenv("DATA_EGOV_API")}'
    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<sign:request xmlns:sign=\"http://xmlns.kztc-cits/sign\">\n<sign:iinBin>" + iin_bin + "</sign:iinBin>\n</sign:request>"
    headers = {
        'User-Agent': 'CUPA-uchet',
        'Content-Type': 'application/xml'
    }
    response = request("POST", url, headers=headers, data=payload)
    counts = 0
    if response.status_code != 200 and counts < try_counts:
        try_counts -= 1
        return tax_debt_agreement_parser(iin_bin, try_counts)
    tmp = xmltodict.parse(response.text)
    return tax_debt_agreement_filter(tmp)
