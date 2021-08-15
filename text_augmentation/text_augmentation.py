import random
import pickle
import re

wordnet = {}
with open("wordnet.pickle", "rb") as f:
	wordnet = pickle.load(f)


# 한글만 남기고 나머지는 삭제
def get_only_hangul(line):
	parseText= re.compile('/ ^[ㄱ-ㅎㅏ-ㅣ가-힣]*$/').sub('',line)

	return parseText

def get_locations(line, tag_line):
	# 탭을 기준으로 배열화
	words = line.split('\t')
	tags = tag_line.split('\t')
	
	# 공백원소와 마지막원소 (\n) 제거
	words = [w for w in words if w][:-1]
	tags = [t for t in tags if t][:-1]
	
	# 위치 태그에 해당하는 단어만 저장
	location_tags = ["LOC", "LOC-B", "LOC-I"]
	location_words = []
	for word, tag in zip(words, tags):
		if tag in location_tags:
			location_words.append(word)

	return words, tags, location_words


########################################################################
# 랜덤하게 단어 삭제
# 확률 p에 기반하여 문장 내 단어를 랜덤하게 삭제합니다.
########################################################################
def random_deletion(words, locations, tags, p):
	if len(words) == 1:
		return words, tags

	# 랜덤 삭제 후 남은 단어와 태그를 저장 (단어와 태그는 1:1 대응됨)
	new_words = []
	new_tags = []

	# 랜덤 확률 r이 p 이상일 때만 단어를 따로 저장 (p 이하일 때의 단어는 삭제됨)
	for word in words:
		r = random.uniform(0, 1)
		if r > p or word in locations:
			new_words.append(word)
			_idx = words.index(word)
			new_tags.append(tags[_idx])

	# 문장 내 단어가 모두 삭제되었을 경우 기존 words 리턴
	if len(new_words) == 0:
		return words, tags

	return new_words, new_tags

########################################################################
# 랜덤하게 단어 교체
# 문장 내 두 단어를 랜덤하게 n번 교체합니다.
########################################################################
def random_swap(words, locations, tags, n):
	new_words = words.copy()
	new_tags = tags.copy()
	
	# n번 단어 교체
	for _ in range(n):
		new_words, new_tags = swap_word(new_words, new_tags, locations)

	return new_words, new_tags


def swap_word(new_words, new_tags, locations):
	# 위치 개체명이 아닌 인덱스들만 추출하고, 그 중 랜덤 인덱스 2개를 얻습니다.
	indices_without_locations = [index for index, word in enumerate(new_words) if word not in locations]
	# 위치 개체명이 아닌 단어가 1개 이하일 경우 교체하지 않습니다.
	if len(indices_without_locations) > 1:
		random_idx_1, random_idx_2 = get_random_indices(indices_without_locations)
	else:
		return new_words, new_tags

	# 단어 교체
	new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
	new_tags[random_idx_1], new_tags[random_idx_2] = new_tags[random_idx_2], new_tags[random_idx_1]
	return new_words, new_tags

def get_random_indices(indices):
	random_idx_1, random_idx_2 = random.sample(indices, 2)
	return random_idx_1, random_idx_2

########################################################################
# 유의어 교체
# wordnet을 기반으로 n개의 단어를 유의어로 교체합니다.
########################################################################
def synonym_replacement(words, n):
	new_words = words.copy()
	random_word_list = list(set([word for word in words]))
	random.shuffle(random_word_list)
	num_replaced = 0
	for random_word in random_word_list:
		synonyms = get_synonyms(random_word)
		if len(synonyms) >= 1:
			synonym = random.choice(list(synonyms))
			new_words = [synonym if word == random_word else word for word in new_words]
			num_replaced += 1
		if num_replaced >= n:
			break

	if len(new_words) != 0:
		sentence = ' '.join(new_words)
		new_words = sentence.split(" ")
	else:
		new_words = ""

	return new_words


def get_synonyms(word):
	synomyms = []

	try:
		for syn in wordnet[word]:
			synomyms.append(syn)
	except:
		pass

	return synomyms


def text_augmentation_sentences(sentence, tag_sentence, alpha_sr=0.1, alpha_rs=0.3, p_rd=0.3, num_aug=9):
	sentence = get_only_hangul(sentence)
	words, tags, locations = get_locations(sentence, tag_sentence)

	sentence = ""
	for word in words:
		sentence += word + " "

	tag_sentence = ""
	for tag in tags:
		tag_sentence += tag + " "

	num_words = len(words)

	augmented_sentences = []
	augmented_tags = []

	num_new_per_technique = int(num_aug/3)

	n_sr = max(1, int(alpha_sr*num_words))
	n_rs = max(1, int(alpha_rs*num_words))

	# sr Synonym Replacement 특정 단어를 유의어로 교체
	for _ in range(num_new_per_technique):
		a_words = synonym_replacement(words, n_sr)
		augmented_sentences.append(' '.join(a_words))
		augmented_tags.append(tag_sentence)

	# rs Random Swap 문장 내 임의의 두단어의 위치를 바꿈
	for _ in range(num_new_per_technique):
		a_words, a_tags = random_swap(words, locations, tags, n_rs)
		augmented_sentences.append(" ".join(a_words))
		augmented_tags.append(" ".join(a_tags))

	# rd Random Deletion 임의의 단어를 삭제
	for _ in range(num_new_per_technique):
		a_words, a_tags = random_deletion(words, locations, tags, p_rd)
		augmented_sentences.append(" ".join(a_words))
		augmented_tags.append(" ".join(a_tags))

	augmented_sentences.append(sentence)
	augmented_tags.append(tag_sentence)

	return augmented_sentences, augmented_tags


if __name__ == "__main__":
	f = open("./output_disasterSMS1_loc.txt", 'r')
	fw = open("./output_disasterSMS1_output.txt", 'w')
	augmented_datas = []

	for _ in range(0,1):
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
	fw.close()
