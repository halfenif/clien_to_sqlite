import sys
import const_config
import article_get
import article_parse
import db_article
import article_get_by_tor

#---------------------------------
# Main Suit
if __name__ == "__main__":
    seq = db_article.sqlGetMinSeq()
    print('start seq:' + str(seq))

    try:
        if const_config.get_request_type() == "TOR":
            tor_process, socket_port = article_get_by_tor.get_tor_process()

        while seq > 0:
            seq = seq - 1
            url = const_config.get_baseurl() + str(seq)

            if const_config.get_request_type() == "TOR":
                status_code, resutl_context = article_get_by_tor.get_article(url, socket_port)

            if status_code == '200':
                resutl_title, resutl_body, resutl_time, result_user = article_parse.parse_article(resutl_context)
                db_article.insertItem(seq, resutl_title, resutl_body, resutl_time, result_user)

            if (seq % 100) == 0:
                print('seq:' + str(seq))

            sys.stdout.flush()

    finally:
        if const_config.get_request_type() == "TOR":
            article_get_by_tor.kill_tor_process(tor_process)
