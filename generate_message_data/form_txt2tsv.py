### augmented data를 tsv로 확장자 변경
'''
fwrite = open("./data/tsv_file/disasterSMS3_augmented.tsv", "w", encoding="utf-8")
file =  open("./data/disaster_augmented/output_disasterSMS3_augmented.txt", "r")
line = None
while line != "" :
    line = file.readline()
    fwrite.write(line)

file.close()
fwrite.close()'''
##### 기존 data와 재난문자 data 합치기 --  원격서버에서 실행할 것
# fwrite_loc = open("test_loc.tsv", "w", encoding="utf-8")
# fread_origin = open("test.tsv","r", encoding="utf-8")
# fread_loc1= open("test_loc_data.tsv", "r", encoding="utf-8")
# # fread_loc2= open("train_loc_data2.tsv", "r", encoding="utf-8")
# # fread_loc3 = open("train_loc_data3.tsv", "r", encoding="utf-8")
# #, encoding="utf-8" 'cp1252'
# for line in fread_origin:
#     fwrite_loc.write(line)
# for line in fread_loc1:
#     fwrite_loc.write(line)

import numpy as np
import csv


if __name__ == "__main__":
    f = open("./data/disaster_tagged_sto_all.txt", 'r')

    with open('./data/test_data_sto_all.tsv', 'w', encoding='utf-8', newline='') as fw:
        tw = csv.writer(fw, delimiter='\t')
        # tw.writerow(['source', 'target', 'value'])
        # tw.writerow(['A', 'B', 10])
        while True:
            # input 파일을 한 문장씩 읽어옵니다.
            sentence = f.readline()
            if not sentence: break
            tag_sentence = f.readline()
            # print("read line ", sentence, tag_sentence)
            # 탭으로 잘라서 array 만들기
            tab_sent = sentence.split("\t")
            tab_tag = tag_sentence.split("\t")
            # 공백원소와 마지막원소 (\n) 제거
            tab_sent = [w for w in tab_sent if w][:-1]
            tab_tag = [t for t in tab_tag if t][:-1]
            str_sentence = " ".join(tab_sent)
            str_tag_sentence = " ".join(tab_tag)
            # print("string ", str_sentence, str_tag_sentence)
            if (len(tab_sent) != len(tab_tag)):
                print("nonnooon ",len(tab_sent) , len(tab_tag), tab_sent)
                # for i in range(len(tab_sent)-1):
                #     print(tab_sent[i], tab_tag[i])
                # continue
            tw.writerow([str_sentence, str_tag_sentence])

