from setuptools import setup,find_packages

classifiers=[
'Development Status :: 5 - Production/Stable',
'Intended Audience :: Education',
'Operating System :: Microsoft :: Windows :: Windows 10',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3.7'
]

setup(
	name='varlock_throw',
	version='0.0.2',
	description='funtion to return scambled list of word when a list of word is inputed',
	long_description=open('README.txt').read()+'\n\n'+ open('CHANGELOG.txt').read(),
	url='',
	author='Varun Dineshan',
	author_email='cc2164@gmail.com',
	license='MIT',
	classifiers=classifiers,
	keywords='scramble',
	packages=find_packages(),
	install_requires=['random']
)