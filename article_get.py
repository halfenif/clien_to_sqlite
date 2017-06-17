import sys
import const_config
import html
import re
import requests
from bs4 import BeautifulSoup

import article_get_by_request
import article_get_by_tor

baseurl = const_config.get_baseurl()

def get_article(strseq, socket_port):
    status_code = ''
    resutl_context = ''

    try:
        if const_config.get_request_type() == "TOR":
            if socket_port == '':
                print('Socket Port Argument is Empty.')
            else:
                status_code, resutl_context = article_get_by_tor.get_article(strseq, socket_port)
        elif const_config.get_request_type() == "REQUEST":
            status_code, resutl_context = article_get_by_request.get_article(strseq)
        else:
            print('Not Defined Request Type:', const_config.get_request_type())

    except Exception:
        print('Request Exception', sys.exc_info()[0])

    return status_code, resutl_context


#---------------------------------
# Test Suit
if __name__ == "__main__":
    tor_process = None
    socket_port = ''

    url = const_config.get_baseurl() + str(const_config.testseq())

    try:
        if const_config.get_request_type() == "TOR":
            tor_process, socket_port = article_get_by_tor.get_tor_process()

        status_code, resutl_context = get_article( url, socket_port)
        status_code, resutl_context = get_article( url, socket_port)
        status_code, resutl_context = get_article( url, socket_port)

    finally:
        if const_config.get_request_type() == "TOR":
            article_get_by_tor.kill_tor_process(tor_process)


    #print('Status Code:', status_code)
    #print('Resut Context:',  resutl_context)
