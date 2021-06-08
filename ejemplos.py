import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('punkt')
nltk.download('stopwords')

#Tokenize text
text = "Este es el texto para probar el laboratorio de base de datos 2 con el profesor Heider."
words = nltk.word_tokenize(text.lower())
print(words)

#Clean words
clean_words = words.copy()
stoplist = stopwords.words("spanish")
print(len(stoplist))

#Filter stopwords
with open('stop-words-spanish.txt') as file:
  stoplist = [line.lower().strip() for line in file]
stoplist += ['.','?','-','hola'] #Add manually stopwords to the list.

clean_words = words[:]
for token in words:
  if token in stoplist:
    clean_words.remove(token)

print(words)
print(clean_words)


#Reduce words to their root
stemmer = PorterStemmer()

words = ["program", "programs", "programmer", ]


# Snowball
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('spanish')
words = ['amor', 'amorcito', 'amores', 'amaras']
for w in words:
  print(w, '->', stemmer.stem(w))
