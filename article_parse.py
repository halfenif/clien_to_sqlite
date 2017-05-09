import const_config
import re
import requests
from bs4 import BeautifulSoup

baseurl = const_config.get_baseurl()

def parse_article(strseq):
    status_code = ''
    resutl_title = ''
    resutl_time = ''
    resutl_body = ''
    result_user = ''

    try:
        request_return = requests.get(baseurl + strseq)

        status_code = str(request_return.status_code)

        if status_code == '200':
            try:
                out = request_return.text
                resutl_title = re.findall('<title>(.*)</title>', out)[0]
                lxml = BeautifulSoup(out,'lxml')
                resutl_time = lxml.find('div', attrs={"class": "post-time"}).text.strip()
                resutl_body = lxml.find('div', attrs={"class": "post-article fr-view"}).text
                result_user = lxml.find('button', attrs={"class": "dropdown-toggle nick"}).text.strip()

            except Exception as e:
                print('Parse Exception:' + baseurl + strseq)
                resutl_title = 'Parse Error'
                resutl_body = 'Exception:' + str(e)

    except Exception as e:
        print('Request Exception:' + baseurl + strseq)
        resutl_title = 'Request Error'
        resutl_body = 'Exception:' + str(e)

    return status_code, resutl_time, result_user, resutl_title, resutl_body


#---------------------------------
# Test Suit
if __name__ == "__main__":
    status_code, resutl_time, result_user, resutl_title, resutl_body = parse_article( str(const_config.testseq()))

    print('Status Code:' + status_code)
    print('Post Datetime:' + resutl_time)
    print('Post User:' + result_user)
    print('Title:' + resutl_title)
    print('Body:' + resutl_body)
