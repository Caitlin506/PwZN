import ascii_graph as ag
import argparse as ap
#import rich
import tqdm
import string
import collections
collections.Iterable = collections.abc.Iterable
#from turtle import color
#from ascii_graph import colors

parser = ap.ArgumentParser()
parser.add_argument("file", help="Creates a histogram of words from a given file")
parser.add_argument('N', nargs='?', type=int, default=10, help='Number of words to be shown in histogram, default=10')
parser.add_argument('min', nargs='?', type=int, default=0, help='Minimal number of letters in a word, default=0')
args = parser.parse_args()

filename=args.file
length = args.N
minimum = args.min
histo=dict()

with open(filename, 'r') as f:
    for line in tqdm.tqdm(f,total=16285):
        sth=line.translate(str.maketrans('','',string.punctuation)).strip().split(' ')
        for w in sth:
            if len(w)>=minimum:
                if w in histo.keys():
                    histo[w] = histo[w]+1
                else:
                    histo[w]=1
            else:
                continue
try:
    histo.pop('—')
except:
    pass
try:
    histo.pop('')
except:
    pass

histogram = sorted(histo.items(), key=lambda x: x[1], reverse=True)

graph = ag.Pyasciigraph()
for line in graph.graph('Histogram dla pliku '+filename, histogram[:length]):
    print(line)