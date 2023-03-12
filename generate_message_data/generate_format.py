import random
import os
import csv
import numpy as np
import pandas as pd

from generate_random_address_date import get_addresses as get_addresses
from generate_random_address_date import get_random_value as get_random_value
from generate_random_address_date import get_random_date_format as get_random_date_format

# 특정 배열에서 랜덤으로 추출하는 함수
def random_array (origin, array, probability, weight, tag): # 원본arr, 추가후보arr, 추가 될 확률, 각 후보의 가중치, 해당 tag
    [existence] = random.choices([True, False], weights=[probability, 1-probability])
    if not existence:   # 만약 해당 part가 존재하지 않는 확률일 때
        return origin
    else:
        [word] = random.choices(array, weights=weight)
        origin.append([word, tag])  # 원본 array에 추가
        return origin



def random_array_multiple (origin, array, probability, weight, tag): #후보가 2단어 이상으로 구성되었을 때
    [existence] = random.choices([True, False], weights=[probability, 1-probability])
    if not existence:   # 만약 해당 part가 존재하지 않는 확률일 때
        return origin
    else:
        [word] = random.choices(array, weights=weight)
        word_array = word.split(" ")
        for a_word in word_array:
            origin.append([a_word, tag])  # 원본 array에 추가
            tag = tag.replace("B", "I") # 두번째 이후부터 I 태그
        return origin

# 상호명 사전 불러오기
def _read_store_files(dir_path):
    data = []

    # read all files in 'store_names' dir
    file_list = os.listdir(dir_path)
    for file in file_list:
        file_path = dir_path + '/' + file
        df = pd.read_csv(file_path)
        data.append([file.replace('.csv',''), df])
    store_names = list(df["상호명"])
    return store_names

def store_loader():
    dir_path = '../sms_ner_pkg/sms_ner_pkg/data/dictionary/store_names'            # path 바꿈?!!!!!!!!!!
    return _read_store_files(dir_path)

# 시군구 사전 불러오기
def sigu_loader():
    file_path = '../sms_ner_pkg/sms_ner_pkg/data/dictionary/sigu_names.xlsx'            # path 바꿈?!!!!!!!!!!
    sigungu_df = _read_sigu_file(file_path)
    short_name = ["서울시","부산시","대구시","인천시","광주시","대전시","울산시","제주시"]
    global_sigungu = list(set(list(sigungu_df["SI"])))+short_name
    local_sigungu = list(set(list(sigungu_df["GU"])))
    return [global_sigungu, local_sigungu]


def _read_sigu_file(file_path):
    # read sigu table file
    sheet_name = 'sigu_table'
    df_sigu = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        names=['SI', 'GU'],
    )
    return df_sigu


def generate_loc(sigungu_local_data, random_store, addresses):
    loc_array = []
    # sigu_local = sigu_loader(False) #기초자치단체
    loc_head = random.choice(sigungu_local_data)   #"광주 명륜동 가천 등등" 기초자치단체  # LOC (0.2) 시~동
    loc_array = random_array(loc_array, [loc_head], 0.2, None, "LOC-B")
    if(len(loc_array)>0):
        loc_head_case = ["소재"]  # O (0.2)
        loc_array = random_array(loc_array, loc_head_case, 0.5, None, "LOC-I")

    loc_store = random_store  # STO (1)
    loc_array.append([loc_store, "STO-B"])

    loc_tail = random.choice(sigungu_local_data)+"점"    # LOC (0.3)    기초자치단체+"점"
    loc_array = random_array(loc_array, [loc_tail], 0.3, None, "LOC-B")


    loc_road_name = random.choice(addresses)  # LOC (0.7)
    loc_array = random_array_multiple(loc_array, [loc_road_name], 0.7, None, "LOC-B")

    return loc_array

def message_middle(sigungu_local_data, random_store, addresses):
    location = generate_loc(sigungu_local_data, random_store, addresses)
    date = get_random_date_format()
    # time의 등장 확률만 랜덤 (0.5)
    # date (time) loc (0.7) 혹은 loc date (time) (0.3)
    # location이 먼저 등장할 확률 0.3
    order_loc = random.choices([True, False], weights=[0.7, 0.3])
    if order_loc:   #location 이 1번째일때
        # location.append(date)
        return date + location

    else:  #locatiob이 0번째 일 때
        # date.append(location)
        return location + date


