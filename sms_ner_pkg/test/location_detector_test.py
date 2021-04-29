import unittest
import location_detector, data_loader
import os

class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, True)

    def setUp(self):
        os.chdir(r'C:\Users\hexa6/Desktop/git/nlp_proj/korean-nlp-package\sms_ner_pkg\sms_ner_pkg\data')
        self.current_path = os.getcwd()

    def test_delete_jamo(self):
        input_string = "가나ㄷ라마ㅜㅜ미도ㅢ뷁^^쿠~ㅁ"
        output_string = "가나라마미도뷁쿠"
        s = location_detector._delete_jamo(input_string)
        self.assertEqual(s, output_string)
        #self.assertRaises(Exception, lambda: location_detector.delete_jamo(1123))

    def test_find_chosung(self):
        input_string = "까다롭군"
        output = "ㄲ"
        c = location_detector._find_chosung(input_string)
        self.assertEqual(c, output)

    def test_get_load_address(self):
        input1 = "시험일에는 서울특별시 성동구 왕십리로 222 공업센터본관 503호로 오세요."
        output1 = "서울특별시 성동구 왕십리로 222 공업센터본관 503호"
        input2 = "약속장소는 부평로 31, 101동입니다."
        output2 = "부평로 31, 101동"
        input3 = "이렇게 된 이상 서울특별시 종로구 청와대로 1 대통령 비서실 로 간다"
        output3 = "서울특별시 종로구 청와대로 1"
        s1 = location_detector._get_load_address(input1)
        self.assertIn(output1, s1)    #띄어쓰기로 in
        s2 = location_detector._get_load_address(input2)
        self.assertIn(output2, s2)
        s3 = location_detector._get_load_address(input3)
        self.assertIn(output3, s3)

    def test_get_subway_location(self):
        input = "dsf"


    def test_get_store_location(self):
        input = "dsf"

    def test_get_locations_by_konlpy(self):
        input = "dsf"

    def test_loc_detector(self):
        input = ["10월 정기 미팅 장소는 코엑스 입니다.", "주소는 서울특별시 강남구 영동대로 513 (삼성동, 코엑스) 입니다.", "14시 반까지 봉은사역의 세븐일레븐 앞에 늦지 않게 도착하세요."]
        output = ["서울특별시 강남구 영동대로 513", "봉은사역", "세븐일레븐"]
        l = location_detector.loc_detector(self.current_path, input)
        boolval = True
        for o in output:
            if o not in l:
                boolval = False

        self.assertTrue(boolval)

if __name__ == '__main__':
    unittest.main()
