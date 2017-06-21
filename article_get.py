import sys
import const_config
import html
import re
import requests
from bs4 import BeautifulSoup

import article_get_by_request
import article_get_by_tor

def get_article(url, socket_port):
    status_code = ''
    resutl_context = ''

    try:
        if const_config.get_request_type() == "TOR":
            if socket_port == '':
                print('Socket Port Argument is Empty.')
            else:
                status_code, resutl_context = article_get_by_tor.get_article(url, socket_port)
        elif const_config.get_request_type() == "REQUEST":
            status_code, resutl_context = article_get_by_request.get_article(url)
        else:
            print('Not Defined Request Type:', const_config.get_request_type())

    except Exception:
        print('Request Exception', sys.exc_info()[0])

    return status_code, resutl_context


def __test__(url):
    tor_process = None
    socket_port = ''

    status_code =''
    resutl_context = ''


    try:
        if const_config.get_request_type() == "TOR":
            tor_process, socket_port = article_get_by_tor.get_tor_process()

        status_code, resutl_context = get_article( url, socket_port)

    finally:
        if const_config.get_request_type() == "TOR":
            article_get_by_tor.kill_tor_process(tor_process)

    return resutl_context

#---------------------------------
# Test Suit
if __name__ == "__main__":
    url = const_config.gey_url_by_seq(const_config.testseq())
    print(__test__(url))


    #print('Status Code:', status_code)
    #print('Resut Context:',  resutl_context)
