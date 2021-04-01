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
        self.times.append(word)

    def hasNumbers(self, str):
        return any(char.isdigit() for char in str)

    # target이 포함된 word가 시간과 관련된 단어인지 유효성 검사
    def isValid(self, target, word):
        if word == '':
            return False
        elif target == '시' or target == '분':
            return self.hasNumbers(word)
        elif target == '반' or target == '후' or target == '뒤':
            return
        return True

    def time_detector(self, sentence):
        words = sentence.split(' ')

        # sentence 안에 시간과 관련된 단어만 times에 추가.
        for i in range(len(words)):
            word = words[i]
            timeChecked = False

            #timeWords 단어 검사
            for timeWord in timeWords:
                if timeWord in word:
                    timeChecked = True
                    validValues[i] = True
                    _time.append(word)
            #targetWords 단어 검사
            if not timeChecked:
                for target in targetWords:
                    if target in word:
                        ################### sudo code #####################
                        if '시' or '분': self.hasNumbers(word) ? append else continue
                        elif '반' or '후' or '뒤' validValues[i-1] ? validValues[i]=True , append : continue
        return _time

if __name__ == "__main__":
    messages = dataLoader._read_data_file()
    timeDetector = TimeDetector()
    timeDetector.time_detector()
    print(timeDetector.getTime())

