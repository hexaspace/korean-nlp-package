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
		return words

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
		return words

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
	# new_words가 모두 위치 개체명일 경우 교체하지 않습니다.
	words_without_locations = [word for word in new_words if word not in locations]
	if not words_without_locations: return new_words

	# 위치 개체명이 아닌 인덱스들만 추출하고, 그 중 랜덤 인덱스 2개를 얻습니다.
	indices_without_locations = [index for index, word in enumerate(new_words) if word not in locations]
	random_idx_1, random_idx_2 = get_random_indices(indices_without_locations)

	# 랜덤 인덱스 찾기에 실패한 경우 교체하지 않습니다.
	if random_idx_1 == -1 and random_idx_2 == -1:
		return new_words

	# 단어 교체
	new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
	new_tags[random_idx_1], new_tags[random_idx_2] = new_tags[random_idx_2], new_tags[random_idx_1]
	return new_words, new_tags

def get_random_indices(indices):
	random_idx_1, random_idx_2 = random.sample(indices, 2)
	return random_idx_1, random_idx_2

########################################################################
# Synonym replacement
# Replace n words in the sentence with synonyms from wordnet
########################################################################
def synonym_replacement(words, n):
	new_words = words.copy()
	random_word_list = list(set([word for word in words]))
	random.shuffle(random_word_list)
	num_replaced = 0
	for random_word in random_word_list:
		synonyms = get_synonyms(random_word)
		# print("--sr--", end=" ")
		# print(random_word, synonyms)
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

			# for s in syn:
			# 	synomyms.append(s)
	except:
		pass

	return synomyms

########################################################################
# Random insertion
# Randomly insert n words into the sentence
########################################################################
def random_insertion(words, n):
	new_words = words.copy()
	for _ in range(n):
		add_word(new_words)
	
	return new_words


def add_word(new_words):
	synonyms = []
	counter = 0
	while len(synonyms) < 1:
		if len(new_words) >= 1:
			random_word = new_words[random.randint(0, len(new_words)-1)]
			synonyms = get_synonyms(random_word)
			counter += 1
		else:
			random_word = ""

		if counter >= 10:
			return
		
	random_synonym = synonyms[0]
	random_idx = random.randint(0, len(new_words)-1)
	new_words.insert(random_idx, random_synonym)


def text_augmentation_sentences(sentence, tag_sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.3, p_rd=0.3, num_aug=9):
	sentence = get_only_hangul(sentence)
	words, tags, locations = get_locations(sentence, tag_sentence)

	sentence = ""
	for word in words:
		sentence += word + " "

	# sentence += word for word in words
	# words = sentence.split(' ')
	# words = [word for word in words if word != ""]
	num_words = len(words)

	augmented_sentences = []
	augmented_tags = []
	num_new_per_technique = int(num_aug/4) + 1

	n_sr = max(1, int(alpha_sr*num_words))
	n_rs = max(1, int(alpha_rs*num_words))

	# sr Synonym Replacement 특정 단어를 유의어로 교체
	for _ in range(num_new_per_technique):
		a_words = synonym_replacement(words, n_sr)
		augmented_sentences.append(' '.join(a_words))

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

	augmented_sentences = [get_only_hangul(sentence) for sentence in augmented_sentences]
	random.shuffle(augmented_sentences)

	if num_aug >= 1:
		augmented_sentences = augmented_sentences[:num_aug]
	else:
		keep_prob = num_aug / len(augmented_sentences)
		augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

	augmented_sentences.append(sentence)

	return augmented_sentences, augmented_tags

if __name__ == "__main__":
	f = open("./output_disasterSMS2_location.txt", 'r')
	for i in range(0,1):
		sentence = f.readline()
		if not sentence: break

		tag_sentence = f.readline()
		dump =  f.readline()

		result_sentence, result_tags = text_augmentation_sentences(sentence, tag_sentence)
		print(result_sentence, "\t", result_tags, "\n")

	# print(text_augmentation_sentences("[경상북도청] 꽃동네노래방(유흥)(대구 북구 경진로1길5) 7/12~7/15 방문자는 가까운 보건소 선별진료소에서 검사	ORG-B ORG-B LOC-B AFW-B DAT-B CVL-B O O O O "))
