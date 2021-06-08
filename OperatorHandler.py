from InvertedIndex import InvertedIndex
from nltk.stem.snowball import SnowballStemmer


class OperatorHandler:
    def __init__(self):
        self.index = InvertedIndex()

    def addBook(self, bookName, bookFileName):
        self.index.addBook(bookName, bookFileName)

    def recover(self, token):
        stemmer = SnowballStemmer('spanish')
        root_token = stemmer.stem(token)
        return self.index.recover(root_token)

    def OR(self, listA, listB):
        result = []
        i, j = (0,0)

        while i < len(listA) and j < len(listB):
            if listA[i] < listB[j]:
                result.append(listA[i])
                i+= 1
            elif listA[i] > listB[j]:
                result.append(listB[j])
                j+= 1
            else:
                result.append(listA[i])
                i += 1
                j += 1

        while i < len(listA):
            result.append(listA[i])
            i+= 1

        while j < len(listB):
            result.append(listB[j])
            j+= 1

        return result


    def AND(self, listA, listB):
        result = []
        i, j = (0, 0)
        
        while i < len(listA) and j < len(listB):
            if listA[i] < listB[j]:
                i += 1
            elif listA[i] > listB[j]:
                j += 1
            else:
                result.append(listA[i])
                i += 1
                j += 1
        return result


    def ANDNOT(self, listA, listB):
        result = []
        i, j = (0,0)

        while i < len(listA) and j < len(listB):
            if listA[i] < listB[j]:
                result.append(listA[i])
                i += 1
            elif  listA[i] > listB[j]:
                j += 1
            else:
                i += 1
                j += 1

        while i < len(listA):
            result.append(listA[i])
            i += 1

        return result