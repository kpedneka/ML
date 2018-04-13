# ML
This is a set of projects that I decided to do in order to learn about machine learning. All of these assignments have been assignments for UPenn's [CIS521](http://www.seas.upenn.edu/~cis521/Homework/homework7.html) course.

### Frankenstein
An introduction to NLP. I gained experience with using n-grams and Markov models.This program allows a user to specify the length of the context and the length of the text to generate.
It does this by ingesting a large body of text to create an n-gram model. The n-gram calculates the probability of the next token given the current context.
In this pattern we can generate random text of any length! 
Sample output:
```
m = create_ngram_model(7, sys.argv[1])
print m.random_text(30)
>>> Oh! The generous nature of Safie was outraged by this command ; she attempted to expostulate with her father , but he left her angrily , reiterating his
```
To run it yourself:
```
$ cd frankenstein
$ python frank.py frankenstein.txt
```

### POS tagging
Part of speech tagging uses hidden markov models to determine the most likely part of speech that each word in a sentence belongs to as defined by the Brown corpus.
For example: 
```
["The", "man", "walks", "."]
['DET', 'NOUN', 'VERB', '.']
```
This is particularly useful when it comes to translating text from one language to another. Google translate uses POS tagging.

### Spam Filter
This was my first ML project. I got to implement a Naive Bayes classification to label emails as spam emails or not spam emails.
The model is trained with some training data to initialize the weights of each word being spam or not spam. In testing, the email is classified as either spam or not spam in only 1 iteration.
To run it yourself:
```
$ cd spamfilter
$ python spamfilter.py
```
