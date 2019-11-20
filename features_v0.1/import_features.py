from inflection import underscore
from collections import OrderedDict
import csv, psycopg2

def init_db():
    conn_string = "dbname=indexphonemica user=postgres password=postgres"
    conn = psycopg2.connect(conn_string)
    sql = conn.cursor()
    return (conn, sql)

conn, sql = init_db()

# Harmonize with Pshrimp now; rectify names in both later.
SEGMENT_COL = 'phoneme'

def get_id(table, field, value, sql = sql):
    '''Get (assumed to be unique) id of the thing in `table` where `field` = `value`. Returns False if it's not there.'''
    # NB: Passing table/column names as parameters doesn't work. This does not appear to be documented.
    sql.execute('SELECT id FROM {} WHERE {} = %s'.format(table, field), (value,))
    res = sql.fetchone()
    return res[0] if res else None

def update(table, props, column, value, sql = sql):
    '''Insert OrderedDict `props` ({col_name: prop}) into `table`.'''
    s = "UPDATE segments SET {} WHERE {SEGMENT_COL} = %s".format(
        ','.join(
            ["{} = %s".format(k, props[k]) for k in props.keys()]
        ), SEGMENT_COL=SEGMENT_COL
    )
    sql.execute(s, (*props.values(), value,))

def dfilter(d, keys):
    '''Return a new OrderedDict consisting of only the key/value pairs in dict d with keys listed in the `keys` set.
    Also munge them so they fit nicely in the DB.'''
    return OrderedDict((munge_key(k), munge_value(v)) for k, v in d.items() if munge_key(k) in keys)

def dupdate(table, d, keys, column, value, sql = sql):
    '''dfilter, then insert'''
    update(table, dfilter(d, keys), column, value, sql = sql)

def munge_key(k):
    key_replacements = {
        'raisedLarynxEjective': 'ejective',
        'loweredLarynxImplosive': 'implosive',
        'lateral': 'lateralis'
    }
    if k in key_replacements:
        return key_replacements[k]
    return underscore(k)

def munge_value(v):
    value_replacements = {
        '0': None,      # for segment features
        'NA': None,     # for marginal, allophones, etc.
        'None': None,   
        'FALSE': False, # for marginal
        'TRUE': True    # for marginal
    }
    if v in value_replacements:
        return value_replacements[v]
    return v

LANGUAGE_FILTER = set([
    'inventory_id', 
    'source', 
    'glottocode', 
    'iso6393', 
    'language_name', 
    'specific_dialect'
])

SEGMENT_FILTER = set([
#   'glyph_id',
    'segment_class',
    'tone',
    'stress',
    'syllabic',
    'short',
    'long',
    'consonantal',
    'sonorant',
    'continuant',
    'delayed_release',
    'approximant',
    'tap',
    'trill',
    'nasal',
    'lateralis',
    'labial',
    'round',
    'labiodental',
    'coronal',
    'anterior',
    'distributed',
    'strident',
    'dorsal',
    'high',
    'low',
    'front',
    'back',
    'tense',
    'retracted_tongue_root',
    'advanced_tongue_root',
    'periodic_glottal_source',
    'epilaryngeal_source',
    'spread_glottis',
    'constricted_glottis',
    'fortis',
    'ejective',
    'implosive',
    'click'
])

if __name__ == '__main__':
    # Import segments
    with open('segments_v02.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        i = 0
        finished_segments = set()
        for row in reader:
            i += 1
            if (i % 1000 == 0):
                print('Importing segments\tRead {} lines'.format(i))

            phoneme = row['Phoneme']
            if not get_id('segments', SEGMENT_COL, phoneme): # it's not in IPHON (yet) so we don't care about it
                finished_segments.add(phoneme)
            if row['Phoneme'] in finished_segments:
                continue
            dupdate('segments', row, SEGMENT_FILTER, SEGMENT_COL, phoneme)
            finished_segments.add(phoneme)
    conn.commit()
    conn.close()