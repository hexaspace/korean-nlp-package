# -*- coding: utf-8 -*-

import re
import konlpy
import os
from konlpy.tag import Hannanum

def _read_data_file(file_path, train=True): #해당 파이썬 내 로드함수 예비용
    sentences = []
    sentence = []
    for line in open(file_path, encoding="utf-8"):
        line = line.strip()
        if line == "":
            sentences.append(sentence)
            sentence = []
        else:
            sentence.append(line)
    return sentences


def loc_detector(messages):
    han = Hannanum()
    rex_loc = []    #도로명주소 리스트
    konlp_loc = []  #형태소 파싱 후 주소후보 리스트

    for message in messages:
        # 정규표현식 도로명주소 추출
        road_location = get_road_address(message)
        if road_location:   # 도로명 주소가 존재한다면
            rex_loc.append(road_location)
            continue
        # 형태소 분석 주소 후보 추출
        konlpy_location_set = get_locations_by_konlpy(message)
        # 결과값인 set을 list로 변환 후 konlpy_loc에 연결추가
        konlpy_location_list = list(konlpy_location_set)
        konlp_loc.extend(konlpy_location_list)

    konlp_loc.reverse() # 역순으로 정렬 (최근 message일수록 장소 확률 증가)

    return rex_loc, konlp_loc

def get_road_address(sentence):
    road_address = ""    #공백 문자열
    #시도, 시군구 정규표현식 이후에 나머지 도로명주소 정규표현식을 적용한다.
    rex_sigu = re.compile("([가-힣]{2,6}(시|도)).([가-힣]+(시|군|구))")
    rex_ro = re.compile("((\s[가-힣\d\,\.]+(읍|면|동|가|리|구))|).([가-힣A-Za-z·\d~\-\.]+(로|길)).((지하 |공중 |)[\d]+)((\,(\s[\d]+동|)(\s[\d~]+층|)(\s[\d]+호|))|)((\s|)\([가-힣]+동\)|)")
    #시도, 시군구 적용
    sigu = rex_sigu.search(sentence)
    #존재한다면 문자열에 추가 후 다음 문자열부터 탐색
    if sigu == None:
        tail_sentence = sentence    # 시, 구 찾지 못했을 때 전체 문자열
    else:
        tail_sentence = sentence[sigu.end():]    #tail_sentence : 시, 구 이후의 나머지 문자열
        road_address += sigu.group()
    #읍면구 로길 상세주소 (동) 정규표현식 적용
    ro = rex_ro.search(tail_sentence)
    # 존재할때 문자열에 추가
    if ro != None:
        road_address += ro.group()
    #문자열 반환
    return road_address

def get_locations_by_konlpy(_sentence):

    sentence = delete_jamo(_sentence)   #자모 제거
    morphemes = han.analyze(sentence) #형태소 분석
    location_set = set()

    string = "" #공백 문자열 (조사 발견시 앞 형태소 저장 용도)

    for word in morphemes:    #문장 내 어절 단위
        for case in word:   #동일 어절의 형태소 분석 경우의 수
            for unit in case: #해당 경우의 하나의 형태소 단위
                #기타일반명사 바로 추출
                if unit[1] == 'nqq':
                    if len(unit[0]) > 1:    #2글자 이상인 단어만 후보
                        location_set.add(unit[0])
                # 부사격, 목적격 조사로 앞에 명사 찾기
                elif unit[1] == 'jca' or unit[1] == 'jco':
                    josa_idx = case.index(unit)
                    for i in range(josa_idx):
                        string += case[i][0]
                    if len(string) > 1:    #2글자 이상인 단어만 후보
                        location_set.add(string)
                    string  = ""

    return location_set

def delete_jamo(_sentence):
    #자음으로, 또는 모음으로만 이뤄진 글자 제거(오타, 감정표현, 초성 등)
    sentence = ""  # 공백 문자열
    not_jamo = re.compile("([^ㄱ-ㅎㅏ-ㅣ~^]+)")    #자음, 모음, 특수문자제거
    not_jamo_list = not_jamo.findall(_sentence)
    # 존재한다면 문자열에 추가 후 다음 문자열부터 탐색
    if not_jamo_list == None:
        sentence = _sentence
    else:
        for i in not_jamo_list:
            sentence += i
    return sentence


if __name__ == "__main__":
    han = Hannanum()    # class 생성

    input = _read_data_file('data/input.txt')
    for i in input:
        road_list, konlpy_list = loc_detector(i)
        print("도로명주소 : ", road_list)
        print("형태소 주소후소 : ", konlpy_list)




