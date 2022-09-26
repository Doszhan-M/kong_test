import xmltodict
from os import getenv
from requests import request

from filters.adilet_opendata_filter import adilet_opendata_filter


def adilet_opendata_parser(bin, try_counts=2):
    ''' https://aisoip.adilet.gov.kz/debtors 201040000013
    '''
    url = 'https://data.egov.kz/egov-opendata-ws/ODWebServiceImpl'
    api_key = getenv("ADILET_OPENDATA_API")
    payload = f"<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" " \
        f"xmlns:soap=\"http://soap.opendata.egov.nitec.kz/\">\n    <soapenv:Header/>\n    <soapenv:Body>\n        " \
        f"<soap:request>\n            <request>\n                <requestInfo>\n                    " \
        f"<messageId>2464f684-d085-45ac-b63e-9bc951696b39</messageId>\n                    " \
        f"<messageDate>2021-01-16T19:18:14.144+06:00</messageDate>\n                    " \
        f"<indexName>aisoip</indexName>\n                    <apiKey>{api_key}</apiKey>\n                " \
        f"</requestInfo>\n                <requestData>\n                    <data " \
        f"xmlns:ns2pep=\"http://bip.bee.kz/SyncChannel/v10/Types/Request\" " \
        f"xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:type=\"ns2pep:RequestMessage\">\n             " \
        f"           <iinOrBin>{bin}</iinOrBin>\n                    </data>\n                </requestData>\n     " \
        f"       </request>\n        </soap:request>\n    </soapenv:Body>\n</soapenv:Envelope> "
    headers = {
        'Content-Type': 'application/xml',
        'User-Agent': 'PostmanRuntime/7.26.10'
    }
    response = request('POST', url, headers=headers, data=payload, verify=False)
    counts = 0
    if response.status_code != 200 and counts < try_counts:
        try_counts -= 1
        return adilet_opendata_parser(bin, try_counts)
    return adilet_opendata_filter(xmltodict.parse(response.text, dict_constructor=dict))