def message_head(sigungu_all_data):
    # [경상북도청] [전남도청] 원주시청 군청 시청 광역시.
    # location detector의  sigu 함수 참고
    sigu = random.choice(sigungu_all_data)
    return ["["+sigu + "청]", "ORG-B"]


def message_tail():
    tail_array = []
    # CVL, 아래 두 배열중 무조건 하나 택
    cvl_head = ["동시간대"] # o (0.1)
    tail_array_head = random_array(tail_array, cvl_head, 0.1, None, "CVL-B")
    cvl_head_len = len(tail_array_head)
    a_cvl = ["방문자는", "이용자는", "이용객은"]    # CVL (0.7)
    tail_array = random_array(tail_array_head, a_cvl, 0.7, [0.7,0.2,0.1], "CVL-B")
    two_cvl = ["방문하신 분은", "다녀오신 분은"]    # CVL-B CVL-I (0.3)
    if (len(tail_array) == cvl_head_len):  # 한단어 cvl이 추가되지 않았다면
        tail_array = random_array_multiple(tail_array_head, two_cvl, 1, None, "CVL-B")

    # 태그 미정. 보건소 지칭
    public_health_head = ["가까운","거주지","임시선별진료소나","주소지","인근"]    #   O (0.3)
    tail_array = random_array(tail_array, public_health_head, 0.3, None, "O")

    public_health = ["보건소에서", "보건소"]    # AFW
    tail_array = random_array(tail_array, public_health, 1, None, "AFW-B")
    if (tail_array[-1][0] == "보건소"):    # 보건소 지칭이 "에서"로 끝나지 않았을때
        public_health_or = ["또는", "및"]  # O (0.1)
        tail_array = random_array(tail_array, public_health_or, 0.1, None, "O")
        public_health_tail = ["선별진료소에서", "선별진료소"]   # 보건소 일때만 동작 AFW (0.3)
        tail_array = random_array(tail_array, public_health_tail, 1, None, "AFW-B")
# 방문하여
    # 진단검사  띄어쓰기 경우의 수 많음
    examine_adverb = ["즉시"] # O (0.2)
    tail_array = random_array(tail_array, examine_adverb, 0.2, None, "O")
    examine_verb_head = ["코로나", "코로나19"]    # TRM (0.7)
    tail_array = random_array(tail_array, examine_verb_head, 0.7, None, "TRM-B")

    examine_verb = ["검사받으세요.", "검사 바랍니다.",
                    "검사 받으시기 바랍니다.", "검사받으시기 바랍니다.",  "검사를 받으시기 바랍니다.", "검사를 받기바랍니다.",
                    "검사 권고 드립니다", "방문검사 바랍니다"]   #O
    tail_array = random_array_multiple(tail_array, examine_verb, 1, [3,3,6,3,3,3,1,1], "O")
    return tail_array
if __name__ == "__main__":




    # 데이터 로더
    sigungu = sigu_loader() # 시군구
    sigungu_all_data = sigungu[0]+sigungu[1]
    sigungu_local_data = sigungu[1]

    store_name_data = store_loader()    # 상호명

    address_data_path = "./data/address.txt"
    addresses = get_addresses(address_data_path)        # 도로명 주소

    # write TSV files
    with open('./data/train_generated_hund_thous.tsv', 'w', encoding='utf-8', newline='') as f:
        tw = csv.writer(f, delimiter='\t')
        # tw.writerow(['source', 'target', 'value'])
        # tw.writerow(['A', 'B', 10])
        
        for i in range(100000):
            head = [message_head(sigungu_all_data)]
            random_store = random.choice(store_name_data)
            middle = message_middle(sigungu_local_data, random_store, addresses)
            tail = message_tail()
            a_message = head + middle + tail
            np_message = np.array(a_message)
            sentence = " ".join(np_message[:, 0])
            tag_sentence = " ".join(np_message[:, 1])
            print(sentence, tag_sentence)

            tw.writerow([sentence, tag_sentence])

