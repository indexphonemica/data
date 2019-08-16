#!/usr/bin/env python3
import sys, re, argparse
from os import path
import configparser

def validate_glottocode(glottocode):
	if not re.match('[a-z]{4}[0-9]{4}', glottocode):
		raise Exception('Invalid glottocode')

def format_path(glottocode, i):
	return 'doculects/{}-{}.ini'.format(glottocode, i)

def find_path(glottocode):
	i = 0
	already_exists = True
	while already_exists:
		i += 1
		if not path.exists(format_path(glottocode, i)):
			already_exists = False
	return format_path(glottocode, i)

def maybe(obj, key, otherwise=None):
	if key in obj:
		return obj[key]
	else:
		return otherwise

def from_bibkey(glottocode, bibkey, name):
	"""Look up source info from the Glottolog bibkey of the source.
	You'll probably want to change GLOTTOLOG_PATH here."""
	GLOTTOLOG_PATH = path.expanduser('~/Documents/glottolog-4.0')

	from pyglottolog import Glottolog
	g = Glottolog(GLOTTOLOG_PATH)

	languoid = g.languoid(glottocode)	
	ref = [x for x in languoid.sources if x.key == bibkey]
	if not ref:
		raise Exception('Reference not found')

	source = ref[0].get_source(g)
	return source.fields

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Initialize a new inventory file from a Glottocode or Glottolog bibkey.')

	parser.add_argument('glottocode', metavar='glottocode', type=str, help='The Glottocode of the doculect.')
	parser.add_argument('-b', '--bibkey', dest='bibkey', nargs='?', default=None, help='The Glottolog bibkey of the source.')
	parser.add_argument('-n', '--name', dest='name', nargs='?', default='REQUIRED', help='The name of the doculect as given in the source.')
	parser.add_argument('--simple', dest='simple', action='store_const', const='simple', default=False, help='Simple mode (omit unfilled optional keys and phoneme/allophone default text)')

	args = parser.parse_args()
	validate_glottocode(args.glottocode)

	if args.bibkey:
		ref_info = from_bibkey(args.glottocode, args.bibkey, args.name)
	else:
		ref_info = {}

	ini_path = find_path(args.glottocode)

	# build the file
	ini = configparser.ConfigParser(allow_no_value=True)
	ini['core'] = {
		'name': args.name
	,	'glottocode': args.glottocode
	,	'dialect': 'OPTIONAL'
	,	'dialect_name': 'OPTIONAL'
	}

	ini['source'] = {
		'glottolog': (args.bibkey if args.bibkey else 'IDEAL')
	,	'url':       "OPTIONAL"
	,	'author':    maybe(ref_info, 'author',    "OPTIONAL (but REQUIRED if there's no glottolog ID)")
	,	'title':     maybe(ref_info, 'title',     "OPTIONAL (but REQUIRED if there's no glottolog ID)")
	,	'publisher': maybe(ref_info, 'publisher', "OPTIONAL")
	,	'volume':    maybe(ref_info, 'volume',    "OPTIONAL")
	,	'number':    maybe(ref_info, 'number',    "OPTIONAL")
	,	'year':      maybe(ref_info, 'year',      "OPTIONAL (but REQUIRED if there's no glottolog ID)")
	,   'pages':     maybe(ref_info, 'pages',     "OPTIONAL")
	}

	if args.simple:
		for key in ini['core'].keys():
			if ini['core'][key] == 'OPTIONAL':
				ini['core'].pop(key)
		for key in ini['source'].keys():
			if ini['source'][key] == 'OPTIONAL':
				ini['source'].pop(key)

		ini['phonemes'] = {}
		ini['allophonic_rules'] = {}
	else:
		ini['phonemes'] = {
			'REQUIRED': None
		}

		ini['allophonic_rules'] = {
			'PHONEME > IPA_REALIZATION / DESCRIPTION_OF_ENVIRONMENT': None
		,	'PHONEME+PHONEME > REALIZATION_OF_CLUSTER / DESCRIPTION_OF_ENVIRONMENT': None
		,	'PHONEME ~ FREE_VARIATION / DESCRIPTION_OF_ENVIRONMENT': None
		,	'PHONEME+PHONEME >~ FREE_VARIATION_FOR_CLUSTER / DESCRIPTION_OF_ENVIRONMENT': None
		}

	with open(ini_path, 'w') as out:
		ini.write(out)
	print(ini_path)