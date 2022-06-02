import sjkabc

"""
This program makes use of Svante Kvarnstrom's abc parser to extract basic information from abc notation files. 

"""

testing = """X: 1
T:A and A's Waltz
% Nottingham Music Database
S:Mick Peat
M:3/4
L:1/4
K:G
e|"G"d2B|"D"A3/2B/2c|"G"B2G|"D"A2e|"G"d2B|"D"A3/2B/2c|[M:2/4]"F"B=F|[M:3/4]"G"G2e:: "C"g2e|"Bb"=f2d|"F"c2A|=F2e|"C"g2e|"Bb"=f2d|[M:2/4]"F"cA|[M:3/4] [1 "G"G2e:| [2"G"G2z||


X: 2
T:Barry's Favourite
% Nottingham Music Database
S:Mick Peat
M:2/2
K:Bb
A2|:"D"a3/2b/2a3/2g/2 f2(3def|"Em"g3/2a/2g3/2f/2 "A"e2A2|"D"f3/2g/2f3/2e/2 d2f2\|"Em"B3/2c/2d3/2e/2 "A"c2A2|"D"a3/2b/2a3/2g/2 f2(3def|"Em"g3/2a/2g3/2f/2 "A"e2A2|\"D"f3/2g/2f3/2e/2 d3/2e/2f3/2A/2|"G"B3/2d/2"A"d3/2c/2 "D"d2A2:||:"G"B3/2A/2B3/2g/2 "D"d2A2|"Em"e3/2d/2e3/2f/2 "A"e2a2|\"G"b3/2a/2(3gab "D"a3/2g/2(3fga|"E"f3/2e/2(3def "A"e2A2|"G"B3/2A/2B3/2g/2 "D"d2A2|"Em"e3/2d/2e3/2f/2 "A"e2a2|\"G"b3/2a/2g3/2f/2 "A"a3/2g/2f3/2e/2|1"D"d2f2 d2A2:|[2 d2f2d2|



"""


### PARSING TUNE

def parse_tunes(abc):
    """
    converts tune into format that is useful (list of numbers corresponding to chromatic distance from keycenter)
    26may22: strips to string of letters and accidentals
    :param abc:
    :return:
    """
    for tune in sjkabc.Parser(abc) :
        title = tune.title[0]
        key = tune.key[0]
        print('stripped music of ', title)

        music = tune.abc[0]
        music = sjkabc.expand_parts(music) #expand repeats with up to 2 different endings
        music = strip_everything_we_dont_want(music) #get rid of other characters
        music = sjkabc.strip_chords(music) #strip chords
        stripped_music = music.upper()

        #music = sjkabc.strip_chords(strip_everything_we_dont_want(sjkabc.expand_parts(tune.abc[0]))).upper()

        print(stripped_music)
        print(key)
        keymap = create_keymap(key)
        print(keymap)



#
#
#
#
#
#

HEADER_KEYS = dict(
    B='book',
    C='composer',
    D='discography',
    F='file',
    G='group',
    H='history',
    I='instruction',
    K='key',
    L='note_length',
    M='metre',
    N='notes',
    O='origin',
    P='parts',
    Q='tempo',
    R='rhythm',
    S='source',
    T='title',
    X='index',
    Z='transcription'
)

class single_song : #based on SJKABC basically jury-rigged to do what we want

    def __init__(self, **kwargs) :
        self.music = []
        self.expanded = []

        for key in HEADER_KEYS:
            setattr(self, HEADER_KEYS[key], [])
        for keyname, value in kwargs.items() :
            try:
                get_id_from_field(keyname)
            except KeyError:
                if keyname not in ['abc']:
                    continue
            setattr(self, keyname, value)

    @property
    def _expanded(self):

        if not self.expanded:
            self.expanded = expand_abc(''.join(self.music))
        return self.expanded

