from __future__ import print_function
from sklearn.feature_extraction.text import CountVectorizer
from urllib.parse import urlparse, unquote
from store import SQL_REGEX ,UNIX_ALIASES,PATH_TRAVERSAL_REGEX
import re
import pickle
import numpy as np
import string
from urllib.parse import urlparse, parse_qs
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

'''
    # Global variables
    1- CURRENT_DIR: the current directory of the project
    2- MODEL_PATH: the path of the model
    3- MODEL: the model
    4- CONFIG: the configuration of the model
    5- LENGTH: the length of the input of the model 
'''
CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, 'models', 'cnn_lstm_final.h5')
MODEL = tf.keras.models.load_model(MODEL_PATH)
CONFIG = MODEL.get_config()
LENGTH = CONFIG["layers"][0]["config"]["batch_input_shape"][1]


class AnomalyDetect():
    def __init__(self):
        pass
    # Creating a dictionary to map each character to an index
    def create_dict(self):
        dictionary = {}
        alphabet = string.ascii_lowercase+string.digits+string.punctuation+' '
        for i in range(len(alphabet)):
            dictionary[alphabet[i]] = i
        return dictionary
    # transform the string to a vector of indexes tensors
    def string_to_index(self, str_request, dictionary):
        index_request = np.zeros(len(str_request))
        for i in range(len(str_request)):
            try:
                index_request[i] = dictionary[str_request[i]]
            except KeyError:
                pass
        return tf.convert_to_tensor(index_request, dtype=tf.int32)
    
    # Predicting the class of the request (normal or anomalous)
    def predict(self, payload):
        # loading model
        dictionary = self.create_dict()
        payload = self.string_to_index(payload, dictionary)
        data = [payload]
        data = tf.keras.preprocessing.sequence.pad_sequences(
            data, padding='post', maxlen=LENGTH)
        return MODEL.predict(data).round()[0] == 1

class SQLIDetect():

    def __init__(self):
        pass
    # detection of SQL injection using pattern matching
    # payload: the statement to be checked
    # The function returns True if the statement is a SQL injection, False otherwise

    def Regex_detect(self, payload):
        if payload.strip() == "":
            return False

        for pattern in SQL_REGEX:
            if re.search(pattern, payload, flags=re.IGNORECASE | re.UNICODE):
                return True
        return False
    # detection of SQL injection using machine learning

    def ML_detect(self, payload):
        with open('../models/sqli_model.pkl', 'rb') as f:
            model, vectorizer = pickle.load(f)
        data = vectorizer.transform([payload])
        return model.predict(data).round()[0] == 1
    # this function checks if the patterns are valid

    def check_patterns(self):
        for pattern in SQL_REGEX:
            if not re.compile(pattern):
                return False
        return True

class XSSDetect():
    def __init__(self):
        pass
    # detection of XSS using Machine Learning

    def ML_detect(self, payload):
        with open('../models/xss_model.pkl', 'rb') as f:
            model, vectorizer = pickle.load(f)
        data = vectorizer.transform([payload])
        return model.predict(data).round()[0] == 1

class CMDiDetect():
    def __init__(self):
        pass
    # detection of Command injection
    def Detect(self, payload):
        if payload.strip() == "":
            return False

        escaped_aliases = [re.escape(alias) for alias in UNIX_ALIASES]
        cmdi_regex = r".*(;|\||&&|\n)( |)(" + "|".join(escaped_aliases) + ").*$"

        if re.search(cmdi_regex, payload, flags=re.IGNORECASE | re.UNICODE):
            return True
        return False


# This function checks if the request is anomalous or not
def isAnomalous(payload):
    anomalyDetect = AnomalyDetect()
    return anomalyDetect.predict(payload)

# This function checks if the request is malicious or not
def getAttackType(payload):
    sqli = SQLIDetect()
    xss = XSSDetect()
    cmdi = CMDiDetect()
    
    if cmdi.Detect(payload):
        return "CMDi"
    elif xss.ML_detect(payload):
        return "XSS"
    elif re.search(PATH_TRAVERSAL_REGEX, payload, flags=re.IGNORECASE | re.UNICODE):
        return "PTR"
    elif sqli.ML_detect(payload):
        return "SQLi"
    else:
        return "Suspicious"
