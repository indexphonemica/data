import iphon_configparser
from glob import glob

num_files = 0
num_missing = 0

for file in glob('doculects/*.ini'):
	doculect = iphon_configparser.parse(file)
	num_files += 1
	if 'phonotactics' not in doculect:
		num_missing += 1
		print(file)

print('{} out of {} complete ({}%)'.format(
	num_files - num_missing,
	num_files,
	round((num_files - num_missing) / num_files * 100, 2)
))