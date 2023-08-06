import sys
import os

print('Hello, World!')

data = {
	"path":sys.path,
	"current_dir":os.getcwd(),
	"__file__":__file__
}

for x in data.keys():
	print(f'\n{x}:\t\t\t\t{data[x]}\n')