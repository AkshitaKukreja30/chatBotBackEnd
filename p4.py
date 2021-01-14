import nltk
import numpy as np
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tag import pos_tag #for identifying proper nouns
from flask_api import FlaskAPI
from flask import request, render_template
from flask_cors import CORS

app = FlaskAPI(__name__)
CORS(app) # This will enable CORS for all routes
app.debug = True

textFileName = 'about.txt'
sent_tokens = []

def readInputFile(textFileName):
    print(textFileName)
    f=open(textFileName,'r',errors = 'ignore')
    raw_text = f.read()
    sent_tokens = nltk.sent_tokenize(raw_text)# converts to list of sentences
    word_tokens = nltk.word_tokenize(raw_text)# converts to list of words
    lemmer = nltk.stem.WordNetLemmatizer()
    # print(type(sent_tokens))
    # print(type(lemmer))
    return sent_tokens,lemmer

@app.route('/getFileContents')
def getFileContents():
    fileName = request.args.get('fileName')
    print(fileName)
    f=open(fileName,'r',errors = 'ignore')
    raw_text = f.read()
    return raw_text

# def tokensFromdata(raw_text):
#     sent_tokens = nltk.sent_tokenize(raw_text)# converts to list of sentences
#     word_tokens = nltk.word_tokenize(raw_text)# converts to list of words
#     lemmer = nltk.stem.WordNetLemmatizer()
#     return sent_tokens,lemmer

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def greeting(sentence):
    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
    GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

@app.route('/')
def home():    
    return "Hello from server"

@app.route('/getDataSetName')
def getDataSetName():
    print('api call')
    category = request.args.get('category')
    category =category.upper() 
    print(category)
    if category == 'CG':
        textFile = "about.txt"
    elif category == 'ENERGY':
        textFile = "energy.txt"
    else:
        textFile = "ecom.txt"   
    global textFileName
    textFileName = textFile
    print('textFileName')
    print(textFileName)
    runThisEveryTime(textFileName)
    return textFile   

@app.route('/upload')
def uploadDataSet():
    return "Hi"

def runThisEveryTime(textFileName):
    print('runthiseverytime')
    print(textFileName)
    global sent_tokens
    global lemmer
    # if textFileName == 'SAME':
    #     return sent_tokens
    sent_tokens = readInputFile(textFileName)[0]
    lemmer = readInputFile(textFileName)[1]
    robo_response = ''
    # return sent_tokens

print('textFile'+ textFileName)
@app.route('/getChatResponse')
def getRes():
    print('in getChatResponse')
    robo_response=''
    userQuery = request.args.get('input')
    print(userQuery)
    userQuery=userQuery.lower()
    if(userQuery!='bye'):
        if(userQuery=='thanks' or userQuery=='thank you' ):
            return "Most welcome."
        elif(userQuery== 'good morning'):
            return "Good Morning!"
        elif(userQuery == 'good evening'):
            return "Good Evening!"
        elif(userQuery == 'good night'):
            return "Good Night!Sleep well"
        else:
            if(greeting(userQuery)!=None):
                return greeting(userQuery)
            else:
                return response(userQuery)
                
    else:
        return "Bye! Take Care."


print('textFile before response method')
print(textFileName)
sent_tokens = readInputFile(textFileName)[0]
lemmer = readInputFile(textFileName)[1]
robo_response = ''

print('before response')
print(textFileName)

def response(user_response):
    print('in response')
    print(textFileName)
    robo_response=''
    print('sent tokens')
    print(sent_tokens)
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    print(idx)
    flat = vals.flatten()
    flat.sort()
    print(flat)
    req_tfidf = flat[-2]
    print(req_tfidf)
    print(robo_response)
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        if(user_response in sent_tokens):sent_tokens.remove(user_response)
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        if(user_response in sent_tokens):sent_tokens.remove(user_response)
        return robo_response

if __name__ == '__main__':
    # textFileName = ''
    # runThisEveryTime(textFileName)
    app.run()
   