import sjkabcfunc as sjk
import key_length as kl
import processer as ps
import note
import csv
import os

cwd = os.getcwd()

def write_data(input):
   with open(cwd+'/data.csv', 'w', newline='') as c:
      writer = csv.writer(c)
      writer.writerows(input)

with open(cwd+"/music/test.abc", "r") as f:
#with open("D:/Programming Projects/musicmodels/music/ashover.txt", "r") as f:
   content = f.read()

#mp.parse_tunes(content)


header = ['title', 'key_center', 'sum_dur', 'n_notes', '[p][d]']
rows = [header]
for tune in sjk.Parser(content):
   new = ps.post_song(tune)
   new.extract_notes() #have pitches, durations caluculated

   row = [tune.title[0], new.key_center, new.total_duration, len(new.notelist)]

   for p in new.transposed_pitches:
      row.append(p)
   #row.append(new.transposed_pitches)

   for d in new.durations:
      row.append(d)
   #row.append(new.durations)

   rows.append(row)
   print(row)

   #print(tune.title, tune.key, tune.note_length, "\nMusic: ", new.music)
   #print("default note length: ", new.default_note_length)
   #print("default key: ", new.given_key.key_raw)
   #print("default keymap: ", new.default_keymap)
   #print(new.do_mapping())


   #print(new.pitches)
   #print(new.durations)
   #print(new.notelist)
   #print(new.transposed_pitches)
   #print(len(new.pitches), len(new.durations), len(new.notelist), len(new.transposed_pitches))
   #print('\n\n')


"""
Running Everything
"""

write_data(rows)

