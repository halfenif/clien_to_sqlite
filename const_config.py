import logging

def set_log_level():
    logging.basicConfig(level=logging.DEBUG)

def get_baseurl():
    return 'https://www.clien.net/service/board/'

def get_bbs_class():
    return 'park'

def gey_url_by_seq(seq):
    return get_baseurl() + get_bbs_class() + '/' + str(seq)

def get_request_type():
    #strType = "REQUEST"
    strType = "TOR"
    return strType

def testseq():
    #return 10718711 # 404 Not Found
    return 10791188

def testseqerror():
    return 10718711 # 404 Not Found

def testurl():
    testurl = get_baseurl() + str(testseq())
    return testurl
