import moparser as mp
import sjkabcfunc as sjk
import key_length as kl
import processer as ps
import note

with open("D:/Programming Projects/musicmodels/music/test.abc", "r") as f:
   content = f.read()

#mp.parse_tunes(content)




for tune in sjk.Parser(content):
   new = ps.post_song(tune)
   new.extract_notes()
   print(tune.title, tune.key, tune.note_length, "\nMusic: ", new.music)
   print("default note length: ", new.default_note_length)
   print("default key: ", new.given_key.key_raw)
   print("default keymap: ", new.default_keymap)
   print(new.do_mapping())
   print(new.pitches)
   print(new.durations)
   print(new.notes)
   print('\n\n')
