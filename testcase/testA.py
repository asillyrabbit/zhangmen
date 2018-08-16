import unittest

class TestOne(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print('12345')
        pass

    def test_B_add(self):
        '''test add method'''
        print('add')
        a = 3 + 4
        b = 7
        self.assertEqual(a, b)

    def test_A_sub(self):
        '''test sub method'''
        print('sub')
        a = 10 - 5
        b = 5
        self.assertEqual(a, b)

    @classmethod
    def tearDownClass(self):
        print('654321')
        pass
