import sys
import argparse
import requests
import re
from itertools import count
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import const_config
import article_get_by_tor
import db_article_index
import z_utils

def get_list(bbs_class, socket_port, startpage=0, processid=0, filewrite=False):
    for page in count(startpage):
        url = urljoin(const_config.get_baseurl(), bbs_class) + '?po=' + str(page)

        if const_config.get_request_type() == "TOR":
            status_code, resutl_context = article_get_by_tor.get_article(url, socket_port)

        if status_code != '200':
            print('End Status Code:', status_code)
            return

        html = resutl_context
        #print(html)
        if filewrite:
            z_utils.strToFile(html, 'BBSList', 'html')

        soup = BeautifulSoup(html, 'html.parser')

        for article in soup.find_all('a', attrs={"class": "list-subject"}):
            #url_path_split= list(filter(lambda x:x,re.split('[/]',re.sub(r':?service|board','',urlparse(article['href']).path))))
            url_path_split = [x for x in re.sub(r':?service|board','',urlparse(article['href']).path).split('/') if x]

            #title = article.text.replace('\0','').strip()
            #print(url_path_split, title)

            if url_path_split[0] == bbs_class:
                db_article_index.insertItem(int(url_path_split[1]), bbs_class, startpage, processid)


#---------------------------------
# Batch Suit
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crawing BBS')
    parser.add_argument('-s', dest='startpage', action='store', type=int, required=True,
                       help='BBS Start Page(po=?)')
    parser.add_argument('-p', dest='processid', action='store', type=int, required=True,
                       help='Process ID for Monitoring')

    parser.add_argument('-f', dest='filewrite', action='store_true',
                       help='Request Out to Write File')

    args = parser.parse_args()

    #print('{}'.format(args))
    # print(args.filewrite)
    # sys.exit(0)

    try:
        if const_config.get_request_type() == "TOR":
            tor_process, socket_port = article_get_by_tor.get_tor_process()

        get_list('park', socket_port, args.startpage, args.processid, args.filewrite) #InitValue

    finally:
        if const_config.get_request_type() == "TOR":
            article_get_by_tor.kill_tor_process(tor_process)
