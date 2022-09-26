from requests import request
from logging import  getLogger

from filters.elicense_filter import elicense_filter


logger = getLogger('fastapi')


def elicense_parser(bin: str, try_counts=2):
    ''' https://elicense.entry.kz/docs
    '''    
    url = 'https://elicense.entry.kz/api/license?iin_bin={}'.format(bin)
    response = request("GET", url)
    if response.status_code == 200:
        data = elicense_filter(response.text)
        return data
    elif response.status_code != 200 and try_counts > 0:
        try_counts -= 1
        return elicense_parser(bin, try_counts)
    else:
        logger.error(f'Elicense error status_code {response.status_code}')