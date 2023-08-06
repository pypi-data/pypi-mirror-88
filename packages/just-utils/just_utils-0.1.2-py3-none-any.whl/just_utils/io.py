'''
Author: shy
Description: 读写各种格式的文件，文件夹等等
LastEditTime: 2020-12-15 16:11:32
'''
import os, yaml
from pathlib import Path, PosixPath
from easydict import EasyDict as edict

def checkfolder(paths):
	""" paths type can be `str, PosixPath, or list`
	"""
	paths = paths if isinstance(paths, list) else [paths]
	
	def creat_dir(x):
		x = Path(x)
		if x.is_dir():
			print(f"Dir {x} already exists")
		else:
			Path.mkdir(x)
			print(f"Created new dir {x}")
	
	list(map(creat_dir, paths))

def read_yml(yml_file):
	with open(yml_file) as f:
		cfg = edict(yaml.safe_load(f))
	return cfg