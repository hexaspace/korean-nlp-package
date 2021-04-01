# 형식:
#  MethodName_StateUnderTest_ExpectedBehavior: There are arguments against this strategy that if method names change as part of code refactoring than test name like this should also change or it becomes difficult to comprehend at a later stage. Following are some of the example:
# 예시:
#  isAdult_AgeLessThan18_False
#  withdrawMoney_InvalidAccount_ExceptionThrown
#  admitStudent_MissingMandatoryFields_FailToAdmit

import unittest
from sms_ner_pkg.sms_ner_pkg import array

class TestArray(unittest.TestCase):
    """
    Test sum of all entries in array
    """
    def test_sum(self):
        instance = array.Array()
        result = instance.sum(6, '1 2 3 4 10 11')
        self.assertEqual(result, 31)

    """
    Make exceptions occur when the number of array entries is differenct  
    """
    def test_sum_raise_exception(self):
        self.assertRaises(Exception, lambda: array.Array().sum(5, '1 2 3 4 10 11'))