import iphon_configparser
from glob import glob
import argparse

REPORT_MAP = {}
REPORT_ALIASES = {}

class Report:
	def __init__(self, fn, name, aliases, help):
		REPORT_MAP[name] = self
		for alias in aliases:
			REPORT_ALIASES[alias] = name
		self.fn = fn
		self.aliases = aliases
		self.help = help

	def run(self):
		return self.fn()

def phonotactics_project():
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
Report(phonotactics_project, 'phonotactics', ['p', 'phono'], 'List doculects with no phonotactics section added yet')

def num_entries():
	doculect_count = 0
	language_count = 0
	for file in glob('doculects/*.ini'):
		doculect_count += 1
		if file[-6:-3] == '-1.':
			language_count += 1
	print('{} doculects representing {} languages'.format(doculect_count, language_count))
Report(num_entries, 'num_entries', ['ne'], 'List total numbers of doculects and languages')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('report', help='select a report (use \'help\' to list reports)')
	args = parser.parse_args()
	
	if args.report in REPORT_MAP:
		REPORT_MAP[args.report].run()
	else:
		if args.report in REPORT_ALIASES:
			REPORT_MAP[REPORT_ALIASES[args.report]].run()
		elif args.report == 'help':
			for report_name, report_obj in REPORT_MAP.items():
				print('{} ({}): {}'.format(report_name, ', '.join(report_obj.aliases), report_obj.help))
		else:
			print("Can't find that report - use 'help' to list reports.")