#things that go into parse_tunes
def strip_everything_we_dont_want(abc):
    """
    strips everything that we don't want from abc notation string: ornaments, rhythm, other markings, etc
    :param abc:
    :return: abc tune without any ornaments, rhythm, or other markings - only notes
    """

    for rid in '''hijklmnopqrstuvwxyzHIJKLMNOPQRSTUVWXYZ1234567890:/\ '{}[],()|''':
        abc = abc.replace(rid, "")
    return abc




def find_keymode(key) :
    """
    finds and returns the keymode that we are working with
    :param key: string of key def from abc header
    :return: scale type (one of the seven modes)
    """

    if "DOR" in key.upper():
        return "dorian"
    elif "PHR" in key.upper():
        return "phrygian"
    elif "LYD" in key.upper():
        return "lydian"
    elif "MIX" in key.upper():
        return "mixolydian"
    elif "LOC" in key.upper():
        return "locrian"
    elif "M" in key.upper():
        return "minor"
    else:
        return "major"


def find_keycenter(key) :
    """
    finds the key center
    :param key: string of key from abc header
    :return: key center string
    """
    if 1 < len(key) :
        if key[1] != ('b' or '#'):
            return key[0]
        else:
            return key[0:2]
    else:
        return key[0]


flat_order = ['B', 'E', 'A', 'D', 'G', 'C', 'F']
sharp_order = ['F', 'C', 'G', 'D', 'A', 'E', 'B']

mode_transposition = {'major': 0, 'minor': 3, 'mixolydian': -7, 'dorian': -2, 'phrygian': -4, 'lydian': -5, 'locrian': 1}


#number of sharps or flats for each major key center
number_accidentals = {'C#': 7, 'F#': 6, 'B': 5, 'E': 4, 'A': 3, 'D': 2, 'G': 1, 'C': 0, 'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7}

#note transpositions
pitch_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
accidental_values = {'': 0, '#': 1, 'b': -1}
chromatic_notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']


def find_relative_major(keycenter, keymode):
    transp_from_maj = mode_transposition[keymode]

    pitchval = pitch_values[keycenter[0].upper()]
    accval = 0
    if 1 < len(keycenter):
        accval = accidental_values[keycenter[1]]
    relmaj = (pitchval + accval + transp_from_maj) % 12
    return relmaj

def create_keymap(key):
    """
    this mapping ignores modified keys as the corpus does not contain any tunes with modified keys.

    :param stripped_music: stripped music string (letters and accidentals only)
    :param key: key definition ex: Gm, Gmixolidian, Bb
    :return: keymapping to translate letters into absolute pitches from map
    """
    #set default keymap
    keymap = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G'}

    rel_major = find_relative_major(find_keycenter(key), find_keymode(key)) #get relative major number
    rel_major_name = chromatic_notes[rel_major] #get relative major notename
    accidentals = number_accidentals[rel_major_name] #get number of accidentals

    #print(rel_major_name, "\n", accidentals) #sanity check

    #if sharp key
    if accidentals > 0:
        for i in range(accidentals):
            keymap[sharp_order[i]] = "^" + keymap[sharp_order[i]]
    else:
        for i in range(-accidentals):
            keymap[flat_order[i]] = "_" + keymap[flat_order[i]]

    return keymap


##functions from SJKABC
def get_id_from_field(field):
    """Get id char from field name

    :param str field: 'long' name of field, for example 'title'
    :returns: id character, for example 'T'
    :rtype: str
    :raises KeyError: if key does not exist.

    """
    for key in HEADER_KEYS:
        if HEADER_KEYS[key] == field:
            return key
    else:
        raise KeyError('No such header key: {}'.format(field))


def get_field_from_id(id):
    """Get long field name from id char.

    :param str id: id char, for example 'T'
    :returns: long field name, like 'title'
    :rtype: str
    :raises KeyError: if key does not exist.

    """
    try:
        return HEADER_KEYS[id]
    except KeyError:
        raise KeyError('No such header key: {}'.format(id))






## running the program
parse_tunes(testing)
