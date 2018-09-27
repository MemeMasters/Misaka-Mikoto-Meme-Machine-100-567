import unittest

from dm_assist import util

# see https://docs.python.org/3.5/library/unittest.html for info on creating a testcase

class TestDieParser(unittest.TestCase):

    def fail_on_success(self, roll):
        try:
            util.parse_die_roll(roll)
            self.fail(roll + ' should not be a valid roll format')
        except util.BadFormat:
            pass

    def test_die_parse(self):

        self.fail_on_success('aah')

        self.fail_on_success('xd5')

        self.fail_on_success('5.4d1')

        self.fail_on_success('1d0')


