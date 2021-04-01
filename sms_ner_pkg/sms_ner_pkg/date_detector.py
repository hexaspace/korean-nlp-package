import sms_ner_pkg.sms_ner_pkg.data_loader as dataLoader

class DateDetector():
    def __init__(self):
        self.dates = []
        self.dateWords = [
            '오늘', '내일', '모레', '글피', '주말', '휴일'
            '월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일',
            '월욜', '화욜', '수욜', '목욜', '금욜', '토욜', '일욜',
            '이번주', '다음주', '이번 주', '다음 주', '담주'
        ]
        self.targetWords = ['월', '일', '뒤', '후']
        self.isPrevValid = False

    def getDates(self):
        return self.dates

    def addDate(self, date):
        self.dates.append(date)

    def hasNumbers(self, word):
        return any(char.isdigit() for char in word)

    # 날짜와 관련된 단어인지 유효성 검사
    def isValid(self, targetWord, word):
        if targetWord=='월' or targetWord=='일':
            return self.hasNumbers(word)
        if targetWord=='뒤' or targetWord=='후':
            return

    # 단어에 포함된 특수문자 제거
    def deleteSpecialCharacters(self, word):
        word = ''.join(char for char in word if char.isalnum())
        return word

    # 각 문장에 포함된 날짜와 관련된 단어를 detect
    def date_detector(self, messages):
        for message in messages:
            words = message.split(' ')
            for word in words:
                for dateWord in self.dateWords:
                    if dateWord in word:
                        _dateWord = self.deleteSpecialCharacters(dateWord) #특수문자 삭제
                        self.addDate(_dateWord)
                        self.isPrevValid = True
                for targetWord in self.targetWords:
                    if targetWord in word:
                        if self.isValid(targetWord, word):
                            _word = self.deleteSpecialCharacters(word) #특수문자 삭제
                            self.addDate(_word.split('에')[0]) #조사 삭제
                            self.isPrevValid = True
                    else: self.isPrevValid = False

def getMessages():
    messages = dataLoader._read_data_file()
    return messages

if __name__ == "__main__":
    dateDetector = DateDetector()
    # messages = getMessages()
    messages = ['화요일이나 수요일에 만날래?', '오늘 어때', '3일에 볼까?', '내일은 별로야?', '4일 뒤', '주말 어때', '2월 1일?']
    dateDetector.date_detector(messages)
    print(dateDetector.dates)
