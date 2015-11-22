##handle_review

크롤링한 네이버 영화 리뷰를 분류하고, 감정 사전을 만들기 위한 코드입니다.
* dictionary.py
* reprocess.py
로 구성되어 있습니다.

### *dictionary.py
크롤링한 네이버 영화 리뷰를 분류하고, 감정 사전을 만들기 위한 코드입니다.

#### Description
실행 루틴은 다음과 같습니다.
1. 크롤링된 영화 리뷰를 별점에 의해 분류합니다.
2. 이 때 0~3점은 부정적, 8~10점은 긍정적으로 분류합니다. (나머지는 버립니다.)
3. 분류된 영화 리뷰를 바탕으로 감정 사전(sentiment dictionary)를 구축합니다.

* 형태소 분석(태깅)을 위해 konlpy의 Mecab 태거를 사용했습니다.
* 리뷰를 분석해 csv파일의 감정 사전으로 변환합니다.

#### Requirement
dictionary.py는 **Python3**를 통해 실행해야 합니다.

### *reprocess.py
json형태의 리뷰 데이터를 txt 형태로 변환합니다.
이 때, 부정적, 긍정적이 아닌 리뷰는 제외합니다.

#### Requirement
dictionary.py는 **Python3**를 통해 실행해야 합니다.