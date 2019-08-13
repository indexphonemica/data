# Index Phonemica

## Data format

Doculect entries are stored as Python INI files, named with the Glottocode of the language followed by a hyphen and an index number: `1` for the first entry for that Glottocode, `2` for the second, etc. 

Entry files have five headers: `core`, `source`, (optionally) `notes`, `phonemes`, and `allophonic_rules`.

### `core`

`core` stores two required attributes:
- `name`: the name of the doculect as given in the source
- `glottocode`: the Glottocode of the language

And two optional attributes:
- `notes`: Any notes relevant to the entry.
- `dialect`: the Glottocode of the specific dialect, if one is defined

### `source`

`source` stores the following attributes:
- `glottolog`
- `url`
- `author`
- `title`
- `publisher`
- `volume`
- `number`
- `year`
- `pages`

Enough information should be given that the paper can be found. At the minimum, a Glottolog ID should be provided if one is available; other information can then be added automatically from Glottolog when a numbered release of the Index is built.

### `notes`

`notes` stores notes relevant to the doculect entry. (For TODOs, add the literal string TODO.)

### `phonemes`

`phonemes` stores a set of phonemes, separated by newlines.

To mark a phoneme as marginal, enclose it in parentheses.

To mark a phoneme as only occurring in non-nativized loans, enclose it in curly brackets.

To mark a phoneme as marginal outside non-nativized loans, enclose it in parentheses and curly brackets.

In some cases, phonemes may be too underspecified or under-described to be easily reducible to one IPA representation, as with the Rotokas voiced series, or coronal plosives that may be either dental or alveolar. Indicate these cases by listing the candidate representations separated by vertical bars, with the canonical representation used by the source document in the first position.

### `allophonic_rules`

`allophonic_rules` stores a set of allophonic rules, written in `source > realization / environment` format.

- The source must be a phoneme listed in `phonemes`.
- The realization must be a phoneme.
- The environment is optional, and may be free-form text.

In cases where an entire cluster or sequence has a specific realization, such as English /nð/ > [n̪ː], join the source phonemes in the sequence with a plus sign: `n+ð > n̪ː`. If this rule has no conditioning factor outside the cluster itself, the `/ environment` component may be omitted.

For cases of free variation, such as Nuosu `m+ɨ >~ m̩`, use the digraph `>~`. For cases of free variation among obligatory conditioned allophones, such as `t > s ~ ts / _i` in Rotokas, use `>` and separate the variants with `~`.

# Non-IPA conventions

For fricated or 'super-close' vowels such as the 'apical vowel' of Mandarin, use the Sinological characters: `ɿ` instead of `i̝` or `z̩`, `ʮ` instead of `y̝` or `ʑ̩ʷ`, and so on. For the fricated back rounded vowel, use `ꭒ` instead of `v̩`.

The IPA palatal series is here interpreted as velar palatals; coronal palatals are represented by the Sinological `ȶ` series.

# Example

An example file, `roto1249-1.ini`, is given below.

```
[core]
name = Rotokas
glottocode = roto1249

[source]
author = Firchow, Irwin; Firchow, Jacqueline
title = An Abbreviated Phoneme Inventory
publisher = Anthropological Linguistics
volume = 11
number = 9
year = 1969
pages = 271-276
glottolog = 110896
url = https://www.jstor.org/stable/30029468

[phonemes]
p
t
k
β|b|m
ɾ|n|l|d
g|ɣ|ŋ
a
e|ɛ
o
i|ɪ
u
aː
eː|ɛː
oː
iː|ɪː
uː

[allophonic_rules]
t > ts / _i
```

# Blank file

```
[core]
name = REQUIRED
glottocode = REQUIRED
notes = OPTIONAL
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

[phonemes]
REQUIRED

[allophonic_rules]
PHONEME > IPA_REALIZATION / DESCRIPTION_OF_ENVIRONMENT
PHONEME+PHONEME > REALIZATION_OF_CLUSTER / DESCRIPTION_OF_ENVIRONMENT
```

# Scripts

## `add.py`

A script to create a blank doculect file. Usage: `>python add.py <glottocode>`. Prints the name of the created file.