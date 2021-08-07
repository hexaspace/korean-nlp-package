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
	# print(words, tags)
	# words, tags = line.split('\t')[0].split(' '), line.split('\t')[1].split(' ')
	locations = ""
	for word, tag in zip(words, tags):
		if tag in ["LOC", "LOC-B", "LOC-I"]:
		# if tag in ["LOC", "LOC-B", "LOC-I", "ORG", "ORG-B", "ORG-I", "AFW", "AFW-B", "AFW-I"]:
			locations += word + " "
	return words, locations


########################################################################
# Random deletion
# Randomly delete words from the sentence with probability p
########################################################################
def random_deletion(words, locations, p):
	if len(words) == 1:
		return words
	new_words = []
	for word in words:
		r = random.uniform(0, 1)
		if r > p or word in locations:
			new_words.append(word)

	if len(new_words) == 0:
		return words
	#	rand_int = random.randint(0, len(words) - 1)
	# return [words[rand_int]].append(locations)

	return new_words

########################################################################
# Random swap
# Randomly swap two words in the sentence n times
########################################################################
def random_swap(words, locations, n):
	for location in locations:
    		if location in words:
    				words.remove(location)
	new_words = words.copy()
	for _ in range(n):
		new_words = swap_word(new_words)

	return new_words

def swap_word(new_words):
	random_idx_1 = random.randint(0, len(new_words)-1)
	random_idx_2 = random_idx_1
	counter = 0

	while random_idx_2 == random_idx_1:
		random_idx_2 = random.randint(0, len(new_words)-1)
		counter += 1
		if counter > 3:
			return new_words

	new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
	return new_words


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



def EDA(sentence, tag_sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.3, p_rd=0.3, num_aug=9):
	sentence = get_only_hangul(sentence)
	# loc_sentence = get_only_hangul(loc_sentence)

	words, locations = get_locations(sentence, tag_sentence)
	sentence = ""
	for word in words:
		sentence += word + " "
	# sentence += word for word in words
	# words = sentence.split(' ')
	# words = [word for word in words if word != ""]
	num_words = len(words)

	augmented_sentences = []
	num_new_per_technique = int(num_aug/4) + 1

	n_sr = max(1, int(alpha_sr*num_words))
	n_ri = max(1, int(alpha_ri*num_words))
	n_rs = max(1, int(alpha_rs*num_words))

	# sr Synonym Replacement 특정 단어를 유의어로 교체
	for _ in range(num_new_per_technique):
		a_words = synonym_replacement(words, n_sr)
		augmented_sentences.append(' '.join(a_words))

	# # ri Random Insertion, 임의의 단어를 삽입
	# for _ in range(num_new_per_technique):
	# 	a_words = random_insertion(words, n_ri)
	# 	augmented_sentences.append(' '.join(a_words))

	# rs Random Swap 문장 내 임의의 두단어의 위치를 바꿈
	for _ in range(num_new_per_technique):
		a_words = random_swap(words, locations, n_rs)
		augmented_sentences.append(" ".join(a_words))

	# rd Random Deletion 임의의 단어를 삭제
	for _ in range(num_new_per_technique):
		a_words = random_deletion(words, locations, p_rd)
		augmented_sentences.append(" ".join(a_words))

	augmented_sentences = [get_only_hangul(sentence) for sentence in augmented_sentences]
	random.shuffle(augmented_sentences)

	if num_aug >= 1:
		augmented_sentences = augmented_sentences[:num_aug]
	else:
		keep_prob = num_aug / len(augmented_sentences)
		augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

	augmented_sentences.append(sentence)

	return augmented_sentences

if __name__ == "__main__":
	f = open("./output_disasterSMS2_location.txt", 'r')
	while True:
		sentence = f.readline()
		if not sentence: break
		tag_sentence = f.readline()
		dump =  f.readline()
		result = EDA(sentence, tag_sentence)
		print(result)

	# print(EDA("[경상북도청] 꽃동네노래방(유흥)(대구 북구 경진로1길5) 7/12~7/15 방문자는 가까운 보건소 선별진료소에서 검사	ORG-B ORG-B LOC-B AFW-B DAT-B CVL-B O O O O "))
