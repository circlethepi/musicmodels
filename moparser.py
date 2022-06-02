import os

"""
This program makes use of Svante Kvarnstrom's abc parser code to extract basic information from abc notation files. 

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
K:D
A2|:"D"a3/2b/2a3/2g/2 f2(3def|"Em"g3/2a/2g3/2f/2 "A"e2A2|"D"f3/2g/2f3/2e/2 d2f2\|"Em"B3/2c/2d3/2e/2 "A"c2A2|"D"a3/2b/2a3/2g/2 f2(3def|"Em"g3/2a/2g3/2f/2 "A"e2A2|\"D"f3/2g/2f3/2e/2 d3/2e/2f3/2A/2|"G"B3/2d/2"A"d3/2c/2 "D"d2A2:||:"G"B3/2A/2B3/2g/2 "D"d2A2|"Em"e3/2d/2e3/2f/2 "A"e2a2|\"G"b3/2a/2(3gab "D"a3/2g/2(3fga|"E"f3/2e/2(3def "A"e2A2|"G"B3/2A/2B3/2g/2 "D"d2A2|"Em"e3/2d/2e3/2f/2 "A"e2a2|\"G"b3/2a/2g3/2f/2 "A"a3/2g/2f3/2e/2|1"D"d2f2 d2A2:|[2 d2f2d2|

X: 29
T:Paddy in Flow
% Nottingham Music Database
S:Mick Peat
P:/f2AABA last time through/fP
M:6/8
K:D
A|:"D"DED FAB|=cBA -AdA|"D"DED FAB|"C"=cAG -G2A|"D"DED FAB|
=cBA Ade|fgf ed=c|1"A"Adc "D"dAF:|2"A"Adc "D"def|
K:A
|:"A"=gfe -efe|eag aec|Ace =gfe-|"E"eag bge|
"A"=gfe -efe|eag aec|Ace =gfe|[1"E"eag "A"aef:|[2"E"eag "A"a3|

X: 21
T:The Frantocini
% Nottingham Music Database
S:Mick Peat
M:6/8
K:F
"F"fcc ~c3|"Dm"dAA ~A3|"Gm"GBA GAF|"C"EFG C3|"F"fcc c3|"Dm"dAA A2f|"C"edc "G"GA=B|"C"c3 c3:|
"C"gcc ~c3|"F"acc ~c3|"Bb"dcB "Gm"AGF|"C"EFG C3|"F"fcc c3|"Dm"dAA ~A3|"Gm"GBA "C"GFE|"F"F3 F3:|

"""


### PARSING TUNE

def parse_tunes(abc):
    """
    converts tune into format that is useful (list of numbers corresponding to chromatic distance from keycenter)
    26may22: strips to string of letters and accidentals
    :param abc:
    :return:
    """
    counter = 0
    for song in Parser(abc) :
        #title = song.title
        key = song.key
        mapping = key.keymap
        #print('stripped music of ', title)


        stripped_music = song._expanded
        mapped_music = song._mapped
        pcr = song._pitch_class_representation
        trans = song._transposed

        #music = sjkabc.strip_chords(strip_everything_we_dont_want(sjkabc.expand_parts(tune.abc[0]))).upper()
        print("\nanalysis for song ", counter)
        print("music: ", stripped_music)
        print("song key: ", key.key_raw)
        print("kay note map: ", mapping)
        print("mapped music: ", mapped_music)
        print("translated: ", pcr)
        print('transposed: ', trans)
        counter += 1

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

        for at in HEADER_KEYS:
            setattr(self, HEADER_KEYS[at], [])

        for keyname, value in kwargs.items() :
            try:
                get_id_from_field(keyname)
            except KeyError:
                if keyname not in ['abc']:
                    continue
            setattr(self, keyname, value)


        self.key = song_key(self.key)



    @property
    def _expanded(self):  #the format we want to analyze
        if not self.expanded:
            self.expanded = expand_music(''.join(self.music))
        return self.expanded

    @property
    def _mapped(self): #map mapping to note
        mapping = self.key.keymap
        convert = self._expanded

        converted = []
        accidental = False

        for note in convert:
            if (note == '=' or note == '_' or note == '^'): #if note char is an accidental
                accidental = True
                converted.append(note)
            elif (note in 'ABCDEFG' and accidental): #if note char is preceeded by an accidental
                accidental = False
                converted.append(note)
            else: #if just a note
                converted.append(mapping[note])

        return ''.join(converted)

    @property
    def _pitch_class_representation(self): #mapping to pitch class values
        mapped = self._mapped
        return pitch_class_representation(mapped)



    @property
    def _transposed(self):
        key_center_pcr = (pitch_class_representation(self.key.keycenter))[0]
        pcr = self._pitch_class_representation

        #return key_center_pcr
        trans = []
        for note in pcr:
            add = (note - key_center_pcr) % 12
            trans.append(add)

        return trans






