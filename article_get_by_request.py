import const_config
import re
import requests
from bs4 import BeautifulSoup

baseurl = const_config.get_baseurl()

def get_article(strseq):
    status_code = ''

    try:
        request_return = requests.get(baseurl + strseq)

        status_code = str(request_return.status_code)

        if status_code == '200':
            return request_return.text

    except Exception as e:
        return "Error"

    return status_code, resutl_time, result_user, resutl_title, resutl_body


#---------------------------------
# Test Suit
if __name__ == "__main__":
    out = get_article( str(const_config.testseq()))

    print('Out:', out)