import csv
import scipy


def read_data_file(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)

    songs = []
    for row in reader:
        songs.append(row_obj(row))
    return

class row_obj:
    def __init__(self, title, key_center, sum_dur, nnotes, *args):
        self.title = title
        self.keycenter = key_center
        self.total_duration = sum_dur
        self.nnotes = nnotes

        p = []
        d= []
        for i in range(nnotes) :
            p.append(*args[i])
            d.append(*args[i+nnotes])
        x = [d / sum_dur for d in d]

        self.pitches = p
        self.durations = d
        self.xvals = x


