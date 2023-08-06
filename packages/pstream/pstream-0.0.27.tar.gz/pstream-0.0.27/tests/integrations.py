import unittest

from pstream import AsyncStream
from tests._async.utils import run_to_completion


class Integrations(unittest.TestCase):

    @run_to_completion
    async def test1(self):
        got = await AsyncStream(range(0, 9)).map(lambda x: x - 1 if x % 2 == 0 else x + 1).collect()
        self.assertEqual(got, [-1, 2, 1, 4, 3, 6, 5, 8, 7])

    @run_to_completion
    async def test2(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).collect()
        self.assertEqual(got, [-1, 2, 1, 4, 3, 6, 8, 7])

    @run_to_completion
    async def test3(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().collect()
        self.assertEqual(got, [-1, 1, 2, 3, 4, 6, 7, 8])

    @run_to_completion
    async def test4(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().\
            group_by(lambda x: x % 2).collect()
        self.assertEqual(got, [[-1, 1, 3, 7], [2, 4, 6, 8]])

    @run_to_completion
    async def test5(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().\
            group_by(lambda x: x % 2).\
            flatten().collect()
        self.assertEqual(got, [-1, 1, 3, 7, 2, 4, 6, 8])

    @run_to_completion
    async def test6(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().\
            group_by(lambda x: x % 2).\
            flatten().\
            pool(4).collect()
        self.assertEqual(got, [[-1, 1, 3, 7], [2, 4, 6, 8]])

    @run_to_completion
    async def test7(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().\
            group_by(lambda x: x % 2).\
            flatten().\
            pool(3).collect()
        self.assertEqual(got, [[-1, 1, 3], [7, 2, 4], [6, 8]])

    @run_to_completion
    async def test8(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().\
            group_by(lambda x: x % 2).\
            flatten().\
            pool(3).\
            group_by(len).collect()
        self.assertEqual(got, [[[-1, 1, 3], [7, 2, 4]], [[6, 8]]])

    @run_to_completion
    async def test9(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().\
            group_by(lambda x: x % 2).\
            flatten().\
            pool(3).\
            group_by(len).\
            flatten().flatten().collect()
        self.assertEqual(got, [-1, 1, 3, 7, 2, 4, 6, 8])

    @run_to_completion
    async def test10(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().\
            group_by(lambda x: x % 2).\
            flatten().\
            pool(3).\
            group_by(len).\
            flatten().flatten().\
            take(4).collect()
        self.assertEqual(got, [-1, 1, 3, 7])

    @run_to_completion
    async def test11(self):
        got = await AsyncStream(range(0, 9)).\
            map(lambda x: x - 1 if x % 2 == 0 else x + 1).\
            filter_false(lambda x: x == 5).\
            sort().\
            group_by(lambda x: x % 2).\
            flatten().\
            pool(3).\
            group_by(len).\
            flatten().flatten().\
            take(4).\
            chain(range(4)).collect()
        self.assertEqual(got, [-1, 1, 3, 7, 0, 1, 2, 3])


if __name__ == '__main__':
    unittest.main()
