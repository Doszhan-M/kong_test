
def adilet_debtors_filter(dict, iin_bin):
    result = {
        "iin_bin": iin_bin,
        "debts": []
    }
    for elem in dict:
        my_dict = {}
        my_dict["debtor_fullname"] = elem["debtorFullName"]
        my_dict["essense_requirements"] = elem["essenseRequirements"]
        my_dict["ip_start_date"] = elem["ipStartDate"]
        my_dict["ban_start_date"] = elem["banStartDate"]
        my_dict["il_organ_ru"] = elem["ilOrgan_ru"]
        my_dict["il_organ_kk"] = elem["ilOrgan_kk"]
        my_dict["officer_full_name"] = elem["officerFullName"]
        my_dict["officer_phone"] = elem["officerPhone"]
        my_dict["disa_department_name_ru"] = elem["disaDepartmentName_ru"]
        my_dict["disa_department_name_kk"] = elem["disaDepartmentName_kk"]
        my_dict["id"] = elem["id"]
        my_dict["type_data"] = elem["typeData"]
        my_dict["uid"] = elem["uid"]
        
        result['debts'].append(my_dict)
    return result
