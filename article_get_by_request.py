import const_config
import re
import requests
from bs4 import BeautifulSoup

def get_article(url):
    status_code = ''

    try:
        request_return = requests.get(url)

        status_code = str(request_return.status_code)

        if status_code == '200':
            return request_return.text

    except Exception as e:
        return '-1', "Error"

    return status_code, request_return


#---------------------------------
# Test Suit
if __name__ == "__main__":
    out = get_article( str(const_config.testseq()))

    print('Out:', out)
