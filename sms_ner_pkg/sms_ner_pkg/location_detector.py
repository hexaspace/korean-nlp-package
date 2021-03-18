# -*- coding: utf-8 -*-

import re


def rex_location(sentence):
    resert_sent = ""    #공백 문자열
    #시도, 시군구 정규표현식 이후에 나머지 도로명주소 정규표현식을 적용한다.
    sigurex = re.compile("([가-힣]{2,6}(시|도)).([가-힣]+(시|군|구))")
    rurex = re.compile("((\s[가-힣\d\,\.]+(읍|면|동|가|리|구))|).([가-힣A-Za-z·\d~\-\.]+(로|길)).((지하 |공중 |)[\d]+)((\,(\s[\d]+동|)(\s[\d~]+층|)(\s[\d]+호|))|)((\s|)\([가-힣]+동\)|)")
    #시도, 시군구 적용
    issigu = sigurex.search(sentence)
    #존재한다면 문자열에 추가 후 다음 문자열부터 탐색
    if issigu==None:
        tail_sent = sentence
    else:
        tail_sent = sentence[issigu.end():]
        resert_sent+=issigu.group()
    #읍면구 로길 상세주소 (동) 정규표현식 적용
    isro = rurex.search(tail_sent)
    # 존재할때 문자열에 추가
    if isro != None:
        resert_sent += isro.group()
    #문자열 반환
    return resert_sent

if __name__ == "__main__":
    massages = ["내일 만나서 뭐할까?",
                  "만나서 영화 보는거 어때",
                  "좋아 그럼 롯데시네마 앞에서 보자",
                  "장소는  경상남도 창원시 의창군 중앙대로 300 (사림동) 입니다"
                  ]
    print(len(massages))
    location = []
    for massage in massages:
        _location = rex_location(massage)
        if _location:
            location.append(_location)
            continue
        #_location = loc_detector(massage)
    print(location)
