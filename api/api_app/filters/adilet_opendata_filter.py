def adilet_opendata_filter(dicti):
    my_list = []
    try:
        rows = dicti["soap:Envelope"]["soap:Body"]["ns1:requestResponse"]["response"]["responseData"]["data"]["rows"]
        for row in rows:
            my_dict = {}
            for element in row:
                if type(row[element]) == dict:
                    my_dict[element] = None
                else:
                    my_dict[element] = row[element]
            my_dict.pop("execProc")
            my_dict.pop("execProcNum")
            my_dict.pop("iinOrBin")
            my_list.append(my_dict)
        return my_list
    except Exception:
        return []
