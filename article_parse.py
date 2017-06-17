import const_config
import html
import re
import requests
from bs4 import BeautifulSoup

import article_get_by_request
import article_get_by_tor

baseurl = const_config.get_baseurl()

def parse_article(strseq):
    status_code = ''
    resutl_title = ''
    resutl_time = ''
    resutl_body = ''
    result_user = ''

    try:
        out = '' #init

        if const_config.get_request_type() == "TOR":
            socket_port = article_get_by_tor.get_socket_port()
            status_code, out = article_get_by_tor.get_article(strseq, socket_port)
        elif const_config.get_request_type() == "REQUEST":
            status_code, out = article_get_by_request.get_article(strseq)
        else:
            print('Not Defined Request Type:', const_config.get_request_type())
            return

        if status_code == '200':
            try:
                resutl_title = re.findall('<title>(.*)</title>', out)[0]
                resutl_title = html.unescape(resutl_title.replace(' : 클리앙','').replace('\0','').strip())


                #print('resutl_title:', resutl_title)
                lxml = BeautifulSoup(out,'lxml')
                resutl_time = lxml.find('div', attrs={"class": "post-time"}).text.strip()
                resutl_body = html.unescape(lxml.find('div', attrs={"class": "post-article fr-view"}).text.replace('\0','').strip())
                result_user = lxml.find('button', attrs={"class": "dropdown-toggle nick"}).text.strip()

            except Exception as e:
                print('Parse Exception')
                resutl_title = 'Parse Error'
                resutl_body = 'Exception:' + str(e)

    except Exception as e:
        print('Request Exception')
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
