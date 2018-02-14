'''
The skeleton for this file was sourced from CIS 521 of U Penn
source link: http://www.seas.upenn.edu/~cis521/#ASSIGNMENTS
'''
import os

def load_corpus(path):
    fp = open(os.path.join(os.getcwd(), path))
    lines = fp.readlines()
    c = []
    for line in lines:
    	l = []
    	line = line.strip()
    	items = line.split(' ')
    	for item in items:
    		l.append((item.split('=')[0], item.split('=')[1]))
    	c.append(l)
    return c

class Tagger(object):

    def __init__(self, sentences):
        pass

    def most_probable_tags(self, tokens):
        pass

    def viterbi_tags(self, tokens):
        pass

if __name__ == "__main__":
	c = load_corpus("brown_corpus.txt")
	print c[1799]
	print c[1402]
