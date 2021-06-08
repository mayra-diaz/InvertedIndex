from OperatorHandler import OperatorHandler
from Parser import get_parser

h = OperatorHandler()
books = ['Gandalf', 'Frodo', 'Parth Galen', 'Mordor', 'Gandalf y Pippin', 'Cirith Ungol']

i = 1
for book in books:
    h.addBook(book, f'./books/libro{str(i)}.txt')
    i +=1

result = h.OR(h.AND(h.recover('frodo'), h.recover('comunidad')), h.recover('mordor'))
print(result)