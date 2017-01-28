import unittest


class MITMITestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_basic_test(self):
        self.assertEqual(1, 1)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
