import setuptools

with open( 'README.rst', 'r' ) as f:
	long_desc = f.read()

classifiers = [
	"Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

project_urls = {
	'Documentation': 	'https://github.com/bicarlsen/juno',
	'Source Code': 		'https://github.com/bicarlsen/juno',
	'Bug Tracker':		'https://github.com/bicarlsen/juno/issues'
}


setuptools.setup(
	name='juno-observer',
	version = '0.0.1',
	author='Brian Carlsen',
	author_email = 'carlsen.bri@gmail.com',
	description = 'Jupyter file watcher.',
	long_description = long_desc,
	long_description_content_type = 'text/x-rst',
	url = 'https://github.com/bicarlsen/juno',
	packages = setuptools.find_packages(),
	project_urls = project_urls,
	classifiers = classifiers,
	
	install_requires = [
	],

	package_data = {
	},

	entry_points = {
		'console_scripts': []
	}
)