import sys

try:
    from importlib import util
except:
    sys.stdout.write("\nIt seems that importlib library is not available on this machine. Please install pip (e.g. for Ubuntu, run 'sudo apt-get install python3-pip'.\n")
    sys.exit()

import glob

if util.find_spec("setuptools") is None:
    sys.stdout.write("\nIt seems that setuptools is not available on this machine. Please install pip (e.g. for Ubuntu, run 'sudo apt-get install python3-pip'.\n")
    sys.exit()
    
from setuptools import setup, find_packages

if sys.version_info <= (3,6):
    sys.exit('Sorry, Python < 3.7 is not supported.')

with open('README.md') as f:
    long_description = f.read()
	
setup(
    name='pyntacle',
    version='1.3.2',
    author='Tommaso Mazza',
    author_email='bioinformatics@css-mendel.it',
	description="A Python package for network analysis based on non-canonical metrics and HPC-Computing",
	long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://pyntacle.css-mendel.it",
    packages=find_packages(),
    include_package_data=True,
    license='GPL3',
    setup_requires=['numpy'],
    install_requires=[
		"pandas==1.1.4",
		"seaborn==0.11.0",
		"setuptools",
		"colorama==0.4.4",
		"numba==0.51.2",
		"ordered-set==4.0.2",
		"python-igraph==0.8.3",
		"xlsxwriter==1.3.7",
		"psutil",
    ],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
	project_urls={
		'Documentation': 'http://pyntacle.css-mendel.it:10080/#docs',
		'Source': 'https://github.com/mazzalab/pyntacle',
		'Tracker': 'https://github.com/mazzalab/pyntacle/issues',
		'Developmental plan': 'https://github.com/mazzalab/pyntacle/projects',
	},
	keywords='network, graph, systems biology, bioinformatics',
    python_requires='>=3.7,<3.8',
	entry_points={
		'console_scripts': [
			'pyntacle = pyntacle.pyntacle:App'
        ]
	},
)
