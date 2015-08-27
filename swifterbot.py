""" Program that takes the texts from Jonathan Swift (author know for writing Gulliver's Travels), the 
Swift Programming Language Manual, and the lyrics of Taylor Swift and returns a new sentence that it
then automagically tweets. """


from nltk.corpus import PlaintextCorpusReader
from random import choice
import sys
import tweepy



# SETTING UP THE DATA

# BUILDING THE CORPUS
location = '/Users/Aagje/Python01/Projects/Swifterbot/data'
swift_corpus = PlaintextCorpusReader(location, '.*.txt')

# Adjusting for disparity between corpora
taylor = [word for word in swift_corpus.words('swift_lyrics.txt')]*12

manual = [word for word in swift_corpus.words('swift_manual.txt')]*8

jonathan = []
for fileid in swift_corpus.fileids():
    if fileid == 'swift_lyrics.txt':
        continue
    elif fileid == 'swift_manual.txt':
        continue
    else:
        add = [word for word in swift_corpus.words(fileid)]
        jonathan = jonathan + add 

# WORDS!!
words = jonathan + manual + taylor


# Unique sets
common_words = sorted(set(manual)&set(taylor)&set(jonathan))
unique_taylor = sorted(set(taylor) - (set(jonathan)| set(manual)))
unique_manual = sorted(set(manual) - (set(jonathan) | set(taylor)))
unique_jonathan = sorted(set(jonathan) - (set(taylor) | set(manual)))



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Strangely enough I will not begin with the actual bot, but instead with write a few lines that will let us analyze the text
# to see from which source the words come. For this we'll look at the references Madelyn sent me:
# http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
class SourceColours:
    OTHER = '\x1b[37m'		# grey
    ALL = '\x1b[31m'		# geel-groen
    TAYLOR = '\x1b[35m' 	# magenta
    MANUAL = '\x1b[32m'		# groen
    JONATHAN = '\x1b[34m'	# paars-blauw
    ENDC = '\x1b[0m'		# zwart


def word_source(sent):
	print "\n\n"
	for word in sent.split():		
		if word in common_words:
			print(SourceColours.ALL + word + SourceColours.ENDC),
		elif word in unique_taylor:
			print(SourceColours.TAYLOR + word + SourceColours.ENDC),
		elif word in unique_manual:
			print(SourceColours.MANUAL + word + SourceColours.ENDC),
		elif word in unique_jonathan:
			print(SourceColours.JONATHAN + word + SourceColours.ENDC),
		else:
			print(SourceColours.OTHER + word + SourceColours.ENDC),	
	print "\n\n"
				
				
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# CONSTRUCTING THE SENTENCE GENERATOR
# BUILDING THE DICTIONARY
def trigram_builder(words):
    """ Builds a trigram from a list of words. The words should be in order of proper sentences in order for the 
    sentence generator to work"""
    trigram_dict = {}
    
    end_punct = ['.', '!', '?', '...', '....']
    
    for index in range(len(words)-2):
        key = (words[index+2], words[index+1])
        value = words[index]
        if value in end_punct:
            continue    		#In other words: don't add end-punctuations to the list of values
        elif key in trigram_dict:
            trigram_dict[key].append(value)
        else:
            trigram_dict[key] = []
            trigram_dict[key].append(value)	
            # creates a list that contains strings of value
        
    return trigram_dict	


# GENERATING THE SENTENCE
def sentence_builder(trigram_dict):
	"""Building the sentence from a trigram_dict"""

	new_sent = []
	end_punct = ['.', '!', '?', '...', '....']
	potential_first_pairs = [pair for pair in trigram_dict.keys() if pair[0] in end_punct]
	# potential_first_pairs returns a list of tuples

	# pudb.set_trace()

	first_pair = choice(potential_first_pairs)
	# first_pair is a tuple
	
	for word in first_pair:
		new_sent.append(word)

	while not new_sent[-1].istitle() and not new_sent[-1].isupper():
		
		potential_words = [word for word in trigram_dict[first_pair]]
		

		new_word = choice(potential_words)
			
		new_sent.append(new_word)
		
		first_pair = (new_sent[-2], new_sent[-1])
	
	return ' '.join(new_sent[::-1])


#  Setting up the twitter bot
def pushTweet(sentence):
	#enter the corresponding information from your Twitter application:
	api_key, api_secret, access_token, token_secret = sys.argv[1:] # Automagically picks up the details form the command line. 
	# api_key = raw_input("api_key > ")  
	# api_secret = raw_input("api_secret > ")
	# access_token = raw_input("Acces_token > ")
	# token_secret = raw_input("Token_secret > ")
	auth = tweepy.OAuthHandler(api_key, api_secret)
	auth.set_access_token(access_token, token_secret)
	api = tweepy.API(auth)
	# this is how we'll connect our robot to Twitter through our application

	api.update_status(status=sentence) 	# Generates the Tweet

def test(trigram_dictionary):
	sent = sentence_builder(trigram_dictionary)
	
	print word_source(sent)

	if len(sent) < 140:
		pushTweet(sent)
	else:
		test(trigram_dict)


# BOIlERPLATE CODE
if __name__ == "__main__":
	trigram_dict = trigram_builder(words)

	test(trigram_dict)	