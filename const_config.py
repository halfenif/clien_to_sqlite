
def get_baseurl():
    return 'https://www.clien.net/service/board/park/'

def get_request_type():
    #return "REQUEST"
    return "TOR"

def testseq():
    #return 10718711 # 404 Not Found
    return 10791188

def testseqerror():
    return 10718711 # 404 Not Found

def testurl():
    testurl = get_baseurl() + str(testseq())
    return testurl
