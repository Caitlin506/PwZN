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
histo=dict()
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
for line in graph.graph('My Histogram', histogram[:10]):
    print(line)