#!/usr/bin/env python3
import sys, re
from os import path

glottocode = sys.argv[1]
i = 0
already_exists = True

# TODO: regex match glottocode
if not re.match('[a-z]{4}[0-9]{4}', glottocode):
	raise Exception('Invalid glottocode')

blank_file = """[core]
name = REQUIRED
glottocode = REQUIRED
dialect = OPTIONAL

[source]
glottolog = IDEAL
url = IDEAL
author = OPTIONAL (but REQUIRED if there's no glottolog ID)
title = OPTIONAL (but REQUIRED if there's no glottolog ID)
publisher = OPTIONAL
volume = OPTIONAL
number = OPTIONAL
year = OPTIONAL (but REQUIRED if there's no glottolog ID)
pages = OPTIONAL

[notes]
OPTIONAL

[phonemes]
REQUIRED

[allophonic_rules]
PHONEME > IPA_REALIZATION / DESCRIPTION_OF_ENVIRONMENT
PHONEME+PHONEME > REALIZATION_OF_CLUSTER / DESCRIPTION_OF_ENVIRONMENT
PHONEME ~ FREE_VARIATION / DESCRIPTION_OF_ENVIRONMENT
PHONEME+PHONEME >~ FREE_VARIATION_FOR_CLUSTER / DESCRIPTION_OF_ENVIRONMENT
"""


while already_exists:
	i += 1
	if not path.exists('doculects/{}-{}.ini'.format(glottocode, i)):
		already_exists = False

with open('doculects/{}-{}.ini'.format(glottocode, i), 'w') as out:
	out.write(blank_file)