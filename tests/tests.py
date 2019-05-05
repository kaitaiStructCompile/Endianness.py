#!/usr/bin/env python3
import itertools
import os
import sys
import unittest
from pathlib import Path

from rangeslicetools import *

from Endianness import *

sys.path.insert(0, str(Path(__file__).absolute().parent.parent))


class Tests(unittest.TestCase):
	def testParsing_(self):
		testMatrix = {
			"l8": (Level(8, False),),
			"l2": (Level(2, False),),
			"b2": (Level(2, True),),
			"b8": (Level(8, True),),
			"l8b4": (Level(8, False), Level(4, True)),
			"l8b4l2": (Level(8, False), Level(4, True), Level(2, False)),
			"b8l4b2": (Level(8, True), Level(4, False), Level(2, True)),
			"l8l2": (Level(8, False), Level(2, False)),
			"b8b2": (Level(8, True), Level(2, True)),
		}
		for s, expectedRes in testMatrix.items():
			with self.subTest(s=s):
				res = tuple(parse_(s))
				self.assertEqual(res, expectedRes)

	def testSimplify(self):
		testMatrix = {
			(Level(8, False),): (Level(8, False),),
			(Level(2, False),): (Level(2, False),),
			(Level(2, True),): (),
			(Level(8, True),): (),
			(Level(8, False), Level(4, True)): (Level(8, False), Level(4, True)),
			(Level(8, False), Level(4, True), Level(2, False)): (Level(8, False), Level(4, True), Level(2, False)),
			(Level(8, True), Level(4, False), Level(2, True)): (Level(4, False), Level(2, True)),
			(Level(8, False), Level(2, False)): (Level(8, False),),
			(Level(8, True), Level(2, True)): (),
			(Level(8, False), Level(4, True), Level(2, True)): (Level(8, False), Level(4, True)),
		}
		for s, expectedRes in testMatrix.items():
			with self.subTest(s=s):
				res = tuple(simplify(s))
				self.assertEqual(res, expectedRes)

	def testParsing(self):
		testMatrix = {
			"l8": (Level(8, False),),
			"l2": (Level(2, False),),
			"b2": (),
			"b8": (),
			"l8b4": (Level(8, False), Level(4, True)),
			"l8b4l2": (Level(8, False), Level(4, True), Level(2, False)),
			"b8l4b2": (Level(4, False), Level(2, True)),
			"l8l2": (Level(8, False),),
			"b8b2": (),
			"l8b4b2": (Level(8, False), Level(4, True)),
		}

		for s, expectedRes in testMatrix.items():
			with self.subTest(s=s):
				res = parse(s)
				self.assertEqual(res, expectedRes)


class TestMapping(unittest.TestCase):
	maxDiff = None

	def _testMapping(self, encoded: str, testMatrix):
		e = Endianness.parse(encoded)

		for size, expectedRes in testMatrix.items():
			with self.subTest(encoded=encoded, e=e, size=size):
				m = EndiannessMapping(e, size)
				r = slice(size - 1, -1, -1)
				#print(r)
				res = m.encode(r)
				#print(m.forward.tree)
				#print(list(m.forward[r]))
				resOnlyIndexee = tuple(sorted((s.indexee for s in res), key=lambda r: r.start))
				#print(resOnlyIndexee)
				self.assertEqual(resOnlyIndexee, expectedRes)

	def testMappings(self):
		sizesLogs = tuple(i for i in range(3, 7))

		matrices = {
			"b8": {2 ** szLog: (slice(2 ** szLog - 1, -1, -1),) for szLog in sizesLogs},
			"l8": {2 ** szLog: tuple(reversed(schunks(slice(2 ** szLog - 1, -1, -1), 8))) for szLog in sizesLogs},
			"l8b4": {2 ** szLog: tuple(reversed(schunks(slice(2 ** szLog - 1, -1, -1), 8))) for szLog in sizesLogs},
		}
		for encoded, matrix in matrices.items():
			self._testMapping(encoded, matrix)


if __name__ == "__main__":
	unittest.main()
