'''
Author: shy
Description: 读写各种格式的文件，文件夹等等
LastEditTime: 2020-12-11 11:38:05
'''
import os
from pathlib import Path, PosixPath

def checkfolder(paths):
	if isinstance(paths, str):
		if not Path(paths).is_dir():
			os.mkdir(paths)
			print("Created new directory in %s" % paths)

	if isinstance(paths, PosixPath):
		if not Path(paths).is_dir():
			Path.mkdir(paths)
			print("Created new directory in %s" % paths)