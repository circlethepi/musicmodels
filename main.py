import parser as p

with open('music/test.txt') as f:
    lines = f.readlines()
    f.close()

test_song = p.Tune(lines)

test_song.parse_header

test_song.parse_abc