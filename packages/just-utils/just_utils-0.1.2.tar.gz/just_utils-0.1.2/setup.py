'''
Author: shy
Description: 
LastEditTime: 2020-12-15 16:12:21
'''
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="just_utils",
	version="0.1.2",
	author="Hansoluo",
	author_email="hansoluo757@gmail.com",
	description="A series of convenience functions to help training large image dataset with CNN",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Hansoluo/cvutils.git",
	packages=['just_utils'],
	install_requires=['easydict', 'PyYAML'],
	python_requires='>=3.6',
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	),
)