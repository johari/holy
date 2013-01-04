from holy import Holy
import unittest
import yaml

class TestRuby(unittest.TestCase):
  pass

y = yaml.load(open("test_ruby.yaml").read())
for test in y.keys():
  def make_test(test):
    def test_def(self):
      import os
      if os.environ["debug"]:
        os.environ["HACK"] = test
      res = Holy(y[test]["py"]).toRuby()
      if os.environ["debug"]:
        open("tmp/foo_%s" % test, "w").write(res)
      self.assertEqual(res, y[test]["rb"])
    return test_def
  crafted_test = make_test(test)
  crafted_test.__name__ = "test_%s" % test
  setattr(TestRuby, crafted_test.__name__, crafted_test)

if __name__ == '__main__':
  unittest.main()
