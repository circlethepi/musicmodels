import sjkabc
import parser

abc_string = """X: 1
T:A and A's Waltz
% Nottingham Music Database
S:Mick Peat
M:3/4
L:1/4
K:G
e|"G"d2B|"D"A3/2B/2c|"G"B2G|"D"A2e|"G"d2B|"D"A3/2B/2c|[M:2/4]"F"B=F|[M:3/4]"G"G2e:|"C"g2e|"Bb"=f2d|"F"c2A|=F2e|"C"g2e|"Bb"=f2d|[M:2/4]"F"cA|[M:3/4] [1 "G"G2e:| [2"G"G2z||"""

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
A2|:"D"a3/2b/2a3/2g/2 f2(3def|"Em"g3/2a/2g3/2f/2 "A"e2A2|"D"f3/2g/2f3/2e/2 d2f2\|"Em"B3/2c/2d3/2e/2 "A"c2A2|"D"a3/2b/2a3/2g/2 f2(3def|"Em"g3/2a/2g3/2f/2 "A"e2A2|\"D"f3/2g/2f3/2e/2 d3/2e/2f3/2A/2|"G"B3/2d/2"A"d3/2c/2 "D"d2A2:||:"G"B3/2A/2B3/2g/2 "D"d2A2|"Em"e3/2d/2e3/2f/2 "A"e2a2|\"G"b3/2a/2(3gab "D"a3/2g/2(3fga|"E"f3/2e/2(3def "A"e2A2|"G"B3/2A/2B3/2g/2 "D"d2A2|"Em"e3/2d/2e3/2f/2 "A"e2a2|\"G"b3/2a/2g3/2f/2 "A"a3/2g/2f3/2e/2|1"D"d2f2 d2A2:|[2 d2f2d2|"""
#edBABcBGAedBABc


def strip_everything_we_dont_want(abc):
    """

    :param abc:
    :return:
    """

    for rid in '''hijklmnopqrstuvwxyzHIJKLMNOPQRSTUVWXYZ1234567890:/\ '{}[],()''':
        abc = abc.replace(rid, "")
    return abc


def parse_tunes(abc):
    """
    
    :param abc: 
    :return: 
    """
    for tune in sjkabc.Parser(abc) :
        title = tune.title[0]
        print('stripped music of ', title)

        music = tune.abc[0]
        music = sjkabc.expand_parts(music)
        music = strip_everything_we_dont_want(music)
        music = sjkabc.strip_chords(music) #strip chords

        print(music)


parse_tunes(testing)





