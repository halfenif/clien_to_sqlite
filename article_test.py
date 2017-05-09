import const_config
import article_parse
import db_article

#---------------------------------
# Test Suit
if __name__ == "__main__":

    if db_article.sqlExistCheck(const_config.testseq()):
        print('Exist Article:' + str(const_config.testseq()))
    else:
        status_code, resutl_time, result_user, resutl_title, resutl_body = article_parse.parse_article(str(const_config.testseq()))
        db_article.sqlInsert(const_config.testseq(), resutl_title, resutl_body, resutl_time, result_user)
        print('Insert Article:' + const_config.testurl())
