from holy import Holy
import unittest
import yaml

class TestRuby(unittest.TestCase):
  pass

import os
script_dir = os.path.dirname(__file__)

y = yaml.load(open(os.path.join(script_dir, "test_ruby.yaml")).read())
for test in y.keys():
  def make_test(test):
    def test_def(self):
      import os
      res = Holy(y[test]["py"]).toRuby()
      try:
        if os.environ["debug"]:
          os.environ["HACK"] = test
        if os.environ["debug"]:
          open("tmp/foo_%s" % test, "w").write(res)
          open("tmp/foo_%s_rb" % test, "w").write(y[test]["rb"])
      except KeyError:
        pass

      self.assertEqual(res, y[test]["rb"])
    return test_def
  crafted_test = make_test(test)
  crafted_test.__name__ = "test_%s" % test
  setattr(TestRuby, crafted_test.__name__, crafted_test)

if __name__ == '__main__':
  unittest.main()
