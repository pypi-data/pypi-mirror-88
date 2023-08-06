import feedparser
from dateutil.parser import parse
from datetime import datetime, timedelta
import pandas as pd
import logging.config


def new_rss(date_tracker):
    """
    다트 RSS를 통해 새로 올라온 공시를 가져오고, 공시의 제목, 링크, 날짜, 작성기업을 반환한다.
    RSS 피드의 가장 최신 공시 발표의 날짜와 시간을 가져온다.

    params:
        date_tracker : 지금까지 확인한 날짜/시각 datetime

    return:
        ret : 공시 table 내용을 가지고 옴
        date_tracker : 확인한 가장 최근공시의 날짜/시각 datetime
    """

    url = "http://dart.fss.or.kr/api/todayRSS.xml"
    fp = feedparser.parse(url)
    ret = []
    print("status: ", fp.status)


    # ret.append(('단일판매ㆍ공급계약체결', 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20201028800603', datetime.today(), '아이에스동서'))

    # RSS에 공급계약체결이 없을 시,
    # entry 가장 최근 공시가 위, 내림차순
    # TODO: use feedparser's etag or status code to check modified RSS
    for e in fp.entries:
        if (parse(e.published) <= date_tracker):  # compare date to get new feed
            break
        entry_tuple = (e.title, e.link, parse(e.published), e.author)
        print("RSS에 새로운 공시가 올라옴 : ")
        print(entry_tuple)
        ret.append(entry_tuple)

    print("Checking RSS - new feed(s): " + str(len(ret)))
    return ret, parse(fp.entries[0].published)
