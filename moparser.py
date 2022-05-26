import os
import textwrap


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

#: List of decoration symbols according to the ABC notation standard v2.1.
DECORATIONS = [
    '!trill!', '!trill(!', '!trill)!', '!lowermordent!', '!uppermordent!',
    '!mordent!', '!pralltriller!', '!roll!', '!turn!', '!turnx!',
    '!invertedturn!', '!invertedturnx!', '!arpeggio!', '!>!', '!accent!',
    '!emphasis!', '!fermata!', '!invertedfermata!', '!tenuto!', '!0!', '!1!',
    '!2!', '!3!', '!4!', '!5!', '!+!', '!plus!', '!snap!', '!slide!',
    '!wedge!', '!upbow!', '!downbow!', '!open!', '!thumb!', '!breath!',
    '!pppp!', '!ppp!', '!pp!', '!p!', '!mp!', '!mf!', '!f!', '!ff!', '!fff!',
    '!ffff!', '!sfz!', '!crescendo(!', '!<(!', '!crescendo)!', '!<)!',
    '!diminuendo(!', '!>(!', '!diminuendo)!', '!>)!', '!segno!', '!coda!',
    '!D.S.!', '!D.C.!', '!dacoda!', '!dacapo!', '!fine!', '!shortphrase!',
    '!mediumphrase!', '!longphrase!', '.', '~', 'H', 'L', 'M', 'O', 'P', 'S',
    'T', 'u', 'v'
]

class Tune:

    def __init__(self, **kwargs):
        #: tune body
        self.abc = []
        self._expanded_abc = []

        for key in HEADER_KEYS:
            setattr(self, HEADER_KEYS[key], [])

        for keyname, value in kwargs.items():
            try:
                get_id_from_field(keyname)
            except KeyError:
                if keyname not in ['abc']:
                    continue
            setattr(self, keyname, value)

def expand_repeats(abc):
    """

    :param str abc: abc to expand repeats
    :return: expanded abc str
    """
    parsed = abc
    start = 0
    end = 0

    parsed = parsed.replace('::',':||:')

    while True:
        end = parsed.find(':|', start)
        if (end == -1):
            break

        new_start = parsed.find('|:', 0, end)
        if (new_start != -1):
            start = new_start + 2



def strip_everything_we_dont_want(abc):




