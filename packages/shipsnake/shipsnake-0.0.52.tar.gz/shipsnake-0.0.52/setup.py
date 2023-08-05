#!/usr/bin/env python3

# +------------------------+                       
# | Created with ShipSnake |                       
# |                        |                       
# | Do not edit this file  |                       
# | directly. Insead       |                       
# | you should edit the    |                       
# | `shipsnake.toml` file. |                       
# +------------------------+    

import setuptools

try:
  with open("README.md", "r") as fh:
      long_description = fh.read()
except:
	long_description = "# ShipSnake\nA quick and easy way to distribute your python projects!\n### Contributors\n- Cole Wilson\n### Contact\n<cole@colewilson.xyz> "

setuptools.setup(
    name="shipsnake",
    version="0.0.52",
		scripts=['bin/shipsnake'],
#		entry_points={
#			'console_scripts': ['shipsnake=shipsnake.__main__'],
#		},
    author="Cole Wilson",
    author_email="cole@colewilson.xyz",
    description="A quick and easy way to distribute your python projects!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cole-wilson/shipsnake",
    packages=setuptools.find_packages(),
		install_requires=['toml', 'githubrelease'],
    classifiers=["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
		package_data={"": ['*.txt', '*.template'],},
		license="MIT",
		keywords='ship distribute package snake python freeze shipsnake setuptools',
)