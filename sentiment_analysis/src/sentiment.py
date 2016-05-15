'''
Can be used for a variety of things. Sentiment or meaning, as a form of opinion mining
Pos or neg as sentiment analysis
'''
import nltk
import random
try:
    import cPickle as pickle
except:
    import pickle
from nltk.classify import ClassifierI
from scipy.stats import mode
from nltk.tokenize import word_tokenize
import os

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers
    def classify(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)[0][0]
    def confidence(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

save_documents = open("../data/pickles/documents.pickle","rb")
documents = pickle.load(save_documents)
save_documents.close()

save_word_features = open("../data/pickles/word_features5k.pickle","rb")
word_features = pickle.load(save_word_features)
save_word_features.close()

def find_features(document):
	words = word_tokenize(document)
	features = {}
	for w in word_features:
		features[w] = (w in words)
	return features

try:

    with open('../data/pickles/voted_classifier.pickle','rb') as classifier_file:
        voted_classifier = pickle.load(classifier_file)

except:

    featuresets = [(find_features(rev),category) for
    (rev,category) in documents]
    random.shuffle(featuresets)

    # set that we'll train our classifier with
    training_set = featuresets[:10000]

    # set that we'll test against.
    testing_set = featuresets[10000:]

    classifier_f = open("../data/pickles/originalnaivebayes5k.pickle", "rb")
    classifier = pickle.load(classifier_f)
    classifier_f.close()
    nltk.classify.accuracy(classifier, testing_set)

    save_classifier2 = open("../data/pickles/MNB_classifier5k.pickle","rb")
    MNB_classifier = pickle.load(save_classifier2)
    save_classifier2.close()
    nltk.classify.accuracy(MNB_classifier, testing_set)

    save_classifier = open("../data/pickles/BernoulliNB_classifier5k.pickle","rb")
    BNB_classifier = pickle.load(save_classifier)
    save_classifier.close()
    nltk.classify.accuracy(BNB_classifier, testing_set)

    save_classifier = open("../data/pickles/LogisticRegression_classifier5k.pickle","rb")
    LogisticRegression_classifier = pickle.load(save_classifier)
    save_classifier.close()
    nltk.classify.accuracy(LogisticRegression_classifier, testing_set)

    save_classifier = open("../data/pickles/SGDC_classifier5k.pickle","rb")
    SGDClassifier_classifier = pickle.load(save_classifier)
    save_classifier.close()
    nltk.classify.accuracy(SGDClassifier_classifier, testing_set)

    save_classifier = open("../data/pickles/LinearSVC_classifier5k.pickle","rb")
    LinearSVC_classifier = pickle.load(save_classifier)
    save_classifier.close()
    nltk.classify.accuracy(LinearSVC_classifier, testing_set)

    voted_classifier = VoteClassifier(classifier,MNB_classifier,BNB_classifier,LogisticRegression_classifier,SGDClassifier_classifier,LinearSVC_classifier)
    nltk.classify.accuracy(voted_classifier, testing_set)

    with open('../data/pickles/voted_classifier.pickle','wb') as classifier_file:
        pickle.dump(voted_classifier, classifier_file)

def sentiment(text):
    feats = find_features(text)
    if voted_classifier.classify(feats) == 'pos':
        return 1
    else:
        return -1
    #return voted_classifier.classify(feats),voted_classifier.confidence(feats)
