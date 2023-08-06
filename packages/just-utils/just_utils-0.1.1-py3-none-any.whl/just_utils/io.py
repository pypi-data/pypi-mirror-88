'''
Author: shy
Description: 读写各种格式的文件，文件夹等等
LastEditTime: 2020-12-11 17:04:57
'''
import os, yaml
from pathlib import Path, PosixPath
from easydict import EasyDict as edict

def checkfolder(paths):
	if isinstance(paths, str):
		if not Path(paths).is_dir():
			os.mkdir(paths)
			print("Created new directory in %s" % paths)

	if isinstance(paths, PosixPath):
		if not Path(paths).is_dir():
			Path.mkdir(paths)
			print("Created new directory in %s" % paths)

def read_yml(yml_file):
	with open(yml_file) as f:
		cfg = edict(yaml.safe_load(f))
	return cfg

