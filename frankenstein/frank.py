'''
The skeleton for this file was sourced from CIS 521 of U Penn
source link: http://www.seas.upenn.edu/~cis521/#ASSIGNMENTS
'''
import sys, re, math, random, os, string

'''
Function to tokenize text of file, treat all punctuations as separate tokens
'''
def tokenize(text):
    delimiters = string.punctuation
    words = re.findall(r"[\w]+|["+delimiters+"]", text)
    return words

def ngrams(n, tokens):
    # padding string with start and end
    for i in range(n):
        tokens.insert(0,"<START>")
    tokens.append("<END>")
    # generate the ngram array
    ngrams = []
    for i in range(n,len(tokens)):
        ngrams.append((tuple(tokens[i-n+1:i]),tokens[i]))
    return ngrams

class NgramModel(object):
    n = 1
    ngrams = []

    def __init__(self, n):
        self.n = n

    def update(self, sentence):
        self.ngrams = self.ngrams+ngrams(self.n, tokenize(sentence))

    def prob(self, context, token):
        ctx_count = 0; match_count = 0
        for i, v in enumerate(self.ngrams):
            if v[0] == context:
                ctx_count = ctx_count+1
                if v[1] == str(token):
                    match_count = match_count+1
        # protect against divide by 0 case
        if ctx_count == 0:
            return 0
        return float(match_count)/float(ctx_count)

    def random_token(self, context):
        tokens = set()
        # get all tokens that are preceeded by context
        for i, v in enumerate(self.ngrams):
            if v[0] == context:
                tokens.add(v[1])

        tokens = list(tokens)
        tokens.sort()
        # get random number 0 < r < 1
        random_num = random.random()
        cdf = 0.0
        print 'RANDOM', random_num
        # find token where probability fits our criteria
        for i in range(len(tokens)):
            cdf = cdf+self.prob(context, tokens[i])
            if cdf > random_num:
                return tokens[i]
        return "<END>"

    def random_text(self, token_count):
        random_sentence = []
        orig_start_context = []
        print "Entered random_text Function"
        for i in range(self.n-1):
            orig_start_context.insert(0,"<START>")
        
        # start_token must be the n-1 start labels
        curr_context = tuple(orig_start_context)
        for i in range(token_count):
            # generate random word based on proability, add it to sentence
            random_word = self.random_token(curr_context)
            random_sentence.append(random_word)
            print i
            if random_word == "<END>":
                curr_context = tuple(orig_start_context)
            else:
                curr_context = self.update_context(curr_context, random_word)
        return random_sentence

    def update_context(self, context, token):
        context = list(context)
        if len(context) == 0:
            return tuple(context)
        del context[0]
        context.append(token)
        return tuple(context)

    def perplexity(self, sentence):
        pass

def create_ngram_model(n, path):
    path = os.path.join(os.getcwd(), path)
    fp = open(path)
    lines = fp.readlines()

    m = NgramModel(n)
    
    for line in lines:
        m.update(line)
    
    return m

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Improper arguments, follow python frank.py <text file>"
        exit()
    '''
    m = NgramModel(1)
    m.update("a b c d")
    m.update("a b a b")
    # print m.prob((), "a")
    # print m.prob((), "c")
    # print m.prob((), "<END>")
    # print m.prob(("<START>",), "a")
    # print m.prob(("b",), "c")
    # print m.prob(("a",), "x")
    print "=========="
    random.seed(1)
    # print [m.random_token(()) for i in range(25)]
    # print [m.random_token(("<START>",)) for i in range(6)]
    # print [m.random_token(("b",)) for i in range(6)]
    print "=========="
    print m.random_text(13)
    '''
    random.seed(6)
    m = create_ngram_model(4, sys.argv[1])
    print m.random_text(15)
    # m = create_ngram_model(3, sys.argv[1])
    # print m.random_text(15)
    # m = create_ngram_model(2, sys.argv[1])
    # print m.random_text(15)
    m = create_ngram_model(7, sys.argv[1])
    print m.random_text(30)