class song_key:
    def __init__(self, keyinfo):
        self.key_raw = keyinfo

    @property
    def keymode(key):  # MO may 22
        """
        finds and returns the keymode that we are working with
        :param key: string of key def from abc header
        :return: scale type (one of the seven modes)
        """

        if "DOR" in key.key_raw.upper():
            return "dorian"
        elif "PHR" in key.key_raw.upper():
            return "phrygian"
        elif "LYD" in key.key_raw.upper():
            return "lydian"
        elif "MIX" in key.key_raw.upper():
            return "mixolydian"
        elif "LOC" in key.key_raw.upper():
            return "locrian"
        elif "M" in key.key_raw.upper():
            return "minor"
        else:
            return "major"

    @property
    def keycenter(key):  # MO May 22
        """
        finds the key center
        :param key: string of key from abc header
        :return: key center string
        """

        ret = ['x','x']
        if 1 < len(key.key_raw):
            if key.key_raw[1] != ('b' or '#'):
                ret[0] = '='
                ret[1] = key.key_raw[0]
            else:
                for c in key.key_raw[0:2]:
                    if c in 'ABCDEFG':
                        ret[1] = c
                    elif c == 'b':
                        ret[0] = '_'
                    elif c == '#':
                        ret[0] = '^'
        else:
            ret[0] = '='
            ret[1] = key.key_raw[0]
        return ''.join(ret)

    @property
    def relative_major(key):
        transp_from_maj = mode_transposition[key.keymode]

        pitchval = pitch_values[key.keycenter[1].upper()]
        accval = 0
        if 1 < len(key.keycenter):
            accval = accidental_values[key.keycenter[0]]
        relmaj = (pitchval + accval + transp_from_maj) % 12
        return relmaj

    @property
    def keymap(key):  # MO may 22
        """
        this mapping ignores modified keys as the corpus does not contain any tunes with modified keys.

        :param key: key definition ex: Gm, Gmixolidian, Bb
        :return: keymapping to translate letters into absolute pitches from map
        """
        # set default keymap
        keymap = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G'}

        rel_major = key.relative_major  # set relative major number
        rel_major_name = chromatic_notes[rel_major]  # get relative major notename
        accidentals = number_accidentals[rel_major_name]  # get number of accidentals in relative major
        # print(rel_major_name, "\n", accidentals) #sanity check

        # if sharp key
        if accidentals > 0:
            for i in range(accidentals):
                keymap[sharp_order[i]] = "^" + keymap[sharp_order[i]]
        else:
            for i in range(-accidentals):
                keymap[flat_order[i]] = "_" + keymap[flat_order[i]]

        return keymap

#
#
#
#
def pitch_class_representation(notes): #mapping to pitch class values
     pcr = []
     accidental = False
     value = 0
     for note in notes:
        if (note == '=' or note == '_' or note == '^'):
           accidental = True
           value += accidental_values[note]
        elif note in 'ABCDEFG' and accidental:
           accidental = False
           value += pitch_values[note]
           pcr.append(value)
           value = 0
        else:
           value += pitch_values[note]
           pcr.append(value)
           value = 0

     return pcr



#
#
#
#

