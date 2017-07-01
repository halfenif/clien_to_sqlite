def get_baseurl():
    return 'https://www.clien.net/service/board/'

def get_bbs_class():
    return 'park'

def get_url_by_seq(seq):
    return get_baseurl() + get_bbs_class() + '/' + str(seq)

def get_start_port():
    return 7000 #Reserved

def get_agent_count():
    return 40

def get_temp_cache_folder():
    return './data_tor/'

def testseq():
    #return 10718711 # 404 Not Found
    return 10791188

def testseqerror():
    return 10718711 # 404 Not Found

def testurl():
    testurl = get_baseurl() + str(testseq())
    return testurl
