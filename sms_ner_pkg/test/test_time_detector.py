# https://dzone.com/articles/7-popular-unit-test-naming

import unittest
from sms_ner_pkg.sms_ner_pkg import time_detector

class TestTimeDetector(unittest.TestCase):
    times = []

    # Create instance
    def setUp(self):
        self.instance = time_detector.TimeDetector()

    def test_hasNumbers(self):
        self.assertEqual(self.instance.hasNumbers('2시'), True)
        self.assertEqual(self.instance.hasNumbers('한시'), False)

    # def test_addTime(self):
    #     self.instance.addTime('2시')
    #     self.assertEqual(self.times, ['2시'])

    def test_deleteSpecialCharacters(self):
        result = self.instance.deleteSpecialCharacters('!2시?*')
        self.assertEqual(result, '2시')

    def test_getOnlyTimeWord(self):
        testWords = ['2시후에', '1시30분', '다섯시에']
        answers = ['2시후', '1시30분', '다섯시']
        for i in range(len(testWords)):
            result = self.instance.getOnlyTimeWord(testWords[i])
            self.assertEqual(result, answers[i])

    # isValid의 True, False 판단 검사
    # def test_isValid_TrueFalse(self):
    #     testWords = ['3시', '3시반', '두시반에', '세시가', '시계']
    #     answers = [True, True, True, True, False]
    #     for i in range(len(testWords)):
    #         print(i)
    #         result = self.instance.isValid(testWords, testWords[i])
    #         self.assertEqual(result, answers[i])

    # words 내에 없는 word가 들어왔을 경우
    def test_isValid_notIncluded(self):
        words = ['a', 'b', 'c']
        result = self.instance.isValid(words, 'd')
        self.assertEqual(result, False)

    # isValid의 이전 단어의 유효성에 따라 True, False 판단
    # def test_isValid_previousWordValidity(self):
        # sentence = '3시 반이나 두시반에 볼까? 세시가 나으려나 시계 보고 알려줘'
        # words = sentence.split(' ') #['세시', '반이나', '두시반에', '볼까?', '3시가', '나으려나', '시계', '보고', '알려줘']

    #     self.times = []
    #     testWords = ['2시', '반', '1시', '4시반', '30분후']
    #     times = ['2시']
    #     answers = ['2시', '1시', '4시반', '30분']
    #     for testWord in testWords:
    #         result = self.instance.isValid(testWords, testWord)
    #     self.assertEqual(result, True)
    #     result = self.instance.isValid(testWords, '반차')
    #     self.assertEqual(result, False)

    def test_timeDetector(self):
        sentences = ['우리 3시에 보자', '14시반어때', '2시랑 3시반 중에 뭐가 좋아?']
        answers = ['3시', '14시반', '2시', '3시반']
        for i in range(len(sentences)):
            result = self.instance.time_detector(sentences[i])
        self.assertEqual(result, answers)

if __name__ == '__main__':
    unittest.main()