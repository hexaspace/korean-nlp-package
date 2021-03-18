import os

# 단어에 숫자가 포함되었는지 확인
def hasNumbers(str):
    return any(char.isdigit() for char in str)

# 이전 단어가 valid였는지 확인
prev = ''
def savePrevValid(value):
    prev = value

def valid(target,_word):
    if _word=='': return False
    elif target=='시' or target=='분':
        return hasNumbers(_word)
    elif target=='반' or target=='후' or target=='뒤':
        # if prev==True: return True
        # else:
        return False
    return True

def time_detector(sentence):
    _time = []
    prev = ''
    targetWords = [
        '시', '분', '퇴근 후', '점심시간', '쉬는시간', '아침', '점심', '저녁', '밤', '새벽',
        '한시', '한 시', '두시', '두 시', '세시', '세 시', '네시', '네 시', '다섯시', '다섯 시', '여섯시', '여섯 시', '일곱시', '일곱 시', '여덟시', '여덟 시',
        '아홉시', '아홉 시', '열시', '열 시', '열한시', '열한 시', '열두시', '열두 시',
        '반', '후', '뒤'
    ]
    words = sentence.split(' ')
    
    # sentence 안에 시간과 관련된 단어가 있는지 확인
    for i in range(len(words)):
        for target in targetWords:
            if target in words[i]:
                _value = valid(target, words[i])
                savePrevValid(_value)
                if _value:
                    _time.append(words)
    return _time

def data_reader(root_path):
    file_path = os.path.join(root_path, 'copiedinput.txt')
    sentences = []
    for line in open(file_path, encoding="utf-8"):
        line = line.strip()
        if line:
            line = line.split('   ')
            sentences.append(line[len(line)-1])
    return sentences

if __name__ == "__main__":
    sentences = data_reader("data")
    print(len(sentences))

    time = []
    for sentence in sentences:
        _time = time_detector(sentence)
        if _time:
            time.append(_time)
    print(time)