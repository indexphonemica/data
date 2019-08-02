#!/usr/bin/env python3
import sys, re, subprocess
from os import path
import configparser

def parse_allophonic_rule(line):
	if not re.fullmatch('[^>]+>[^\/]+\/[^>\/\n]+', line):
		raise Exception('Invalid allophonic rule: {}'.format(line))

	phonemes = re.match('[^>]+', line).group(0).strip().split('+')
	allophone = re.search('>([^/]+)', line).group(1).strip()
	environment = re.search('/(.+)', line).group(1).strip()
	rule_type = 'strict'

	if allophone[0] == '~':
		allophone = allophone[1:].strip()
		rule_type = 'variant'
	allophones = allophone.split('~')

	return {'phonemes': phonemes, 'allophones': allophones, 'environment': environment, 'rule_type': rule_type}

def no(section, prop):
	if prop not in section:
		return True
	if section[prop] is None:
		return True
	if section[prop] in set(['REQUIRED', 'IDEAL', 'OPTIONAL', 'OPTIONAL (but REQUIRED if there\'s no glottolog ID)']):
		return True
	if section[prop] == '':
		return True
	return False

# -- Tests -- 
def validate(doculect):
	if set(doculect.sections()) != set(['core', 'source', 'notes', 'phonemes', 'allophonic_rules']):
		raise Exception('Sections are incorrect (should be core, source, notes, phonemes, allophonic_rules)')

	# -- Core tests -- 
	if no(doculect['core'], 'name'):
		raise Exception('Missing property: core -> name')
	if no(doculect['core'], 'glottocode'):
		raise Exception('Missing property: core -> glottocode')

	# -- Source tests --
	if no(doculect['source'], 'glottolog'):
		print('Warning: No glottolog ID provided for source - are you sure?')
		for prop in ['author', 'title', 'year']:
			if no(doculect['source'], prop):
				raise Exception('Missing required property for source without glottolog ID: {}'.format(prop))
	elif not re.fullmatch('[0-9]+', doculect['source']['glottolog']):
		raise Exception('Invalid source glottolog ID: {}'.format(doculect['source']['glottolog']))

	if no(doculect['source'], 'url'):
		print('Warning: No URL provided for source - are you sure?')

	# -- Phonemes tests --
	# TODO: once we have more entries, keep a cache and warn for each new (unattested so far in IPHON) phoneme
	# also, ensure proper diacritic ordering

	phonemes = list(doculect['phonemes'])

	if set(phonemes) != set(doculect['phonemes']):
		raise Exception('Duplicate phoneme')

	if phonemes[0] == 'REQUIRED':
		raise Exception('No phonemes given')

	canonical_phonemes = [phoneme.split('|')[0] for phoneme in phonemes]

	# -- Allophonic rules tests --
	for rule_raw in doculect['allophonic_rules']:
		rule = parse_allophonic_rule(rule_raw)
		for phoneme in rule['phonemes']:
			if phoneme not in canonical_phonemes:
				raise Exception('Phoneme {} in rule {} not listed as canonical in phonemes section'.format(phoneme, rule))

	return True

if __name__ == '__main__':
	filename = sys.argv[1]
	doculect = configparser.ConfigParser(allow_no_value=True)
	doculect.read(path.join('doculects', '{}.ini'.format(filename)), encoding='utf-8')
	validate(doculect) # if it's invalid, this will throw an exception
	subprocess.run(['git', 'add', path.join('doculects', '{}.ini'.format(filename))])