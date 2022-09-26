from os import getenv
from time import sleep
from requests import request
from datetime import datetime

from filters.payments_filter import payments_filter


def api_payments_parser(bin, start_date, try_counts=2):
    ''' https://kgd.gov.kz/ru/content/api-servis-po-predostavleniyu-informacii-ob-uplachennyh-summah-na-licevom-schete
    '''
    url = f'http://open.egov.kz/proxy2/culs_payments?token={getenv("DATA_EGOV_API")}'
    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \
        \n<sign:Request xmlns:sign=\"http://xmlns.kztc-cits/sign\" xmlns:ds=\"http://www.w3.org/2000/09/xmldsig#\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"> \
        \n<sign:IIN_BIN>" + bin + "</sign:IIN_BIN> \
        \n<sign:BeginDate>" + start_date + "</sign:BeginDate> \
        \n<sign:EndDate>" + str(datetime.now().date()) + "</sign:EndDate>  \
        \n</sign:Request>"
    headers = {
        'User-Agent': 'CUPA-uchet',
        'Content-Type': 'application/xml'
    }
    response = request("POST", url, headers=headers, data=payload)
    counts = 0
    if response.status_code != 200 and counts < try_counts:
        sleep(2 * 60)
        try_counts -= 1
        return api_payments_parser(bin, start_date, try_counts)
    return payments_filter(response.text)
