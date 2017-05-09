import db_article
import db_error
import article_parse
import time

cnt_error = 0

def get_seq():
    seq = db_article.sqlGetMaxSeq()
    seq = seq + 1
    print('Start seq:' + str(seq))

    cnt_error = 0 #Reset Error
    print('Reset Error:' + str(cnt_error))
    return seq


#---------------------------------
# Test Suit
if __name__ == "__main__":
    seq = get_seq() #Check Seq

    while True:
        status_code, resutl_time, result_user, resutl_title, resutl_body = article_parse.parse_article(str(seq))
        if status_code == '200':
            db_article.insertItem(seq, resutl_title, resutl_body, resutl_time, result_user)
            cnt_error = 0 #Reset Error
        else:
            cnt_error = cnt_error + 1 #
            if cnt_error >= 100:
                print('Reset seq:' + str(seq))
                time.sleep(1 * 60 * 10) #wait
                seq = get_seq()

        seq = seq + 1 #Next

        if (seq % 10) == 0:
            print('seq:' + str(seq))
