import sms_ner_pkg.sms_ner_pkg.data_loader as dataLoader
import re

class DateDetector():
    def __init__(self):
        self.dates = []
        self.dateWords = [
            '오늘', '내일', '모레', '글피'
            '월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일',
            '월욜', '화욜', '수욜', '목욜', '금욜', '토욜', '일욜',
            '이번주', '다음주', '이번 주', '다음 주'
        ]
        self.targetWords = ['월', '일']

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

    def date_detector(self, messages):
        for message in messages:
            words = message.split(' ')
            for word in words:
                for dateWord in self.dateWords:
                    if dateWord in word:
                        self.addDate(dateWord)
                for targetWord in self.targetWords:
                    if targetWord in word:
                        if self.isValid(targetWord, word):
                            # '3일에', '3월에'일 경우 조사 '에'를 삭제
                            self.addDate(word.split('에')[0])

def getMessages():
    messages = dataLoader._read_data_file()
    return messages

if __name__ == "__main__":
    dateDetector = DateDetector()
    # messages = getMessages()
    messages = ['화요일이나 수요일에 만날래?', '오늘 어떄', '3일 볼까?', '내일은 별로야?']
    dateDetector.date_detector(messages)
    print(dateDetector.dates)
