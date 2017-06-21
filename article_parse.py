import sys
import const_config
import html
import re
import requests
from bs4 import BeautifulSoup

import article_get

def parse_article(content):
    resutl_title = ''
    resutl_pubdate = ''
    resutl_body = ''
    result_user = ''

    try:
        resutl_title = re.findall('<title>(.*)</title>', content)[0]
        resutl_title = html.unescape(resutl_title.replace(' : 클리앙','').replace('\0','').strip())
        #print('resutl_title:', resutl_title)

        lxml = BeautifulSoup(content,'lxml')
        resutl_pubdate = lxml.find('div', attrs={"class": "post-time"}).text.strip()
        resutl_body = html.unescape(lxml.find('div', attrs={"class": "post-article fr-view"}).text.replace('\0','').strip())
        result_user = lxml.find('button', attrs={"class": "dropdown-toggle nick"}).text.strip()

    except Exception as e:
        print('Parse Exception:', sys.exc_info()[0])


    return resutl_title, resutl_body, resutl_pubdate, result_user


#---------------------------------
# Test Suit
if __name__ == "__main__":
    
    url = const_config.get_baseurl() + const_config.get_bbs_class() + '/' + str(const_config.testseq())
    status_code, resutl_pubdate, result_user, resutl_title, resutl_body = article_get.get_article(url)

    print('Status Code:', status_code)
    print('Post Datetime:', resutl_pubdate)
    print('Post User:', result_user)
    print('Title:', resutl_title)
    print('Body:', resutl_body)
