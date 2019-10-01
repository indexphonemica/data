# Index Phonemica

## Data format

Doculect entries are stored as Python INI files, named with the Glottocode of the language followed by a hyphen and an index number: `1` for the first entry for that Glottocode, `2` for the second, etc. 

Entry files have five headers: `core`, `source`, (optionally) `notes`, `phonemes`, and `allophonic_rules`. An optional `todo` section is also permitted.

### `core`

`core` stores two required attributes:
- `name`: the name of the doculect as given in the source
- `glottocode`: the Glottocode of the language

And two optional attributes:
- `dialect`: the Glottocode of the specific dialect, if one is defined
- `dialect_name`: the name of the specific dialect as given in the source, if a specific dialect is referenced

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

`notes` stores notes relevant to the doculect entry.

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

## Consonants

The frication diacritic is carried over from PHOIBLE: for example, the voiced velar lateral fricative is `ʟ͓`.

The retroflex lateral flap is written `ɺ̢`.

The IPA palatal series is here interpreted as velar palatals; coronal palatals are represented by the Sinological `ȶ` series.

Affricates and consonants with bilabially trilled release are assumed to agree in voice unless otherwise specified.

## Vowels 

Fricated or 'super-close' vowels such as Mandarin -i are written with extensions of the Sinological characters: 
- `ɿ` instead of `z̩`
- `ɿᶾ` instead of `ʒ̩`
- `ʅ` instead of `ʐ̩`
- `ɿᶽ` instead of `ʑ̩`
- `ꭒ` instead of `v̩`

There may eventually be a `ʮ` series also, but we haven't needed one yet.

The retraction diacritic on vowels is used in the Tibeto-Burman manner, to represent the 'tight throat' quality or 'tense voice' that appears in Liangshan Yi and Bai.

`ʵ` replaces `˞` as a marker of rhoticity.

## Tones

Tone is written with Chao tone letters. The super-high _66_ tone of Bai is written ˥́.

# Other conventions

## Sino-Tibetan
Inventories of 'eroded' Sino-Tibetan languages are typically given as onsets, rimes, and tones. We convert these to inventories of consonants and vowels, and err on the side of segmental simplicity, although complex rimes may be represented as unit segments in certain cases where we can identify good reason to do so.

## Non-syllabicity
The non-syllabicity diacritic is used on diphthongs when:

- it is used in the source
- every diphthong given in the source is closing, with the possible exception of close-to-close diphthongs (since in these cases, it's likely that all diphthongs are falling in prominence)

If diphthongs that are not closing or close-to-close are present and the source does not use the non-syllabicity diacritic, it is not used.

For example, if a source lists a diphthong inventory of /ai au ei eu oi ou iu/, these diphthongs will be input as /ai̯ au̯ ei̯ eu̯ oi̯ ou̯ iu̯/. But if a source lists /ai au ea oa/, these will be input as /ai au ea oa/, since it isn't clear whether /ea oa/ are falling or rising in prominence. 

## SIL OPDs 
SIL Organized Phonology Data sheets almost always list the low vowel as /ɑ/ rather than /a/. In these cases, /a/ will be input unless the low vowel is clearly described to be backed.

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