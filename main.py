import argparse

books = {}
# books["092832"] = 2
outfilename = 'books'

def addBook(isbn, quantity):
    if isbn in books:
        books[isbn] += quantity
    else:
        books[isbn] = quantity


def loadFile(filename):
    try:
        f = open(filename, 'r')
        for line in f:
            words = line.split()
            key = words[0]
            quantity = int(words[1])
            books[words[0]] = quantity
        return books
    except(FileNotFoundError):
        return {}


def createInvoice():
    codes = []
    counts = []
    codefile = open("invoice/codes/out.txt")
    countfile = open("invoice/counts/out.txt")

    for code in codefile:
        codes.append(int(code))
    codefile.close()

    for count in countfile:
        counts.append(int(count))
    countfile.close()

    invoice = {}
    if len(codes) != len(counts):
        print("Length of count({}) and codes({}) mismatches".format(
            len(codes), len(counts)))
        for i in range(0, len(codes)):
            invoice[codes[i]] = 1
    else:
        print("Successfully matched {} books!".format(len(codes)))
        for i in range(0, len(codes)):
            invoice[codes[i]] = counts[i]
    return invoice

def exportBooks(books, filename):
        export = open(filename, 'w')
        catalog = createCatalog()
        exported = {}
        for (key, value) in books.items():
            if key in catalog:
                bookdata = catalog[key]
                if bookdata[2] in exported:
                    exported[bookdata[2]].append(bookdata)
                else:
                    exported[bookdata[2]] = [bookdata]
                # export.write("{:25} {:14s} {:2d} {}\n".format(bookdata[2], key, value, bookdata[1]))
            else:
                export.write("{} {}\n".format(key, value))

        keys = []
        for (key, value) in exported.items():
            keys.append(key)
        keys.sort()

        for (key, value) in exported.items():
            print(exported[key])
            exported[key].sort(key=lambda entry: entry[1])
                
        for key in keys:
            samePublishedBooks = exported[key]
            for book in samePublishedBooks:
                export.write("{:25} {:14s} {:2d} {}\n".format(book[2], book[0],
                    books[book[0]], book[1]))

        export.close()

def createCatalog():
    catalog = {}
    catalogfile = open('TestiFinal.txt', 'r')
    for line in catalogfile:
        words = line.split('|')
        catalog[words[0]] = words
    return catalog
        

def getFromCatalog(isbn):
    catalogfile = open('TestiFinal.txt', 'r')
    for line in catalogfile:
        values = line.split('|')
        if values[0] == isbn:
            return values
    return []

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--compare', action="store_true" )
parser.add_argument('--book', type=str)
args = parser.parse_args()
if args.compare:
    books = loadFile(outfilename)
    if len(books) == 0:
        print("No load file found")
        exit()
    invoice = createInvoice()
    if len(invoice) != 0:
        exportBooks(books, 'booksExported')
        exportBooks(invoice, 'invoiceExported')
    print("Exported {} books from invoice".format(len(invoice)))
    exit()

if args.book:
    bookFound = getFromCatalog(args.book) 
    if bookFound:
        print(bookFound)
    else:
        print("No book found")
    exit()

    

while True:
    a = input("> ")
    cmds = a.split(" ")
    command = cmds[0]

    if len(cmds) == 0 or cmds[0] == "":
        continue
    elif command == "ls":
        for (key, value) in books.items():
            print(key, value)
    # possible matches are
    # {new,n} <count> <isbn>
    # <isbn>
    # {new,n} <isbn>
    elif command == 'new' or command == 'n' or command[0] == '9':
        if command[0] == '9':
            # try to get the full ISBN
            addBook(command, 1)
        else:
            # go with new command syntax
            quantity = 1
            if len(cmds) == 3:
                quantity = int(cmds[1])
                key = cmds[2]
            else:
                key = cmds[1]

            addBook(key, quantity)

    elif command == 'save':
        f = open(outfilename, 'w')
        for (key, value) in books.items():
            f.write("{} {}\n".format(key, value))
        f.close()
    elif command == 'load':
        books = loadFile(outfilename)
        if len(books) == 0:
            print("No load file found")
    elif command == "count":
        counter = 0
        for (key, value) in books.items():
            counter += value
        print(counter)
    elif command == 'export' or command == 'exp':
        exportBooks(books, 'exported')
    elif command == 'quit' or 'exit':
        break
    else:
        print("Command not recognized")

