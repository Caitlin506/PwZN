import ascii_graph as ag
import argparse as ap
#import rich
import tqdm
import string
import collections
collections.Iterable = collections.abc.Iterable
#from turtle import color
#from ascii_graph import colors

filename='ATaleOfTwoCities.txt'
filename2='HrabiaMonteChristo.txt'
histo=dict()
histo2=dict()
with open(filename, 'r') as f:
    for line in tqdm.tqdm(f,total=16285):
        sth=line.translate(str.maketrans('','',string.punctuation)).strip().split(' ')
        for w in sth:
            if w in histo.keys():
                histo[w] = histo[w]+1
            else:
                histo[w]=1
                
histo.pop('')
histogram = sorted(histo.items(), key=lambda x: x[1], reverse=True)

graph = ag.Pyasciigraph()
for line in graph.graph('Histogram dla pliku '+filename, histogram[:10]):
    print(line)
    
with open(filename2, 'r') as f:
    for line in tqdm.tqdm(f,total=34907):
        sth=line.translate(str.maketrans('','',string.punctuation)).strip().split(' ')
        for w in sth:
            if w in histo2.keys():
                histo2[w] = histo2[w]+1
            else:
                histo2[w]=1
                
histo2.pop('')
histo2.pop('—')
histogram2 = sorted(histo2.items(), key=lambda x: x[1], reverse=True)

graph2 = ag.Pyasciigraph()
for line in graph2.graph('Histogram dla pliku '+filename2, histogram2[:10]):
    print(line)
