##news_crawler

감정 분석을 하기 위한 커뮤니티를 크롤링합니다.

#### Description
ZUM의 실시간 반응을 이용해서 커뮤니티 반응을 가져옵니다. 
(http://search.zum.com/search.zum?method=realtime&option=accu&qm=f_typing&query=)

1. **Selenium**을 이용해 다이나믹 스크롤링을 적용한 웹에서 각 커뮤니티의 URL을 가져옵니다.
2. URL을 통해 requests한 뒤, BeautifulSoup로 컨텐츠를 크롤링합니다.
3. 감정 분석을 하고 파일에 저장합니다.

#### Requirement
**Python3**를 통해 실행해야 합니다.
