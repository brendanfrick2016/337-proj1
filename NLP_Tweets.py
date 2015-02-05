import operator
import re, string
## Imports Stanford's Named Entity Recognition Tagger
from nltk.tag.stanford import NERTagger


## Initialize tagger, make sure these files are in the same directory
st = NERTagger('english.all.3class.distsim.crf.ser.gz', 'stanford-ner.jar', 'utf-8')

## Category
##  contains:
##      - Name/Title
##      - Associated Tweets
##      - Associated decisions (winner, loser, presenter, nominees, etc.)
class Category:

    # Category(name,decisions)
    #   Set name
    #   Set decisions
    #   Set keys
    def __init__(self,nam,key):
        self.name = nam
        self.keys = key
        self.tweets = []
        self.nominees  = {}
        self.presenters = {}

    # addTweet(tweet)
        # Add parsed tweet to two dimensional array
    def addTweet(self,t):
        self.tweets.append(t)

    def addNominees(self,nom):
        for n in nom:
            if n in self.nominees.keys():
                self.nominees[n] += 1
            else:
                self.nominees[n] = 1

    def addPresenter(self,pres):
        for n in nom:
            if n in self.nominees.keys():
                self.nominees[n] += 1
            else:
                self.nominees[n] = 1

    def findWinner(self):
        try:
            return max(self.nominees.iteritems(), key=operator.itemgetter(1))[0]
        except Exception:
            return 'Error. No nominees added'

    
        
## Global Keys
##  Keys are the words we are searching for
##  The keys I'm using are not refined at all, probably wouldn't work to well
##  Idea - use a dictionary to weight keys (i.e. {Best:1,Actor:2,Drama:5})
BEST_ACTOR_DRAMA = ['best','actor','drama']
BEST_ACTOR_COMEDY = ['best','actor','comedy']

## Global Structures
catArray = [Category('Best Actor in a Drama',BEST_ACTOR_DRAMA),
            Category('Best Actor in a Comedy', BEST_ACTOR_COMEDY)]

## processTweets
##  Checks tweets line by line
##      - Tags each tweet
##  Iterative debugger. Probably can remove

def processTweets():
    fname = "gg13tweets.txt"

    with open(fname, "r") as ins:
        feed = [] #Line by line
        for line in ins:
            feed.append(line.split())

    for tweet in feed: # Run through each tweet
        tagTweetCat(tweet)        # Run through each category

    findWinners()
    
    
            
        

## tagTweetCat(tweet)
##  Checks categories one at a time
##  Right now this puts the tweet that has the highest score (for debugging purposes)
def tagTweetCat(tweet):
    ind = -1
    scores = {}
    # Place tweet in appropriate categories
    for cat in catArray:
        ind += 1
        scores[ind] = 0
        # Search word by word and compare against keyword set for each category
        for tword in tweet:
            if tword.lower() in cat.keys:
                scores[ind] += 1 #Augment category score
    if max(scores.values()) > 1: # Thresholding
        ind = max(scores.iteritems(), key=operator.itemgetter(1))[0]    # Index of highest scoring category
    else:
        ind = -1
        
    if ind > -1:
        catArray[ind].addTweet(tweet)                   # Add Tweet
        catArray[ind].addNominees(findPeople(tweet))    # Add People
       

    
## Regex functions
FN_and_LN ="([A-Z][a-z]*)[\s-]([A-Z][a-z]*)"
FN_or_LN = "([A-Z][a-z]+)"
    

## findPeople(tweet, key)
##  returns set of people in the tweet
def findPeople(tweet):
    nominees = list()
    st.tag
    try:
        tagged = st.tag(tweet)
        print tagged
        for item in tagged:
          if item[1] == u'PERSON':
            print "found a person! " + item[0]
            nominees.append(item[0])
    except Exception:
        print "encoding error, reverting to naive"
        FN_or_LN_noms = re.findall(FN_or_LN,' '.join(tweet))
        FN_and_LN_noms = re.findall(FN_and_LN,' '.join(tweet))
        #Filter duplicates
        for name_1 in FN_or_LN_noms:
            for name_2 in FN_and_LN_noms:
                if name_1 in name_2:
                    if name_1 in FN_or_LN_noms:
                        FN_or_LN_noms.remove(name_1)
    

        # Return single names then last names
        nominees = FN_or_LN_noms + FN_and_LN_noms
    return nominees

def findWinners():
    for cat in catArray:
        print ""+ cat.name + ": " + cat.findWinner()   
            
def main():
    processTweets()

if __name__ == "__main__":
    main()

    

    

