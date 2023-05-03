from __future__ import print_function
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from urllib.parse import urlparse,unquote
import numpy as np
import string
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

# laoding main  model of detection
CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, 'models' ,'lstm_final.h5')
MODEL=tf.keras.models.load_model(MODEL_PATH)
CONFIG= MODEL.get_config()
LENGTH=CONFIG["layers"][0]["config"]["batch_input_shape"][1]

class AnomalyDetect(): 
    def __init__(self):
        pass
     
    def string_to_index(self,str_request,dictionary):
        index_request=np.zeros(len(str_request))
        for i in range(len(str_request)):
            try:
                index_request[i]=dictionary[str_request[i]]
            except KeyError:
                pass
        return tf.convert_to_tensor(index_request,dtype=tf.int32)

    def create_dict(self):
        dictionary={}
        alphabet=string.ascii_lowercase+string.digits+string.punctuation+' '
        for i in range(len(alphabet)):
            dictionary[alphabet[i]]=i
        return dictionary
    
    def predict(self,payload):
        #loading model
        dictionary= self.create_dict()
        payload = self.string_to_index(payload,dictionary)
        data=[payload]
        data=tf.keras.preprocessing.sequence.pad_sequences(data,padding='post',maxlen=LENGTH)
        return MODEL.predict(data).round()[0] == 1
    

class SQLIDetect():

    SQL_KEYWORDS=[
        'TABLE',
        'TABLESPACE',
        'PROCEDURE',
        'FUNCTION',
        'TRIGGER',
        'KEY',
        'VIEW',
        'MATERIALIZED VIEW',   
        'LIBRARYDATABASE LINK',
        'DBLINK',
        'INDEX',
        'CONSTRAINT',
        'TRIGGER',
        'USER',
        'SCHEMA',
        'DATABASE',
        'PLUGGABLE DATABASE',
        'BUCKET',
        'CLUSTER',
        'COMMENT',
        'SYNONYM',
        'TYPE',
        'JAVA',
        'SESSION',
        'ROLE',
        'PACKAGE',
        'PACKAGE BODY',
        'OPERATORSEQUENCE',
        'RESTORE POINT',
        'PFILE',
        'CLASS',
        'CURSOR',
        'OBJECT',
        'RULE',
        'USER',
        'DATASET',
        'DATASTORE',
        'COLUMN',
        'FIELD',
        'OPERATOR',
        'SHUTDOWN',
    ]

    SQL_REGEX=[
        "(?i)(.*)(\\b)+(OR|AND)(\\s)+(true|false)(\\s)*(.*)",
        "(?i)(.*)(\\b)+(OR|AND)(\\s)+(\\w)(\\s)*(\\=)(\\s)*(\\w)(\\s)*(.*)",
        "(?i)(.*)(\\b)+(OR|AND)(\\s)+(equals|not equals)(\\s)+(true|false)(\\s)*(.*)",
        "(?i)(.*)(\\b)+(OR|AND)(\\s)+([0-9A-Za-z_'][0-9A-Za-z\\d_']*)(\\s)*(\\=)(\\s)*([0-9A-Za-z_'][0-9A-Za-z\\d_']*)(\\s)*(.*)",
        "(?i)(.*)(\\b)+(OR|AND)(\\s)+([0-9A-Za-z_'][0-9A-Za-z\\d_']*)(\\s)*(\\!\\=)(\\s)*([0-9A-Za-z_'][0-9A-Za-z\\d_']*)(\\s)*(.*)",
        "(?i)(.*)(\\b)+(OR|AND)(\\s)+([0-9A-Za-z_'][0-9A-Za-z\\d_']*)(\\s)*(\\<\\>)(\\s)*([0-9A-Za-z_'][0-9A-Za-z\\d_']*)(\\s)*(.*)",
        "(?i)(.*)(\\b)+SELECT(\\b)+\\s.*(\\b)(.*)",
        "(?i)(.*)(\\b)+SELECT(\\b)+\\s.*(\\b)+FROM(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+INSERT(\\b)+\\s.*(\\b)+INTO(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+UPDATE(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+DELETE(\\b)+\\s.*(\\b)+FROM(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+UPSERT(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+SAVEPOINT(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+CALL(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+ROLLBACK(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+KILL(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+DROP(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+CREATE(\\b)+(\\s)*(" + "|".join(SQL_KEYWORDS) + ")(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+ALTER(\\b)+(\\s)*(" +  "|".join(SQL_KEYWORDS) + ")(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+TRUNCATE(\\b)+(\\s)*(" +  "|".join(SQL_KEYWORDS) + ")(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+LOCK(\\b)+(\\s)*(" +  "|".join(SQL_KEYWORDS) + ")(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+UNLOCK(\\b)+(\\s)*(" +  "|".join(SQL_KEYWORDS) + ")(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+RELEASE(\\b)+(\\s)*(" +  "|".join(SQL_KEYWORDS) + ")(\\b)+\\s.*(.*)",
        "(?i)(.*)(\\b)+DESC(\\b)+(\\w)*\\s.*(.*)",
        "(?i)(.*)(\\b)+DESCRIBE(\\b)+(\\w)*\\s.*(.*)",
        "(.*)(/\\*|\\*/|;){1,}(.*)",
        "(.*)(-){2,}(.*)",
    ]
    def __init__(self):
        pass
    # detection of SQL injection using pattern matching
    # payload: the statement to be checked
    # The function returns True if the statement is a SQL injection, False otherwise
    def Regex_detect(self, payload):
        if payload.strip() == "":
            return False

        for pattern in self.SQL_REGEX:
            if re.search(pattern,payload,flags=re.IGNORECASE|re.UNICODE):
                return True
        return False
    # detection of SQL injection using machine learning
    def ML_detect(self, payload):
        with open('../models/sqli_model.pkl', 'rb') as f:
            model,vectorizer = pickle.load(f)
        data=vectorizer.transform([payload])
        return model.predict(data).round()[0]==1
    # this function checks if the patterns are valid
    def check_patterns(self):
        for pattern in self.SQL_REGEX:
            if not re.compile(pattern):
                return False
        return True
    
class XSSDetect():
    def __init__(self):
        pass
    # detection of XSS using Machine Learning
    def ML_detect(self, payload):
        with open('../models/xss_model.pkl', 'rb') as f:
            model,vectorizer = pickle.load(f)
        data=vectorizer.transform([payload])
        return model.predict(data).round()[0] == 1


def isAnomalous(payload):
    anomalyDetect=AnomalyDetect()
    return anomalyDetect.predict(payload)
def getAttackType(payload):
    sqli=SQLIDetect()
    xss=XSSDetect()
    if sqli.Regex_detect(payload) or sqli.ML_detect(payload):
        return "SQLi"
    elif xss.ML_detect(payload):
        return "XSS"
    else:
        return "Suspicious"


payload="/dvwa/vulnerabilities/exec?"
print(payload)
if isAnomalous(payload):
    print("Anomaly detected")
    print(f"attack type:{getAttackType(payload)}")
else:
    print("No anomaly detected")
