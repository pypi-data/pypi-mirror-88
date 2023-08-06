from setuptools import setup, find_packages

classification = [
	'Development status :: 5 - Production/stable',
	'Intended Audience :: Education',
	'Operating System :: Linux :: ubuntu',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: PYthon :: 3'
]

setup(
	name='kuldeepcalculator',
	version='0.0.1',
	description='A baisc calulcator',
	Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
	url='',
	author='kuldeep khatana',
	author_email='kuldeep.si.softprodigy@gmail.com',
	License='MIT',
	classifiers=[],
	keywords='calulcator',
	package=find_packages(),
	install_requires=['']


)