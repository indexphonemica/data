#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re, argparse
from os import path
import iphon_configparser

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

def maybe(obj, key, otherwise=None, filters=None):
	if key in obj and obj[key] and (filters is None or obj[key] not in filters):
		return obj[key]
	else:
		return otherwise

def sil_pacific_label(field_reap):
	  key = field_reap.find('div', 'field-label').text
	  vals = [field_item.text for field_item in field_reap.find_all('div', 'field-item')]
	  return (key, vals)

def from_sil_pacific(id_or_url):
	"""Look up source info from silpacific.org.
	Remap the fields we already store, but also store all the rest - why not."""
	# TODO: can we also get Glottolog bibkeys? Probably not...
	if re.match('[0-9]+', id_or_url):
		id = id_or_url
	elif re.match('https?:\/\/(?:www\.|)silpacific.org/resources/archives/([0-9]+)', id_or_url):
		id = re.match('https?:\/\/(?:www\.|)silpacific.org/resources/archives/([0-9]+)', id_or_url)[1]
	else:
		raise Exception('Invalid SIL ID')

	import requests
	from bs4 import BeautifulSoup

	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	page = requests.get('http://www.silpacific.org/resources/archives/{}'.format(id), headers=headers)
	soup = BeautifulSoup(page.text, 'html.parser')

	# TODO: should probably check for 403s and whatnot

	reap_data = soup.find_all('div', 'reap-data')

	res = dict([sil_pacific_label(f) for f in soup.find_all('div', 'field-reap')])

	if res == {}:
		raise Exception('Nothing found - wrong ID?')

	# Calculate properties. None values are replaced by defaults later.
	author = None
	if 'Authors:' in res:
		author = '; '.join(res['Authors:'])

	publisher = None
	if 'Publication Status:' in res and res['Publication Status:'][0] == "Draft (posted 'as is' without peer review)":
		publisher = 'SIL Pacific' # so far it's just been SIL but we may as well be more... spacific B)

	title = None
	if soup.find(id='page-title') and soup.find(id='page-title').find('h2', 'page-title'):
		title = soup.find(id='page-title').find('h2', 'page-title').text

	year = None
	if 'Date Created:' in res and res['Date Created:'][0] not in set(['n.d.', 'nd']):
		year = int(re.match('([0-9]+)', res['Date Created:'][0])[0]) # in case of e.g. 1999-03
	elif 'Issue Date:' in res and res['Issue Date:'][0] not in set(['n.d.', 'nd']):
		year = int(re.match('([0-9]+)', res['Issue Date:'][0])[0])

	pages = None
	if 'Extent:' in res and re.match('([0-9]+) pages', res['Extent:'][0]):
		pages = re.match('([0-9]+) pages', res['Extent:'][0])[1]

	return {
		'url':       'https://silpacific.org/resources/archives/{}'.format(id)
	,	'author':    author
	,	'title':     title
	,	'publisher': publisher
	,	'year':      year
	,	'pages':     pages
	}

def from_bibkey(glottocode, bibkey):
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
	parser.add_argument('-b', '--bibkey',    dest='bibkey',       nargs='?', default=None, help='The Glottolog bibkey of the source.')
	parser.add_argument('--sp',              dest='sil_pacific',  nargs='?', default=None, help='The SIL Pacific URL of the source page, or the ID in /resources/archives. (https://www.silpacific.org/resources/archives/#####)')
	parser.add_argument('-n', '--name',      dest='name',         nargs='?', default='REQUIRED', help='The name of the doculect as given in the source.')
	parser.add_argument('-d', '--dialect-name', dest='dialect_name', nargs='?', default='OPTIONAL', help='The name of the dialect.')
	parser.add_argument('--simple', dest='simple', action='store_const', const='simple', default=False, help='Simple mode (omit unfilled optional keys and phoneme/allophone default text)')

	parser.add_argument('-t', dest='phon_invs_tb', action='store_const', const='phon_invs_tb', default=False, help='Add language from Phonological Inventories of Tibeto-Burman Languages')

	args = parser.parse_args()
	validate_glottocode(args.glottocode)

	ref_info = {}

	if args.bibkey:
		ref_info.update(from_bibkey(args.glottocode, args.bibkey))
	if args.sil_pacific:
		ref_info.update(from_sil_pacific(args.sil_pacific))

	if args.phon_invs_tb:
		args.simple = True
		args.bibkey = 'hh:hld:Namkung:Tibeto-Burman'
		ref_info.update(from_bibkey(args.glottocode, args.bibkey))
		ref_info['url'] = 'https://stedt.berkeley.edu/pubs_and_prods/STEDT_Monograph3_Phonological-Inv-TB.pdf'
		ref_info['author'] = 'Namkung, Ju'

	ini_path = find_path(args.glottocode)

	# build the file
	ini = iphon_configparser.parser()
	ini['core'] = {
		'name': args.name
	,	'glottocode': args.glottocode
	,	'dialect': 'OPTIONAL'
	,	'dialect_name': args.dialect_name
	}

	ini['source'] = {
		'glottolog': (args.bibkey if args.bibkey else "IDEAL")
	,	'url':       maybe(ref_info, 'url',       "IDEAL")
	,	'doi':		 maybe(ref_info, 'doi',       "OPTIONAL")
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

		ini['notes'] = {}
		ini['phonotactics'] = {}
		ini['phonemes'] = {}
		ini['allophonic_rules'] = {}
	else:
		ini['notes'] = {'OPTIONAL': None}
		ini['phonotactics'] = {
			'max_initial': 'REQUIRED IF no_info IS NOT PRESENT'
		,	'max_final':   'REQUIRED IF no_info IS NOT PRESENT'
		}
		ini['phonemes'] = {
			'REQUIRED': None
		}

		ini['allophonic_rules'] = {
			'PHONEME > IPA_REALIZATION / DESCRIPTION_OF_ENVIRONMENT': None
		,	'PHONEME+PHONEME > REALIZATION_OF_CLUSTER / DESCRIPTION_OF_ENVIRONMENT': None
		,	'PHONEME ~ FREE_VARIATION / DESCRIPTION_OF_ENVIRONMENT': None
		,	'PHONEME+PHONEME >~ FREE_VARIATION_FOR_CLUSTER / DESCRIPTION_OF_ENVIRONMENT': None
		}

	with open(ini_path, 'w', encoding='utf-8') as out:
		ini.write(out)
	if args.sil_pacific:
		with open('last_sp.txt', 'w', encoding='utf-8') as out:
			out.write(args.sil_pacific)
	elif args.phon_invs_tb:
		with open('last_tb.txt', 'w', encoding='utf-8') as out:
			out.write(args.name)
	print(ini_path)