from test_rss_pkg import RSSreader
from dateutil.parser import parse

print("example loaded")
def try_example():
  date_tracker = parse("Mon, 1 Jan 1000 00:00:01 GMT")
  feed, time_tracker = RSSreader.new_rss(date_tracker)

