import csv
import scipy
from fractions import Fraction as frac
from scipy.stats import beta
def generate_random_beta(n, a, b):
    return beta.rvs(a, b, size=n)

def fit_beta(vars):
    a1, b1, loc1, scale1 = beta.fit(vars)
    #print(a1, b1)
    results = (a1, b1)
    return results



def read_data_file(filename):
    """

    :param filename: csv file
    :return: list of row objects for each song in the file
    """
    songs = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header != None:
            for row in reader:
                songs.append(row_obj(row))

    return songs




class row_obj:
    def __init__(self, *args):
        args = args[0]
        title = args[0]
        keycenter = int(args[1])
        sum_dur = frac(args[2])
        nnotes = int(args[3])

        #print(title, keycenter, sum_dur, nnotes)

        self.title = title
        self.keycenter = keycenter
        self.total_duration = sum_dur
        self.nnotes = nnotes

        p = []
        d= []
        for i in range(nnotes) :
            p.append(int(args[i+3]))
            d.append(frac(args[i+3+nnotes]))
        x = [d / sum_dur for d in d]

        exes = []
        for moment in range(1, len(x)+1):
            upto_now = sum(x[0:moment])
            exes.append(upto_now)

        self.pitches = p
        self.durations = d
        self.xvals = x
        self.times = exes

        #print(nnotes, len(exes))
        #print(x)
        #print(exes)


def create_analysis_sets(rowlist):
    """
    will need to input songs into this function (generated in read_data_file) - or merge these two functions in the future
    :param rowlist:
    :return: analysis sets to do MLE to
    """
    set_mat = [[[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]],
               [[],[],[],[],[],[],[],[],[],[],[],[]]]
    #set_mat=[]

    for row in rowlist:
        for i in range(12):
            for j in range(12):
                #set = []
                for n in range(1, row.nnotes):
                    if row.pitches[n] == j and row.pitches[n-1] == i:
                        set_mat[i][j].append(float(row.times[n]))
                #set_mat[i].insert(j, set)

    #for i in set_mat:
    #    print(i)
    return set_mat




class analysis_set:
    def __init__(self, data_list):
        self.set = data_list

        fits = [[],[],[],[],[],[],[],[],[],[],[],[]]
        for i in range(12):
            for j in range(12):
                current_set = data_list[i][j]
                if len(current_set):
                    mle = fit_beta(current_set)
                    fits[i].append(mle)
                else:
                    fits[i].append('n/a')
        self.fit = fits

        self.dist = create_distribution_matrix(fits)


        #for i in fits:
        #    print(i)

    def trans_size(self):
        for i in self.set:
            for j in i:
                print(len(j))




def create_distribution_matrix(beta_matrix):
    """

    :param beta_matrix: list(list) - a list of 12 lists, each inner list consists of 12 tuples as the paramaters of a beta function
        theoretically created via an analysis_set.find_fit() function on a data set
    :return: mat: list(list) - a list of 12 lists, each inner list consisiting of 12 distribution objects
    """

    mat = [[],[],[],[],[],[],[],[],[],[],[],[]]
    for i in range(12):
        nna = 0     #set number of n/as in row

        #getting value of nna for row
        for j in range(12):
            if beta_matrix[i][j] == 'n/a':
                nna += 1

        #based on the value of nna
        if nna == 0:
            #then the last dist will become non-beta to assure prob 1 at all times
            for j in range(11):
                mat[i].append(beta(beta_matrix[i][j][0], beta_matrix[i][j][1]))  #mult by 1/12
                # mat[i].append
                pass
            nb = mat[i][0:10]   #betalist
            nnadist = nna_bonus(nb, 1)
            mat[i].append(nnadist)


        elif nna >= 1:
            nb1 = [] #betalist
            for j in range(12):
                nb1.append(beta(beta_matrix[i][j][0], beta_matrix[i][j][1]))  #mult by 1/12

            for j in range(12):
                if beta_matrix[i][j] == 'n/a':
                    mat[i].append(nna_bonus(nb1, nna))
                elif beta_matrix[i][j] != 'n/a':
                    mat[i].append(beta(beta_matrix[i][j][0], beta_matrix[i][j][1]))  #   * 1/12

    return mat






class nna_bonus:
    def __init__(self, betalist, n_nna):
        """
        :param betalist: should be beta distrubutions each scaled to 1/12
        """
        self.betas = betalist
        self.n = n_nna

    def pdf(self, x):
        val = 0
        for b in self.betas:
            val += b.pdf(x)

        result = (1 - (1/12)*val)/self.n

        return result

