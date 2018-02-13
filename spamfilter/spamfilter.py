
import email, math, os, operator

'''
Function to tokenize each word in an email (text file) and return them as a list of words
'''
def load_tokens(email_path):
    fp = open(email_path)
    message = email.message_from_file(fp)
    words = []
    for line in email.iterators.body_line_iterator(message):
        for word in line.split():
            words.append(word)
    return words
'''
Function to calculate the Laplace-smoothed log-probabilities and store in a dictionary
'''
def log_probs(email_paths, smoothing):
    dir_path = os.getcwd()
    dictionary = dict()
    words = []
    for path in email_paths:
        dir_path = os.getcwd()
        file_path = os.path.join(dir_path, path)
        words = words+load_tokens(file_path)

    # get count of each word
    counts = get_counts(words)
    words_in_file = len(words)

    for word in counts.keys():
        len_other_words = words_in_file - counts[word]
        prob = (counts[word] + smoothing) / (len_other_words + (smoothing*(len(counts)+1)))
        dictionary[word] = math.log(prob)

    prob = smoothing / (words_in_file + (smoothing*(len(counts)+1)))
    dictionary["<UNK>"] = math.log(prob)

    return dictionary

'''
Function to create a dictionary to keep track of frequency count of each word
'''
def get_counts(words):
    wordcounts = dict()
    for word in words:
        if wordcounts.has_key(word):
            count = wordcounts.get(word)
            wordcounts[word] = count+1
        else:
            wordcounts[word] = 1
    return wordcounts

class SpamFilter(object):
    spam_dict = dict()
    ham_dict = dict()
    p_spam = 0
    p_ham = 0

    '''
    Init function to process the training data and adjust log-probabilities of our dictionaries
    '''
    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_paths = [os.path.join(spam_dir, spam_file) for spam_file in os.listdir(spam_dir)]
        ham_paths = [os.path.join(ham_dir, ham_file) for ham_file in os.listdir(ham_dir)]
        self.spam_dict = log_probs(spam_paths, 1e-5)
        self.ham_dict = log_probs(ham_paths, 1e-5)
        self.p_spam = len(spam_paths)/(len(spam_paths)+len(ham_paths))
        self.p_ham = len(ham_paths)/(len(spam_paths)+len(ham_paths))
    '''
    Function to detect whether an individual email is spam or not
    '''
    def is_spam(self, email_path):
        tokens = load_tokens(email_path)
        spam_count = 0; ham_count = 0
        for token in tokens:
            if self.spam_dict.has_key(token):
                spam_count = spam_count+1
            if self.ham_dict.has_key(token):
                ham_count = ham_count+1
        if spam_count > ham_count:
            return True
        return False

    '''
    Function to calculate most indicative spam word using bayes theorem 
    '''
    def most_indicative_spam(self, n):
        allwords = []
        for spam_word, p_spam in self.spam_dict.iteritems():
            if self.ham_dict.has_key(spam_word):
                allwords.append((spam_word, p_spam - math.log(math.exp(self.ham_dict.get(spam_word)) + math.exp(p_spam))))
        allwords.sort(key=operator.itemgetter(1))
        return allwords[:n]

    '''
    Function to calculate most indicative spam word using bayes theorem 
    '''
    def most_indicative_ham(self, n):
        allwords = []
        for ham_word, p_ham in self.ham_dict.iteritems():
            if self.spam_dict.has_key(ham_word):
                allwords.append((ham_word, p_ham - math.log(math.exp(self.spam_dict.get(ham_word)) + math.exp(p_ham))))
        allwords.sort(key=operator.itemgetter(1))
        return allwords[:n]

if __name__ == "__main__":
    sf = SpamFilter("train/spam/","train/ham/", 1e-5)
    print sf.is_spam("train/spam/spam1")
    print sf.is_spam("train/spam/spam2")
    print sf.is_spam("train/ham/ham1")
    print sf.is_spam("train/ham/ham1")
    print sf.most_indicative_spam(5)
    print sf.most_indicative_ham(5)
    