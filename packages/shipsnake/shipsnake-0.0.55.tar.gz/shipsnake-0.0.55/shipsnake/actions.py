import shipsnake.build
import toml
import sys
import os

with open('shipsnake.toml') as file:
	data = toml.loads(file.read())

if sys.platform.startswith('win'):
	shipsnake.build.main(data['latest_build'],[],nointeraction=True)


elif sys.platform.startswith('darwin') or True:
	shipsnake.build.main(data['latest_build'],[],nointeraction=True)

else:
	print('This is not being run on Mac and Windows.')