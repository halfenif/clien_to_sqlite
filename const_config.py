def get_baseurl():
    return 'https://www.clien.net/service/board/'

def get_boardurl():
    return 'https://www.clien.net/service/group/board_all/'

def get_cmurl():
    return 'https://www.clien.net/service/group/cm_all/'

def get_userurl():
    return 'https://www.clien.net/service/popup/userInfo/basic/'

def get_url_by_seq(bbsclass, seq):
    return get_baseurl() + bbsclass + '/' + str(seq)

def get_start_port():
    return 7001 #Reserved

def get_agent_count():
    return 3

def get_target_make_count():
    return 1000

def get_agent_reset_count():
    return 200

def get_temp_cache_folder():
    return './data_tor/'

def testseq():
    #return 10718711 # 404 Not Found
    return 10791188

def testseqerror():
    return 10718711 # 404 Not Found

def testurl():
    testurl = get_url_by_seq(testseq())
    return testurl
