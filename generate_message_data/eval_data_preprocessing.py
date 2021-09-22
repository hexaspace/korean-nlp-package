import numpy as np
import csv


if __name__ == "__main__":
    days = ['월', '화', '수', '목', '금', '토', '일']
    # f = open("./data/location_tagged/output_disasterSMS3_loc.txt", 'r')
    # f1 = open("./data/location_tagged/output_disasterSMS1_loc.txt", 'r')
    # f2 = open("./data/location_tagged/output_disasterSMS2_loc.txt", 'r')
    # f3 = open("./data/location_tagged/output_disasterSMS3_loc.txt", 'r')
    path = ["./data/location_tagged/output_disasterSMS1_loc.txt","./data/location_tagged/output_disasterSMS2_loc.txt","./data/location_tagged/output_disasterSMS3_loc.txt"]
    fw = open("./data/disasterSMS_bracket_ONE.txt", 'w')
    save = []
    for file_path in path:
        f = open(file_path, 'r')
        while True:
            # input 파일을 한 문장씩 읽어옵니다.
            sentence = f.readline()
            if not sentence: break
            tag_sentence = f.readline()
            dump = f.readline()
            # 탭으로 잘라서 array 만들기
            tab_sent = sentence.split("\t")
            tab_tag = tag_sentence.split("\t")
            # 공백원소와 마지막원소 (\n) 제거
            tab_sent = [w for w in tab_sent if w][:-1]
            tab_tag = [t for t in tab_tag if t][:-1]
            # 본격 괄호 삭제
            for idx, word in enumerate(tab_sent):  # 각 문장의 단어를 확인
                open_idx = word.find("(")  # 여는 괄호 발견
                close_idx = word.find(")")  # 닫는 괄호 발견
                if open_idx >= 0:
                    # print(open_idx, word)
                    if word[open_idx + 1] in days and word[open_idx + 2] == ")":  # 다음 글자가 요일이라면 무시
                        continue
                    # 요일이 아닌 여는괄호라면 띄어야함. 해당 인덱스의 tag 에 loc-b 추가
                    sliced_open = word.split("(")  # ( 기준으로 분리
                    del tab_sent[idx]  # 해당 단어 삭제
                    tab_sent.insert(idx, sliced_open[1])  # ( 기준 오른쪽을 idx 위치에 추가 (뒤로 밀려가는 형태)
                    tab_sent.insert(idx, sliced_open[0])  # ( 기준 왼쪽을 idx 추가
                    tab_tag.insert(idx + 1, "LOC-B")  # 테그도 추가함 (주로 도로명주소)
                    continue  # 원래 해당 word에 ) 가 있었더라도, 다음 array 원소로 넘어갔으므로 continume함

                if close_idx >= 0 and open_idx < 0:  # 닫힘있지만 열린괄호 없을 때
                    if word[-1] == ")":  # 단어 마지막에 닫는괄호라면 괄호삭제만 함
                        tab_sent[idx] = tab_sent[idx].replace(")", "")
                        continue
                    # 닫는 괄호도 띄어쓰기 취급해서 분리해야함
                    sliced_close = word.split(")")

                    del tab_sent[idx]  # 해당 위치 word삭제
                    tab_sent.insert(idx, sliced_close[1])  # )  기준 오른쪽 추가
                    tab_sent.insert(idx, sliced_close[0])  # ) 기준 왼쪾 추가
                    tab_tag.insert(idx, "LOC-B")  # 괄호 앞이 location 도로명주소 # 태그 추가

            sentence = "\t".join(tab_sent)
            tag_sentence = "\t".join(tab_tag)
            # print(sentence, tag_sentence) 	#	fw.write(line+"\n")
            # if (len(tab_sent) != len(tab_tag)):
            #     print("nonnooon ", tab_sent)
            save.append(sentence.replace("\"","")+"\n"+tag_sentence)
            # fw.write(sentence.replace("\"","")+"\n")
            # fw.write(tag_sentence+"\n")

        f.close()
    print(len(save))
    save = list(set(save))
    print(len(save))

    '''
    # write TSV files
    with open('disasterSMS_bracket.tsv', 'w', encoding='utf-8', newline='') as fw:
        tw = csv.writer(fw, delimiter='\t')
        # tw.writerow(['source', 'target', 'value'])
        # tw.writerow(['A', 'B', 10])
        for file_path in path:
            f = open(file_path, 'r')
            while True:
                # input 파일을 한 문장씩 읽어옵니다.
                sentence = f.readline()
                if not sentence: break
                tag_sentence = f.readline()
                dump = f.readline()
                # 탭으로 잘라서 array 만들기
                tab_sent = sentence.split("\t")
                tab_tag = tag_sentence.split("\t")
                # 공백원소와 마지막원소 (\n) 제거
                tab_sent = [w for w in tab_sent if w][:-1]
                tab_tag = [t for t in tab_tag if t][:-1]
                # 본격 괄호 삭제
                for idx, word in enumerate(tab_sent):  # 각 문장의 단어를 확인
                    open_idx = word.find("(")  # 여는 괄호 발견
                    close_idx = word.find(")")  # 닫는 괄호 발견
                    if open_idx >= 0:
                        # print(open_idx, word)
                        if word[open_idx + 1] in days and word[open_idx + 2] == ")":  # 다음 글자가 요일이라면 무시
                            continue
                        # 요일이 아닌 여는괄호라면 띄어야함. 해당 인덱스의 tag 에 loc-b 추가
                        sliced_open = word.split("(")  # ( 기준으로 분리
                        del tab_sent[idx]  # 해당 단어 삭제
                        tab_sent.insert(idx, sliced_open[1])  # ( 기준 오른쪽을 idx 위치에 추가 (뒤로 밀려가는 형태)
                        tab_sent.insert(idx, sliced_open[0])  # ( 기준 왼쪽을 idx 추가
                        tab_tag.insert(idx + 1, "LOC-B")  # 테그도 추가함 (주로 도로명주소)
                        continue  # 원래 해당 word에 ) 가 있었더라도, 다음 array 원소로 넘어갔으므로 continume함

                    if close_idx >= 0 and open_idx < 0:  # 닫힘있지만 열린괄호 없을 때
                        if word[-1] == ")":  # 단어 마지막에 닫는괄호라면 괄호삭제만 함
                            tab_sent[idx] = tab_sent[idx].replace(")", "")
                            continue
                        # 닫는 괄호도 띄어쓰기 취급해서 분리해야함
                        sliced_close = word.split(")")

                        del tab_sent[idx]  # 해당 위치 word삭제
                        tab_sent.insert(idx, sliced_close[1])  # )  기준 오른쪽 추가
                        tab_sent.insert(idx, sliced_close[0])  # ) 기준 왼쪾 추가
                        tab_tag.insert(idx, "LOC-B")  # 괄호 앞이 location 도로명주소 # 태그 추가

                sentence = "\t".join(tab_sent)
                tag_sentence = "\t".join(tab_tag)
                # print(sentence, tag_sentence)
                if (len(tab_sent) != len(tab_tag)):
                    print("nonnooon ", tab_sent)
                # tw.writerow([sentence, tag_sentence])
                tw.writerow(sentence)
                tw.writerow(tag_sentence)

            f.close()


	# fw = open("./data/output_disasterSMS1_bracket.txt", 'w')

while True:
		# input 파일을 한 문장씩 읽어옵니다.
		sentence = f.readline()
		if not sentence: break
		tag_sentence = f.readline()
		dump = f.readline()

		result_sentences, result_tags = text_augmentation_sentences(sentence, tag_sentence)
		for result_sentence, result_tag in zip(result_sentences, result_tags):
			augmented_data = result_sentence + "\t" + result_tag
			augmented_datas.append(augmented_data)

	random.shuffle(augmented_datas)

	for line in augmented_datas:
		print(line)
		fw.write(line+"\n")

	f.close()
	# fw.close()'''