import os
import sms_ner_pkg.sms_ner_pkg.data_loader as dataLoader

class TimeDetector():
    def __init__(self):
        self.times = []
        self.targetWords = ['시', '분', '반', '후', '뒤', ]
        self.timeWords = [
            '퇴근 후', '점심시간', '쉬는시간', '아침', '점심', '저녁', '밤', '새벽',
            '한시', '두시', '세시', '네시', '다섯시', '여섯시', '일곱시', '여덟시', '아홉시', '열시', '열한시', '열두시'
        ]

    def getTime(self):
        return self.times

    def addTime(self, word):
        if word: self.times.append(word)

    def hasNumbers(self, str):
        return any(char.isdigit() for char in str)

    # 단어에 포함된 특수문자 제거
    def deleteSpecialCharacters(self, word):
        word = ''.join(char for char in word if char.isalnum())
        return word

    # 시간과 관련된 단어 외의 글자들은 삭제
    def getOnlyTimeWord(self, _word):
        word = []
        def slice_list_by_targetWord(targetWord, word):
            idx = word.index(targetWord)
            return word[:idx+1]
        def slice_list_from_targetWord(targetWord, word):
            idx = word.index(targetWord)
            return word[idx:]

        #후, 뒤 -> 반 -> 분 -> 시 우선순위대로 자른다.
        targetWords = ['후', '뒤', '반', '분', '시']
        for targetWord in targetWords:
            if targetWord in _word:
                word = slice_list_by_targetWord(targetWord, _word)
                break
        # 첫번째 숫자 이전의 글자들 삭제
        for character in _word:
            if self.hasNumbers(character):
                word = slice_list_from_targetWord(character, word)
                break
        return word

    # target이 포함된 word가 시간과 관련된 단어인지 유효성 검사
    def isValid(self, word, idx):
        if word == '':
            return False
        elif '시' in word or '분' in word:
            return self.hasNumbers(word)
        elif word in '반' or word in '후' or word in '뒤':
            if self.hasNumbers(word) :
                return True
            elif self.words[idx-1] in self.times:
                return True
            else: return False
        return False

    def time_detector(self, sentence):
        words = sentence.split(' ')

        # sentence 안에 시간과 관련된 단어만 times에 추가.
        for word in words:
            #timeWords 단어 검사
            for timeWord in self.timeWords:
                if timeWord in word:
                    _word = self.deleteSpecialCharacters(word)
                    _word = self.getOnlyTimeWord(_word)
                    self.addTime(_word)
            #targetWords 단어 검사
            for targetWord in self.targetWords:
                if targetWord in word:
                    idx = words.index(word)
                    if self.isValid(word,idx):
                        _word = self.deleteSpecialCharacters(word)
                        _word = self.getOnlyTimeWord(_word)
                        self.addTime(_word)
        return self.times

if __name__ == "__main__":
    os.chdir(r'C:\Users\ghio1\PycharmProjects\senior-project-2021\sms_ner_pkg\sms_ner_pkg\data')
    current_path = os.getcwd()
    messages = dataLoader.sms_data_loader(current_path)
    timeDetector = TimeDetector()
    for message in messages:
        timeDetector.time_detector(message)
    print(timeDetector.getTime())

