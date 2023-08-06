import RSSreader
from dateutil.parser import parse


date_tracker = parse("Mon, 1 Jan 1000 00:00:01 GMT")
feed, time_tracker = RSSreader.new_rss(date_tracker)

