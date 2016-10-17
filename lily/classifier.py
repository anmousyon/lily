'''classify the search term using gnb classifier'''
import pickle
import logging
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.cross_validation import train_test_split
from lily import ml_helpers

logging.basicConfig(filename='lily/info/logger.log', filemode='w', level=logging.DEBUG)

def classify(encoders, test, test_):
    '''test the classifier'''
    with open('lily/info/classifier.pickle', 'rb') as cfile:
        classifier = pickle.load(cfile)
    prediction = classifier.predict(test)
    decoded = [key for item in prediction for key, val in encoders[5].items() if item == val]
    actual = [key for item in test_ for key, val in encoders[5].items() if item == val]
    correct = [i for i, j in zip(decoded, actual) if i == j]
    logging.info('accuracy: %s', len(correct)/len(decoded))

def fit_classifier(data):
    '''fit the classifier to the list of lists'''
    data, classes, encoders = ml_helpers.prep_data(data)

    #write to csv for class
    data_csv = pd.DataFrame(data)
    data_csv.to_csv('lily/info/data.csv', index=False, header=False)

    train, test, train_, test_ = train_test_split(data, classes, test_size=0.2, random_state=42)

    classifier = MLPClassifier(algorithm='l-bfgs', epsilon=1e-08, hidden_layer_sizes=(50, 30), learning_rate='constant', learning_rate_init=0.001, max_iter=1000)
    classifier.fit(train, train_)

    with open('lily/info/classifier.pickle', 'wb') as cfile:
        pickle.dump(classifier, cfile)

    classify(encoders, test, test_)

def train_classifier():
    '''train the classifier on the database'''
    data = ml_helpers.get_data()
    fit_classifier(data)
