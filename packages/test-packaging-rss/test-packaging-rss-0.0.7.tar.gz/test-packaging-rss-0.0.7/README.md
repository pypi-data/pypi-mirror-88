# test-packaging-rss

패키징 Test  

Test Pypi Link:  
https://test.pypi.org/project/test-packaging-rss/  

Pypi:  
https://pypi.org/project/test-packaging-rss  
  
  
## Installation
<pre>
<code>
  $ python - m pip install -i https://test.pypi.org/simple/ test-packaging-rss
  $ python - m pip install feedparser
</code>
</pre>
  
  
## Installation2 
<pre>
<code>
  $ python - m pip install --upgrade test-packaging-rss
</code>
</pre>

## Example

<pre>
<code>
  $ python
  >>> import test_rss_pkg  
  test rss pkg loaded  
  >>> import test_rss_pkg.RSSreader  
  RSSreader.py loaded  
  >>> import test_rss_pkg.example
  example loaded
  >>> test_rss_pkg.example.try_example()
  status:  200
  RSS에 새로운 공시가 올라옴 : 
  ('(코스닥)KMH - 소송등의제기ㆍ신청(경영권분쟁소송) (주주총회 개최금지 가처분)', 'http://dart.fss.or.kr/api/link.jsp?rcpNo=20201210900523', datetime.datetime(2020, 12, 10, 7, 49, tzinfo=tzutc()), 'KMH')
  RSS에 새로운 공시가 올라옴 : 
  ('(기타)한국투자캐피탈 - 일괄신고추가서류', 'http://dart.fss.or.kr/api/link.jsp?rcpNo=20201210000423', datetime.datetime(2020, 12, 10, 7, 48, tzinfo=tzutc()), '한국투자캐피탈')
</code>
</pre>
