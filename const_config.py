def get_dbms():
    return 'e:/db_clien.db'

def get_baseurl():
    return 'https://www.clien.net/service/board/park/'

def testseq():
    #return 10718711 # 404 Not Found
    return 10719920

def testseqerror():
    return 10718711 # 404 Not Found

def testurl():
    testurl = get_baseurl() + str(testseq())
    return testurl
