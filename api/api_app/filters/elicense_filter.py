from json import loads


def elicense_filter(data):
    result = loads(data)
    result['iin_bin'] = result['bin']
    result.pop('bin')
    return result