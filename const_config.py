def get_dbms():
    return 'c:/temp/db_clien.db'

def get_baseurl():
    return 'https://www.clien.net/service/board/park/'

def get_type():
    #return "REQUEST"
    return "TOR"

def testseq():
    #return 10718711 # 404 Not Found
    return 10843438

def testseqerror():
    return 10718711 # 404 Not Found

def testurl():
    testurl = get_baseurl() + str(testseq())
    return testurl
