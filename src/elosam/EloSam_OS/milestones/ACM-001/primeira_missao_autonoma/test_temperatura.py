import unittest
from temperatura import celsius_para_fahrenheit

class TestTemperatura(unittest.TestCase):
    def test_celsius_0(self):
        self.assertEqual(celsius_para_fahrenheit(0), 32)

    def test_celsius_100(self):
        self.assertEqual(celsius_para_fahrenheit(100), 212)

    def test_celsius_neg40(self):
        self.assertEqual(celsius_para_fahrenheit(-40), -40)

def main():
    unittest.main(argv=[''], exit=False)

if __name__ == '__main__':
    main()