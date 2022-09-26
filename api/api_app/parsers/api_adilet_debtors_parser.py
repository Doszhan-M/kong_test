import time
from os import getenv
from requests import request

from filters.adilet_debtors_filter import adilet_debtors_filter


CAPTCHATOKEN = getenv("2CAPTCHATOKEN")


def adilet_debtors_parse(iin_bin):
    ''' https://aisoip.adilet.gov.kz/debtors
    '''
    cap = False
    while cap == False:
        # 2capcha v3
        solve = request('GET',
            f"http://2captcha.com/in.php?key={CAPTCHATOKEN}&method=userrecaptcha&version=v3&action=findErd&min_score=0.3&googlekey=6LdPj8YZAAAAAF94C16Pd93KT8a_TCy-XihB4CBL&pageurl=https://aisoip.adilet.gov.kz/debtors&json=1"
            )
        id = int(solve.json()["request"])
        time.sleep(10)
        tokken = request('GET', f"http://2captcha.com/res.php?key={CAPTCHATOKEN}&action=get&json=1&id={id}")
        g_response = tokken.json()["request"]
        # 2capcha v3 end
        payload = '''{"iin":"","bin":'''+f'''"{iin_bin}","fullName":"","searchType":1,"docNum":"",''' + \
            f'''"captcha":"{g_response}",'''+'''"action":"findErd"}'''
        headers = {
            'Content-Type': 'application/json'
        }
        response = request("POST", headers=headers, data=payload, 
            url="https://aisoip.adilet.gov.kz/rest/debtor/findErd?ignoreCaptcha=false&page=0&size=10",
        )
        for el in response.json():
            if el == "error":
                cap = False
            elif el == "content":
                cap = True
    if response.json()["pagination"]["empty"] == True:
        return {'iin_bin': iin_bin}
    elif response.json()["pagination"]["empty"] == False:
        return adilet_debtors_filter(response.json()["content"], iin_bin)
