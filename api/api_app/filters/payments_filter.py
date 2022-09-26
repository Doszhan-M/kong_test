from types import NoneType
import xmltodict

from datetime import datetime

def payments_filter(xml):
    tmp = xmltodict.parse(xml)
    temp_dict = tmp["answer"]
    result ={}
    result["iin_bin"] = temp_dict.get('IIN_BIN', '')
    result["name_ru"] = temp_dict.get('NameRu', '')
    result["name_kz"] = temp_dict.get('NameKz', '')
    result["payments"] = temp_dict.get('payment', None)
    if type(result["payments"]) not in (list, NoneType):
        result["payments"] = [temp_dict.get('payment', None)]
    return result

