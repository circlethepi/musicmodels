import sjkabcfunc as sjk
import key_length as kl
import note
from fractions import Fraction as frac

def expand_music(music):
    for f in [sjk.expand_repeats, sjk.strip_chords, sjk.strip_extra_chars]:
        music = f(music)
    return music.upper()

def pitch_class_representation(notes):  # mapping to pitch class values
    """
    :param notes: notes given in abc notation as (^_=)(ABCDEFG) string
    :return: list of integers; pitch class representation of note(s) - integer in base 12 
    """
    pcr = []
    accidental = False
    value = 0
    for note in notes:
        if (note == '=' or note == '_' or note == '^'):
            accidental = True
            value += kl.accidental_values[note]
        elif note in 'ABCDEFG' and accidental:
            accidental = False
            value += kl.pitch_values[note]
            pcr.append(value)
            value = 0
        else:
            value += kl.pitch_values[note]
            pcr.append(value)
            value = 0

    return pcr


##essentially a tune object from sjkabc
class pre_song:  #song object that has properties as defined by the header lines in abc content
    def __init__(self, **kwargs):
        """Initialise Tune"""
        #: Tune body.
        self.abc = []
        self._expanded_abc = []

        for key in sjk.HEADER_KEYS:
            setattr(self, sjk.HEADER_KEYS[key], [])

        for keyname, value in kwargs.items():
            try:
                sjk.get_id_from_field(keyname)
            except KeyError:
                if keyname not in ['abc']:
                    continue
            setattr(self, keyname, value)



class post_song:  #processed song that has the information that we want
    def __init__(self, pre_song):
        self.pre = pre_song
        self.music = expand_music(' '.join(pre_song.abc))

    @property
    def given_key(self):
        k = self.pre.key[0]
        key = kl.song_key(k)
        return key

    @property
    def default_note_length(self):
        len = self.pre.note_length
        met = self.pre.metre[0]
        length = kl.song_div(len, met).default_length
        return length

    @property
    def default_keymap(self):
        return self.given_key.keymap

    def do_mapping(self):
        music = self.music

        key = self.given_key                    #song_key object
        keychange = False

        to_ksm = []
        out = []
        newkey = []

        for char in music:
            if char == 'K':
                keychange = True
            elif not keychange:
                to_ksm.append(char)
            elif keychange:
                out.append(key_signature_mapping(''.join(to_ksm), key.keymap)) #keymap in the first key

                to_ksm = [] #reset the container

                if char in 'ABCDEFG' or char == '#':
                    newkey.append(char) #start finding new key
                elif char == ' ':

                    new = ''.join(newkey)
                    key = kl.song_key(new)
                    newkey = []
                    keychange = False

        if to_ksm != []:
            out.append(key_signature_mapping(''.join(to_ksm), key.keymap))

        return ''.join(out)


    def extract_notes(self):
        music = self.do_mapping()
        default_len = self.default_note_length

        # set lists of pitches and durations
        pitches = []
        durations = []
        # list of notes to extract
        notes = []

        current_pitch = []
        current_duration = []

        finding_pitch = True

        for char in music:
            if char in 'ABCDEFG' and finding_pitch:  # if a note character
                current_pitch.append(char)  # add to current pitch
                finding_pitch = False

            elif char in '_^=' and finding_pitch:
                current_pitch.append(char)
                finding_pitch = True

            elif not finding_pitch:  # we are now getting the duration
                if char in '1234567890/':  # if a duration
                    current_duration.append(char)  # add to our duration list

                elif char not in '1234567890/':  # if no longer a duration character

                    # set duration
                    if current_duration == []:
                        dur = default_len
                    else:
                        dur = frac(''.join(current_duration))  # this is our duration

                    # set pitch
                    pit = pitch_class_representation(''.join(current_pitch))[0]  # getting integer value of pitch

                    # add to our lists
                    pitches.append(pit)
                    durations.append(dur)
                    notes.append(note.note(pit, dur))

                    # reset note containers
                    current_pitch = []
                    current_duration = []

                    finding_pitch = True  # now finding pitches
        setattr(self, 'pitches', pitches)
        setattr(self, 'durations', durations)
        setattr(self, 'notelist', notes)

        return


### key mapping
def key_signature_mapping(music, keymap):
    converted = []
    accidental = False

    for note in music:
        if (note == '=' or note == '_' or note == '^'):  # if note char is an accidental
            accidental = True
            converted.append(note)
        elif (note in 'ABCDEFG' and accidental):  # if note char is preceeded by an accidental
            accidental = False
            converted.append(note)
        elif note in 'ABCDEFG':  # if just a note
            converted.append(keymap[note])
        elif note in ' 1234567890/\ ':
            converted.append(note)

    return ''.join(converted)


### parsing notes