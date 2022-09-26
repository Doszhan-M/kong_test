import xmltodict


def accurals_filter(xml):
    tmp = xmltodict.parse(xml)
    temp_dict = tmp["answer"]
    new_dict ={}
    new_dict["iin_bin"] = temp_dict.get('IIN_BIN', '')
    new_dict["comp_name"] = temp_dict.get('NameRu', '')
    new_dict["items"] = temp_dict.get('items', None)
    return new_dict