class Parser:

    """
    This class provides iterable parsing capabilities.

    `Parser` must be initialised with a string containing ABC music
    notation. This class is iterable and will return a `Tune` object
    for every tune found in the provided ABC notation.

    Example::

        #>>> for tune in Parser(abc):
        ...     print('Parsed ', tune.title)

    .. seealso:: :class:`Tune`
    """

    def __init__(self, abc=None):
        """Initialise Parser

        :param abc: string containing ABC to parse

        """
        self.tunes = []
        self.last_field = None

        if abc:
            self.parse(abc)
        self.index = len(self.tunes)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.tunes[self.index]

    def parse(self, abc):
        """Parse ABC notation.

        This function will append found ABC tunes to `self.tunes`.

        :param abc: string containing abc to parse

        """
        in_header = False
        current_tune = None

        for line in abc.splitlines():
            if self._line_empty(line) or self._line_comment(line):
                continue

            # At beginning of header
            if self._line_is_index(line):
                if current_tune:
                    # We have a parsed tune already, append it to list of
                    # tunes.
                    self.tunes.append(current_tune)

                in_header = True
                current_tune = single_song()  #changed class to be the one we like mo 0522

            if in_header:
                (key, val) = line.split(':', 1)
                #if key in HEADER_KEYS:
                    #getattr(current_tune, HEADER_KEYS[key]).append(val.strip())
                    #self.last_field = HEADER_KEYS[key]
                if key == 'K':
                    setattr(current_tune, "key", song_key(val))

                # Continuation of info field.
                if key == '+' and self.last_field:
                    field = getattr(current_tune, self.last_field)
                    field[-1] = field[-1] + ' ' + val.strip()

                # Header ends at K:
                if self._line_is_key(line):
                    in_header = False

            else:
                if current_tune:
                    current_tune.music.append(line)

        else:
            if current_tune:
                self.tunes.append(current_tune)

    def _line_is_key(self, line):
        """Check if line is a K: line

        :param str line: line to check
        :returns: True if line is a key line and False if not.
        :rtype: bool

        """
        if line.startswith('K:'):
            return True
        else:
            return False

    def _line_empty(self, line):
        """Check if line is empty

        :param str line: line to check
        :returns: True if line is empty and False if not.
        :rtype: bool

        """
        line = line.strip()
        if line == '':
            return True
        else:
            return False

    def _line_comment(self, line):
        """Check if line is a comment

        :param str line: line to check
        :returns: True if line is a comment and False if not.
        :rtype: bool

        """
        line = line.strip()
        if line.startswith('%'):
            return True
        else:
            return False

    def _line_is_index(self, line):
        """Check if line is an index line (X:).

        If it is, it is considered to be the start of a tune.

        :param str line: line to check
        :returns: True if line is a index line, False if not.
        :rtype: bool

        """
        if line.startswith('X:'):
            return True
        else:
            return False

    def _line_is_continued_line(self, line):
        """Check if line is a continuation of the last

        :param str line: Line to check
        :returns: true if the line is a continuation line

        """
        if line.startswith('+:'):
            return True
        else:
            return False

#
#  EXPANDING THE MUSIC
#   MO May 22
#

def expand_music(music):
    for f in [expand_repeats, strip_ties, strip_everything_we_dont_want, strip_chords]:
        music = f(music)
    return music.upper()

def expand_repeats(abc):
    """
    Expand repeats with support for (two) alternate endings.

    Example::

      #  >>> print(expand_parts('aaa|bbb|1ccc:|2ddd|]'))
        aaa|bbb|ccc|aaa|bbb|ddd|

    :param str abc: abc to expand
    :returns: expanded abc
    :rtype: str

    """
    parsed_abc = abc
    start = 0
    end = 0

    parsed_abc = parsed_abc.replace('::', ':||:')

    while True:
        end = parsed_abc.find(':|', start)
        if (end == -1):
            break

        new_start = parsed_abc.rfind('|:', 0, end)
        if (new_start != -1):
            start = new_start+2

        tmp = []
        if end + 2 < len(parsed_abc) and parsed_abc[end+2].isdigit():
            first_ending_start = parsed_abc.rfind('|', 0, end)
            num_bars = 1
            if not parsed_abc[first_ending_start+1].isdigit():
                first_ending_start = parsed_abc.rfind('|', 0,
                                                      first_ending_start)
                num_bars = 2

            tmp.append(parsed_abc[start:first_ending_start])
            tmp.append('|')
            tmp.append(parsed_abc[first_ending_start+2:end])
            tmp.append('|')

            second_ending_start = end+2
            second_ending_end = None
            for i in range(num_bars):
                second_ending_end = parsed_abc.find('|', second_ending_start)

            tmp.append(parsed_abc[start:first_ending_start])
            tmp.append('|')
            tmp.append(parsed_abc[second_ending_start+1:second_ending_end])
            parsed_abc = parsed_abc.replace(
                parsed_abc[start:second_ending_end],
                ''.join(tmp), 1)
            start += len(tmp)
        else:
            tmp.append(parsed_abc[start:end])
            tmp.append('|')
            tmp.append(parsed_abc[start:end])
            tmp.append('|')
            parsed_abc = parsed_abc.replace(parsed_abc[start:end+2],
                                            ''.join(tmp), 1)
            start += len(tmp)

    for rep in ['|:', ':', ']']:
        parsed_abc = parsed_abc.replace(rep, '')
    parsed_abc = parsed_abc.replace('||', '|')

    return parsed_abc

