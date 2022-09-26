def delete_useless(dict):
    pop_list = ["edw:bccNameKz", "@xmlns:edw", "edw:messageId",
                "edw:sendTime", "edw:responseCode", "ds:Signature"]
    for elem in pop_list:
        try:
            dict.pop(elem)
        except:
            pass
    return dict

# Filter all data and get it back!


def tax_debt_agreement_filter(dict):
    try:
        # Delete all useless
        delete_useless(dict["edw:response"])
        # Check is it list?
        if type(dict["edw:response"]["edw:taxOrgInfo"]) == list:
            # Delete all useless in list
            list(map(delete_useless, dict["edw:response"]["edw:taxOrgInfo"]))
        else:
            # Set it as list
            dict["edw:response"]["edw:taxOrgInfo"] = [dict["edw:response"]["edw:taxOrgInfo"]]
            # Delete all useless in list
            list(map(delete_useless, dict["edw:response"]["edw:taxOrgInfo"]))

        for element in dict["edw:response"]["edw:taxOrgInfo"]:
            try:
                # Check is it list?
                if type(element["edw:taxPayerInfo"]["edw:bccArrearsInfo"]) == list:
                    # Set new value
                    element["edw:taxPayerInfo"] = element["edw:taxPayerInfo"]["edw:bccArrearsInfo"]
                else:
                    # Set it as list
                    element["edw:taxPayerInfo"]["edw:bccArrearsInfo"] = [
                        element["edw:taxPayerInfo"]["edw:bccArrearsInfo"]]
                    # Set new value
                    element["edw:taxPayerInfo"] = element["edw:taxPayerInfo"]["edw:bccArrearsInfo"]
            except Exception as ex:
                print("TaxPayerInfo probably not found!")
                print(ex)
        result = {
            "iin_bin": dict["edw:response"]["edw:iinBin"],
            "comp_name": dict["edw:response"]["edw:nameRu"],
            "totalArrear": dict["edw:response"]["edw:totalArrear"],
            "totalTaxArrear": dict["edw:response"]["edw:totalTaxArrear"],
            "pensionContributionArrear": dict["edw:response"]["edw:pensionContributionArrear"],
            "socialContributionArrear": dict["edw:response"]["edw:socialContributionArrear"],
            "socialHealthInsuranceArrear": dict["edw:response"]["edw:socialHealthInsuranceArrear"],
            "taxOrgInfo": dict["edw:response"]["edw:taxOrgInfo"]
        }
        change_name(result)
    except Exception as e:
        print(e)
        result = {
            "iin_bin": dict["edw:response"]["edw:iinBin"],
            "comp_name": dict["edw:response"]["edw:nameRu"],
            "totalArrear": dict["edw:response"]["edw:totalArrear"],
            "totalTaxArrear": dict["edw:response"]["edw:totalTaxArrear"],
            "pensionContributionArrear": dict["edw:response"]["edw:pensionContributionArrear"],
            "socialContributionArrear": dict["edw:response"]["edw:socialContributionArrear"],
            "socialHealthInsuranceArrear": dict["edw:response"]["edw:socialHealthInsuranceArrear"],
            "taxOrgInfo": None
        }
    finally:
        return result


def change_name(dict):
    ''' Delete "edw:" in all keys!
    '''
    tax_org_list = []
    for element in dict["taxOrgInfo"]:
        try:
            # print("ELEMENT = ", element)
            if type(element["edw:taxPayerInfo"]) == list:
                tax_payer_list = []
                for elem in element["edw:taxPayerInfo"]:
                    # print("ELEM = ", elem)
                    bcc_dict = {}
                    for el in elem:
                        bcc_dict[el[4:]] = elem[el]
                        # print("DICT = ", bcc_dict)
                    tax_payer_list.append(bcc_dict)
                    # print("LIST = ", tax_payer_list)
                element["edw:taxPayerInfo"] = tax_payer_list
                # print("ELEMENT2 = ", element)
                tax_org_dict = {}
                for elem in element:
                    tax_org_dict[elem[4:]] = element[elem]
                tax_org_list.append(tax_org_dict)
            else:
                tax_org_dict = {}
                for elem in element:
                    tax_org_dict[elem[4:]] = element[elem]
                tax_org_list.append(tax_org_dict)
        except Exception as ex:
            tax_org_dict = {}
            for elem in element:
                tax_org_dict[elem[4:]] = element[elem]
            tax_org_list.append(tax_org_dict)
            print(ex)
        finally:
            dict["taxOrgInfo"] = tax_org_list
