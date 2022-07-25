import sjkabcfunc as sjk
import key_length as kl
import song_processer as ps
import note
import csv
import os
import ast
import data_reader as dr
import numpy as np
#import analyze_set as an

cwd = os.getcwd()

class generator:
   def __init__(self, fit_filename):
      # reading fit data
      with open(cwd + "/" + fit_filename, "r") as f:
         reader = csv.reader(f)
         rowlist = list(reader)  # list of lists - inner have strings

      ##format back into list of lists
      fitmat = [[], [], [], [], [], [], [], [], [], [], [], []]
      for row in rowlist:


         for i in range(12):
            if row[i] == 'n/a':
               fitmat[i].append(row[i])
            else:
               fitmat[i].append(ast.literal_eval(row[i]))
      # print(fitmat)
      self.fitmat = fitmat

      distmat = dr.create_distribution_matrix(fitmat)
      self.distmat = distmat

      ##set scaling factors
      scales = [[], [], [], [], [], [], [], [], [], [], [], []]
      #for row in rowlist:
       #  nscale = 0
         #for i in range(12):
         #   if row[i] == 'n/a':
          #     nscale += 1

      #putting scales into matrix

      for row in distmat:
         for i in range(12):
            if type(row[i]) is dr.nna_bonus :
               scales[i].append(1)   #dont need to scale for nna dist bc embedded in pdf calc
            else:
               scales[i].append(1/12)   #if its a beta dist then 1/12


      self.scales = scales

      for i in scales:
         print(i)
         print(len(i))

      #for i in distmat:
       #  print(i)
         #print(len(i))



   def generate_pitch_melody(self, start_pitch, total_notes):
      """

      :param start_pitch: integer value of starting pitch class for melody
      :param total_notes: total number of notes to be in melody
      :return:
      """
      #for i in range(12):
        # print(self.distmat[i])

      #for i in range(12):
      print(self.fitmat[0])

      increment = 1/total_notes
      melody_pitches = [start_pitch]

      for t in range(1, total_notes+1):
         #situating ourselves in the melody
         current_time = increment * t
         next_time = increment * (t+1)
         last_pitch = melody_pitches[t-1]

         print(current_time, '\t',next_time)

         #setting up to generate next value
         trans_row = []
            #getting dist row for last pitch
         pit_row = self.distmat[last_pitch]
         print(pit_row)

         #creating row of transition probabilities
         for i in range(12):
            #print(pit_row[i].cdf(next_time), '\t', pit_row[i].cdf(current_time))
            pdf_val = pit_row[i].pdf(current_time)
            trans_row.append(pdf_val)

         print(trans_row)
         print(np.sum(trans_row))
         next_pit = np.random.choice(range(12), 1, p=trans_row)

         print(next_pit)
         melody_pitches.append(next_pit)

      return melody_pitches


######################################################
######################################################
######################################################

test = generator('afit.csv')

#test.generate_pitch_melody(0, 12)

#for i in test.distmat:
   #s = 0
   #for j in i:
      #type(j) is dr.nna_bonus :
      #print(j, j.cdf(0.9999999999999999999))

w = test.distmat[0][0]
print(w, w.pdf(0.8))
