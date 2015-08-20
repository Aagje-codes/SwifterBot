""" Program that takes the texts from Jonathan Swift (author know for writing Gulliver's Travels), the 
Swift Programming Language Manual, and the lyrics of Taylor Swift and returns a new sentence that it
then automagically tweets. """


from nltk.corpus import PlaintextCorpusReader

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
    ALL = '\x1b[33m'		# geel-groen
    TAYLOR = '\x1b[35m' 	# magenta
    MANUAL = '\x1b[32m'		# groen
    JONATHAN = '\x1b[34m'	# paars-blauw
    ENDC = '\x1b[38m'		# zwart


def word_source(sent):
	for word in sent.split():
		if word in common_words:
			return SourceColours.ALL + word + SourceColours.ENDC
		elif word in unique_taylor:
			return SourceColours.TAYLOR + word + SourceColours.ENDC
		elif word in unique_manual:
			return SourceColours.MANUAL + word + SourceColours.ENDC
		elif word in unique_jonathan:
			return 	SourceColours.JONATHAN + word + SourceColours.ENDC
		else:
			return 	SourceColours.OTHER + word + SourceColours.ENDC	

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# CONSTRUCTING THE SENTENCE GENERATOR
# BUILDING THE DICTIONARY
def trigram_builder(words):
	""" Builds a trigram from a list of words. The words should be in order of proper sentences in order for the 
	sentence generator to work"""	
	trigram_dict = {}

	for index in range(len(words)-2):
		key = (words[index+2], words[index+1])
		value = words[index]

		if key in trigram_dict:
			trigram_dict[key].append(value)
		else:
			trigram_dict[key] = []
			trigram_dict[key].append(value)	
			# creates a list that contains strings of values
	
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



# BOIlERPLATE CODE
if __name__ == "__main__":
	trigram_dict = trigram_builder(words)
	sent = sentence_builder(trigram_dict)

	print word_source(sent)

