from setuptools import setup
import simplecfg

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name=simplecfg.MODULE_NAME,
	version=simplecfg.MODULE_VERSION,
	packages=[simplecfg.MODULE_NAME],
	url=simplecfg.MODULE_URL,
	license="Mozilla Public License version 2.0",
	author=simplecfg.MODULE_AUTHOR,
	author_email='',
	description=simplecfg.MODULE_DESCRIPTION,
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.3"
)