def strip_everything_we_dont_want(music):
    """
    strips everything that we don't want from abc notation string: ornaments, rhythm, other markings, etc
    :param music: string
    :return: abc tune without any ornaments, rhythm, or other markings - only notes (and chords)
    """

    for rid in '''hijklmnopqrstuvwxyzHIJKLMNOPQRSTUVWXYZ1234567890:/\ '{}[],()|~''':
        music = music.replace(rid, "")
    return music

def strip_chords(abc):  ##directly from sjkabc
    """Strip chords and 'guitar chords' from string.

    Example::

        >>> from sjkabc import strip_chords
        >>> stripped = strip_chords('"G" abc|"Em" bcd|[GBd] cde')
        >>> stripped
        ' abc| bcd | cde'

    :param str abc: abc to filter
    :returns: abc with chords stripped
    :rtype: str

    """
    ret = []
    in_chord = False

    for c in abc:
        if c == '[' or (c == '"' and not in_chord):
            in_chord = True
        elif c == ']' or (c == '"' and in_chord):
            in_chord = False
        elif in_chord:
            continue
        else:
            ret.append(c)

    return ''.join(ret)

def strip_ties(abc):
    ret = []
    tied = False

    for c in abc:
        if c == '-':
            tied = True
        elif c in 'ABCDEFGabcdefg' and tied:
            tied = False
        elif tied:
            continue
        else:
            ret.append(c)

    return ''.join(ret)




#order of accidentals added
flat_order = ['B', 'E', 'A', 'D', 'G', 'C', 'F']
sharp_order = ['F', 'C', 'G', 'D', 'A', 'E', 'B']
#transposition from relative major in half steps for each mode
mode_transposition = {'major': 0, 'minor': 3, 'mixolydian': -7, 'dorian': -2, 'phrygian': -4, 'lydian': -5, 'locrian': 1}


#number of sharps or flats for each major key center
number_accidentals = {'C#': 7, 'F#': 6, 'B': 5, 'E': 4, 'A': 3, 'D': 2, 'G': 1, 'C': 0, 'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7}

#note transpositions
pitch_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
accidental_values = {'=': 0, '^': 1, '_': -1}
chromatic_notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']







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


def wrap_line(string, id, max_length=78, prefix='+'):
    """
    Wrap header line.

    :param str string: string to wrap
    :param str id: character id of header line
    :param int max_length: maximum line length
    :param str prefix: Line prefix for wrapped lines (first line exempted)
    :returns: wrapped line
    :rtype: str

    .. seealso:: :func:`get_id_from_field`
    """
    w = textwrap.TextWrapper()
    w.initial_indent = '{}:'.format(id)
    w.subsequent_indent = '{}:'.format(prefix)
    w.width = max_length
    return '\n'.join(w.wrap(string))


#
#
#
#

def parse_file(filename):
    """

    :param filename:
    :return:
    """

    with open(filename, 'r') as f:
        content = f.read()

    for song in Parser(content):
        yield song

def parse_directory(directory):
    """

    :param directory:
    :return:
    """

    for dirpath, dirnames, filenames in os.walk(directory) :
        for filename in [f for f in filenames if (f.endswith('.abc') or f.endswith('.txt'))] :
            for song in parse_file(os.path.join(dirpath, filename)):
                yield song


## running the program

with open("D:/Programming Projects/musicmodels/music/ashover.txt", "r") as f:
   content = f.read()

parse_tunes(content)
