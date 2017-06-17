import db_article
import db_error
import article_parse
import sys

#---------------------------------
# Test Suit
if __name__ == "__main__":
    seq = db_article.sqlGetMinSeq()
    print('start seq:' + str(seq))

    while seq > 0:
        seq = seq - 1

        status_code, resutl_time, result_user, resutl_title, resutl_body = article_parse.parse_article(str(seq))
        if status_code == '200':
            db_article.insertItem(seq, resutl_title, resutl_body, resutl_time, result_user)
        # else:
        #     db_error.insertItem(seq)



        if (seq % 100) == 0:
            print('seq:' + str(seq))

        sys.stdout.flush()
