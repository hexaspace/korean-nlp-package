
# -*- coding: utf-8 -*-
from sms_ner_pkg.location_detector import loc_detector as location_detector
import os

# fw = open("./data/disaster_augmented/output_disasterSMS1_augmented.txt", 'w')
# augmented_datas = []
# input 파일을 한 문장씩 읽어옵니다.
# path = '../config/hello.txt'
#


def get_locations(line, tag_line):
    # 탭을 기준으로 배열화
    words = line.split(' ')
    tags = tag_line.split(' ')

    # 공백원소와 마지막원소 (\n) 제거
    words = [w for w in words if w][:-1]
    tags = [t for t in tags if t][:-1]

    # 위치 태그에 해당하는 단어만 저장
    # location_tags = ["LOC", "LOC-B", "LOC-I"]     , "AFW-B", "AFW-I"
    location_tags = ["LOC-B", "LOC-I", "ORG-B", "ORG-I"]
    location_words = []
    for word, tag in zip(words, tags):
        if tag in location_tags:
            location_words.append(word)
    return location_words

def measure_accuracy(accuracy_list, result_list):
    accuracy_string = " ".join(accuracy_list)   # result는 무조건 1단어로 구성되었기 때문에 (if in)을 쓰기위해 accuracy 를 string으로 이어준다.
    accuracy_len = len(accuracy_list)
    result_len = len(result_list)
    if result_len == 0: # 측정 결과 아무것도 없다면 0으로 반환
        return 0,0,0
    # 실제정답 accuracy와 분규결과 result의 교집합인 true_positive 개수 측정
    true_positive = 0
    for result_word in result_list:
        if result_word in accuracy_string:
            true_positive += 1
    print("true_positive:",true_positive,"  result_len:",result_len,"  accuracy_len:",accuracy_len)
    if true_positive == 0: # 교집합이 아무것도 없다면 0으로 반환 (0으로 나누기 불가)
        return 0,0,0
    precision = true_positive/result_len
    recall= true_positive/accuracy_len
    f1_score = 2*precision*recall / (precision+recall)
    return recall, precision, f1_score

msg=[]
message = "[전남도청] 7.9(금) 21시 광주 소재 상무나이트( 서구 상무번영로 30)를 방문하신 분은 거주시 보건소에서 코로나 검사 받으시기 바랍니다."
message1 = "[경상북도청] 꽃동네노래방(유흥)(대구 북구 경진로1길5) 7/12~7/15 방문자는 가까운 보건소 선별진료소에서 검사 받으시기 바랍니다."

total_recall=0
total_precision=0
total_f1_score=0
total_data = 0
isZero = 0
fw = open("../sms_ner_pkg/data/location_accuracy_result_2.txt", 'w')

# body = f.read()
# body = body.replace("\t"," ")
# print(body)
# sentence = body.readline()

# print(sentence)
file_path = "../sms_ner_pkg/data/input/tagged_disasterSMS1.txt"  #위치???
f = open(file_path, 'r')
while True :
    sentence = f.readline().replace("\t", " ")
    if not sentence: break
    tag_sentence = f.readline().replace("\t", " ")
    dump = f.readline()
    # location = location_detector([sentence])
    msg.append(sentence)
    msg.append(tag_sentence)

f.close()
file_path = "../sms_ner_pkg/data/input/tagged_disasterSMS2.txt"  #위치???
f = open(file_path, 'r')
while True :
    sentence = f.readline().replace("\t", " ")
    if not sentence: break
    tag_sentence = f.readline().replace("\t", " ")
    dump = f.readline()
    # location = location_detector([sentence])
    msg.append(sentence)
    msg.append(tag_sentence)

f.close()
file_path = "../sms_ner_pkg/data/input/tagged_disasterSMS3.txt"  #위치???
f = open(file_path, 'r')
while True :
    sentence = f.readline().replace("\t", " ")
    if not sentence: break
    tag_sentence = f.readline().replace("\t", " ")
    dump = f.readline()
    # location = location_detector([sentence])
    msg.append(sentence)
    msg.append(tag_sentence)

f.close()
data_len = int(len(msg)/2)
total_data += data_len
print("data size: ", data_len)
accuracy_sum = 0
# print("데이터수",len(msg))
for i in range(data_len):
    sentence = msg[i*2]
    tag = msg[i*2+1]
    print(" ")
    print(sentence)
    fw.write(sentence+"\n")
    accuracy_loc = get_locations(sentence, tag)
    # location = location_detector([message])
    result_loc = location_detector(sentence)
    print("accuracy_loc : ", accuracy_loc, " / result_loc: ", result_loc)
    fw.write("accuracy_loc : "+ str(accuracy_loc)+ " / result_loc: "+ str(result_loc)+"\n")
    recall, precision, f1_score =  measure_accuracy(accuracy_loc, result_loc)
    print("[accuracy] f1_score: ",f1_score," recall: ", recall," precision: ", precision)
    fw.write("[accuracy] f1_score: "+str(f1_score)+" recall: "+ str(recall)+" precision: "+ str(precision)+"\n")
    if(f1_score==0):
        isZero += 1
    total_recall += recall
    total_precision += precision
    total_f1_score += f1_score

    # accuracy_sum += accuracy
print("")
print("zero result : ",isZero)
print("[total accuracy] total_recall: ",total_recall," total_precision: ", total_precision," total_f1_score: ",total_f1_score)
print("")
print("[total accuracy] f1_score: ",total_f1_score/data_len," recall: ", total_recall/data_len," precision: ", total_precision/data_len)
fw.write("[total accuracy] f1_score: "+str(total_f1_score/data_len)+" recall: "+str(total_recall/data_len)+" precision: "+str(total_precision/data_len)+"\n")

print(data_len)
fw.write(str(data_len))
'''
# if __name__ == "__main__":
file_list = os.listdir("../sms_ner_pkg/data/input")
# abs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_path)
print(file_list)

# f=open(file_path, encoding="cp949")
while True:
    sentence = f.readline()
    if not sentence: break
    tag_sentence = f.readline()
    dump = f.readline()
    location = location_detector([sentence])

    print(location)
f.close()
'''
# 	result_sentences, result_tags = text_augmentation_sentences(sentence, tag_sentence)
	# 	for result_sentence, result_tag in zip(result_sentences, result_tags):
	# 		augmented_data = result_sentence + "\t" + result_tag
	# 		augmented_datas.append(augmented_data)
    #
	# random.shuffle(augmented_datas)
    #
	# for line in augmented_datas:
	# 	print(line)
	# 	fw.write(line+"\n")

	# fw.close()
