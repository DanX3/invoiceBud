import argparse

fixed_isbn = "9788808"
books = {}
# books["092832"] = 2
outfilename = 'books'

def addBook(isbn, quantity):
    if isbn in books:
        books[isbn] += quantity
    else:
        books[isbn] = quantity


def loadFile(filename):
    f = open(filename, 'r')
    for line in f:
        words = line.split()
        key = words[0]
        quantity = int(words[1])
        books[words[0]] = quantity
    return books


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

    if len(codes) != len(counts):
        print("Length of count and codes mismatches")
        return None
    else:
        print("Successfully matched {} books!".format(len(codes)))
        invoice = {}
        for i in range(0, len(codes)):
            invoice[codes[i]] = counts[i]
            print("{} {}".format(codes[i], counts[i]))
        return invoice

def exportBooks(books, filename):
        export = open(filename, 'w')
        for (key, value) in books.items():
            export.write("{} {}\n".format(key, value))
        export.close()


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--compare', action="store_true" )
args = parser.parse_args()
if args.compare:
    books = loadFile(outfilename)
    invoice = createInvoice()
    if invoice != None:
        exportBooks(books, 'booksExported')
        exportBooks(invoice, 'invoiceExported')
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
    elif command == 'new' or command == 'n' or command[0] == '9':
        # try to get the full ISBN

        try:
            addBook(int(command), 1)
        except(ValueError):
            quantity = 1
            try:
                if len(cmds) == 3:
                    quantity = int(cmds[2])
            except(ValueError):
                quantity = 1

            key = cmds[1]
            if len(key) != 6:
                print("Probably wrong ISBN, retry")
                continue
            
            addBook(fixed_isbn + key, quantity)

    elif command == 'save':
        f = open(outfilename, 'w')
        for (key, value) in books.items():
            f.write("{} {}\n".format(key, value))
        f.close()
    elif command == 'load':
        books = loadFile(outfilename)
    elif command == "count":
        counter = 0
        for (key, value) in books.items():
            counter += value
        print(counter)
    elif command == 'export':
        exportBooks('exported')
    elif command == 'quit' or 'exit':
        break
    else:
        print("Command not recognized")

