# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import arvid

setup(
	name='arvid',

	version=arvid.__version__,

	packages=find_packages(),

	author="antcho",

	description="This module is used to compare two Salesforce .json conf file.",

	long_description=open('README.md').read(),

	include_package_data=True,

	url='https://github.com/Sylpheo/Arvid',

	classifiers=[
		"Programming Language :: Python",
		"Natural Language :: English",
		"Operating System :: OS Independent"
	],

	entry_points = {
		'console_scripts': [
			'arvid = arvid.arvid:main',
		]
	},

	license="MIT"
)