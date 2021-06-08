import os
import json
import nltk
import atexit
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')
# from nltk.corpus import stoptokens
# nltk.download('stoptokens')

class InvertedIndex:
  def __init__(self, indexFile='./data/InvertedIndex.json', booksFile='./data/Books.txt'):
    self.indexFile = indexFile
    self.booksFile = booksFile
    self.stopWordsFile = './stopWords/stop-words-spanish.txt'
    self.frequentTokensFile = './data/FrequentTokens.txt'
    self.index = {}
    self.books={}
    self.frequentTokens = []
    self.readIndexFile()
    self.readBooksFile()
    self.readFrequentTokensFile()
    atexit.register(self.cleanup)

  def readIndexFile(self):
    if os.path.exists('./'+self.indexFile):
      with open(self.indexFile, 'r') as file:
        self.index = json.load(file)
    else:
      f = open(self.indexFile, 'x')
      f.close()
  
  def readBooksFile(self):
    if os.path.exists('./'+self.booksFile):
      with open(self.booksFile) as file:
        i = 0
        for book in file:
          self.books[book[:-1]]=i
          i +=1
    else:
      f = open(self.booksFile, 'x')
      f.close()

  def readFrequentTokensFile(self):
    if os.path.exists('./'+self.frequentTokensFile):
      with open(self.frequentTokensFile) as file:
        for token in file:
          self.frequentTokens.append(token[:-1])
    else:
      f = open(self.frequentTokensFile, 'x')
      f.close()

  def cleanup(self):
    self.writeIndexJson()
    self.writeFrequentTokens()

  def writeIndexJson(self):
    file = open(self.indexFile, 'w')
    file.write(json.dumps(self.index))
    file.close()

  def writeFrequentTokens(self):
    file = open(self.frequentTokensFile, 'w')
    for token in self.frequentTokens:
      file.write(token+'\n')
    file.close()

  def writeBook(self, bookName):
    self.books[bookName] = len(self.books)
    with open(self.booksFile, 'a') as file:
      file.write(f'{bookName}\n')

  def getFileText(self, fileName):
    with open(fileName) as file:
      return [line.lower().strip() for line in file]


  def preProcess(self, text):
    tokens = []
    # Tokenizar el texto
    for line in text:
      tokens += nltk.word_tokenize(line.lower())
    # Retirar signos innecesarios
    with open('symbols.txt') as file:
      symbol_list = [line.lower().strip() for line in file]
    for word in tokens:
      if word in symbol_list:
        tokens.remove(word)
        
    #Filtrar stoptokens
    clean_tokens = []
    with open(self.stopWordsFile) as file:
      stoplist = [line.lower().strip() for line in file]
    for token in tokens:
      if not token in stoplist:
        clean_tokens.append(token)
        
    # Reducir palabras a su raiz
    stemmer = SnowballStemmer('spanish')
    root_tokens = []
    for word in clean_tokens:
      root_tokens.append(stemmer.stem(word))
    #print(f'root_tokens: {root_tokens}')
    return root_tokens


  def addBookTokens(self, bookId, tokens):
    for token in tokens:
      if token in self.index:
        self.index[token][0] += 1
        if bookId in self.index[token][1]:
          self.index[token][1][bookId] += 1 
        else:
          self.index[token][1][bookId] = 1
      else:
        self.index[token] = [1, {bookId: 1}]
  
  def setFrequentTokens(self):
    self.index = dict(sorted(self.index.items(), key=lambda x: x[1][0], reverse=True))
    self.frequentTokens = sorted(list(self.index.keys()))[:500]
  
  def addBook(self, bookName, bookFileName):
    if bookName in self.books:
      return
    self.writeBook(bookName)
    text = self.getFileText(bookFileName)
    tokens = self.preProcess(text)
    self.addBookTokens(self.books[bookName], tokens)
    self.setFrequentTokens()

  def recover(self, token): #L()
    if token in self.frequentTokens: 
      return list(self.index[token][1].keys())
    raise Exception("Token not found in top 500 tokens.")

  def printTokens(self):
    print(self.index)
