# -*- coding: utf-8 -*-

import re
import konlpy
import os
from konlpy.tag import Hannanum

def loc_detector(massage):
    print(massage)

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

def konlpy_parsing(sentence):
    han = Hannanum()
    sent3 = del_initial(sentence)   #자모 제거
    x = han.analyze(sent3) #형태소 분석
    nset = set()
    jcset = set()
    string = ""

    for word in x:    #문장 내 어절 단위
    #print(word)
        #if len(word)>=1:
        #    case = word[0]
        for case in word:   #동일 어절의 형태소 분석 경우의 수
            for unit in case: #해당 경우의 하나의 형태소 단위
                # 비서술성 명사, 기타일반명사 바로 추출

                if unit[1] == 'nqq':  #unit[1] == 'ncn' or
                    nset.add(unit[0])
                '''
                elif unit[1] == 'ncn':
                    not_inital = del_initial(unit[0])
                    nset.add(not_inital)
                    print(not_inital, "(nc)", end=" ") or unit[1] == 'jco'
                    '''
                # 부사격, 목적격 조사로 앞에 명사 찾기
                if unit[1] == 'jca' or unit[1] == 'jco':
                    joidx = case.index(unit)
                    for i in range(joidx):
                        string += case[i][0]
            nset.add(string)
            #if string != "":
            #    print(string, "(jc)", end=" ")
            string  = ""
    result_set = nset
    #result_set.remove("")  #공백제거 왜 에러
    return result_set

def del_initial(sentence):
    #자음으로, 또는 모음으로만 이뤄진 글자 제거(오타, 감정표현, 초성 등)
    result_sent = ""  # 공백 문자열
    initial = re.compile("([^ㄱ-ㅎㅏ-ㅣ~^]+)")    #자음 모음 제거
    inilist = initial.findall(sentence)
    # 존재한다면 문자열에 추가 후 다음 문자열부터 탐색
    if inilist == None:
        result_sent = sentence
    else:
        for i in inilist:
            result_sent += i
    return result_sent


if __name__ == "__main__":
    han = Hannanum()

    rex_loc = []
    konlp_loc = []
    konlp_num = 0
    input = _read_data_file('input.txt')
    for story in input:
        # print("원본 : ", story)
        for sent in story:
            #정규표현식 도로명주소
            _location = rex_location(sent)
            if _location:
                rex_loc.append(_location)
                continue
            #형태소 분석
            loc = konlpy_parsing(sent)
            locations = locations | loc
        # print(locations)
        # print()
        konlp_loc.append(locations)
        konlp_num += len(locations)
        locations = set()

    '''
    massages = ["내일 만나서 뭐할까?",
                  "만나서 영화 보는거 어때",
                  "좋아 그럼 롯데시네마 앞에서 보자",
                  "장소는  경상남도 창원시 의창군 중앙대로 300 (사림동) 입니다"
                  ]
    for massage in massages:
        _location = rex_location(massage)
        if _location:
            location.append(_location)
            continue
        #_location = loc_detector(massage)
        '''


