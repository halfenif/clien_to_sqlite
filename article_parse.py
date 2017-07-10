import sys
import const_config
import html
import re
import requests
from bs4 import BeautifulSoup
import z_utils

import article_get

def parse_article(content, seq=0):
    result = {}
    result['title'] = ''
    result['body'] = ''
    result['postuser'] = ''
    result['pubdate'] = ''

    try:

        #result['title'] = html.unescape(re.find('<title>(.*)</title>', content).replace(' : 클리앙','').replace('\0','').strip())
        #print('resutl_title:', resutl_title)

        lxml = BeautifulSoup(content,'lxml')
        result['title'] = lxml.find('title').text.replace(' : 클리앙','').replace('\0','').strip()
        result['pubdate'] = lxml.find('div', attrs={"class": "post-time"}).text.strip()
        result['body'] = html.unescape(lxml.find('div', attrs={"class": "post-article fr-view"}).text.replace('\0','').strip())
        result['postuser'] = lxml.find('button', attrs={"class": "dropdown-toggle nick"}).text.strip()

    except Exception as e:
        print('Parse Exception:', sys.exc_info()[0])
        print('Parse Exception:', sys.exc_info()[1])
        print('Parse Exception:', sys.exc_info()[2])
        z_utils.strToFile(content,'ParseError_' + str(seq),'html')

    return result


#---------------------------------
# Test Suit
if __name__ == "__main__":

    #url = const_config.get_url_by_seq(const_config.testseq())
    url = const_config.get_url_by_seq(2823857)

    content = article_get.__test__(url)
    result = parse_article(content)

    print('Title:', result['title'])
    print('Body:', result['body'])
    print('Post User:', result['postuser'])
    print('Post Datetime:', result['pubdate'])
