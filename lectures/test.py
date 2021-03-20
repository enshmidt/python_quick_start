import unittest

class TestStringMethods(unittest.TestCase):

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

class TestDummy(unittest.TestCase):

  def test_equal(self):
      self.assertEqual(1, 2)


unittest.main(exit=False)