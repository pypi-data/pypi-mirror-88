'''
Author: shy
Description: 测试
LastEditTime: 2020-12-15 16:07:08
'''

import unittest
from pathlib import Path
from just_utils.io import checkfolder

class TestIO(unittest.TestCase):

	def test_single_path(self):
		path = "/mnt/shy/test_io/"
		checkfolder(path)
		self.assertTrue(Path(path).is_dir())
		path = Path("/mnt/shy/test_io/")
		checkfolder(path)
		self.assertTrue(Path(path).is_dir())

	def test_multi_path(self):
		paths = [   "/mnt/shy/test_io/1/",
					"/mnt/shy/test_io/2/",
					"/mnt/shy/test_io/3/", ]

		checkfolder(paths)
		for x in paths:
			self.assertTrue(Path(x).is_dir())


if __name__ == "__main__":
	unittest.main()