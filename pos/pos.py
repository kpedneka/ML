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

def tag_counts(sentences):
    counts = dict()
    for sentence in sentences:
        for word in sentence:
            if counts.has_key(word[1]):
                tag_count = counts.get(word[1])
                counts[word[1]] = tag_count+1
            else:
                counts[word[1]] = 1
    return counts

def word_counts(sentences):
    counts = dict()
    for sentence in sentences:
        for word in sentence:
            if counts.has_key(word[0]):
                tag_count = counts.get(word[0])
                counts[word[0]] = tag_count+1
            else:
                counts[word[0]] = 1
    return counts

def start_tag_prob(counts, sentences):
    tags = dict()
    smoothing = 1e-5
    count = len(sentences)
    # calculate start probabilities of tags with laplace smoothing
    for sentence in sentences:
        key = sentence[0][1]
        if tags.has_key(key):
            tags[key] = ( (tags[key]*count) +1) / count
    return tags

def transitions_prob(counts, sentences):
    transitions = dict()
    smoothing = 1e-5
    for sentence in sentences:
        for i in range(1,len(sentence)):
            t_i = sentence[i-1]; t_j = sentence[i]
            # need to store counts of each combination of tags
            # C(t_i-1 | t_i)/C(t_i-1) calculate counts of t_i-1 given t_i divided by count of t_i-1
            key = t_i[1]+t_j[1]
            if transitions.has_key(key):
                count = transitions.get(key)
                transitions[key] = ((count*counts[t_i[1]])+1)/counts[t_i[1]]
            else:
                transitions[key] = float(1)/counts[t_i[1]]
    return transitions

def emission_prob(tag_counts, word_counts, sentences):
    emissions = dict()
    set_of_words = set()
	# create a set of words from the corpus
    for sentence in sentences:
        for word in sentence:
            set_of_words.add(word)
    # update probabilities for each word only once now that it is a set
    for word in set_of_words:
        # stores a tuple in the format (word, probability of word)
        if emissions.has_key(word[1]):
            probs = emissions.get(word[1])
            probs.append((word[0], float(word_counts[word[0]])/tag_counts[word[1]]))
            emissions[word[1]] = probs
        else:
             emissions[word[1]] = [(word[0], float(word_counts[word[0]])/tag_counts[word[1]])]
    return emissions

class Tagger(object):

    def __init__(self, sentences):
        # get counts of tags
        self.tag_counts = tag_counts(sentences)
        self.word_counts = word_counts(sentences)
        self.start_tag_prob = start_tag_prob(self.tag_counts, sentences)
        self.transitions_prob = transitions_prob(self.tag_counts, sentences)
        self.emission_prob = emission_prob(self.tag_counts, self.word_counts, sentences)

    def most_probable_tags(self, tokens):
        highest_prob = 0.
        cur_tag = ""
        tags = []
        for token in tokens:
            for entry in self.emission_prob:
                match = list(filter(lambda x: x[0] == token, self.emission_prob[entry]))
                if len(match) > 0:
                    if match[0][1] > highest_prob:
                        highest_prob = match[0][1]
                        cur_tag = entry
            tags.append(cur_tag)
            cur_tag = ""; highest_prob = 0.
        return tags

    def viterbi_tags(self, tokens):
        pass

if __name__ == "__main__":
    c = load_corpus("brown_corpus.txt")
    # print c[1799]
    # print c[1402]
    t = Tagger(c)
    print t.most_probable_tags(["The", "man", "walks", "."])
    print t.most_probable_tags(["The", "blue", "bird", "sings"])
	