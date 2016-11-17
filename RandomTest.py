import random
fileList = ['Quotes\BeatlesQuotes.txt', 'Quotes\MiscDisneyCharQuotes.txt', 'Quotes\MiscQuotes.txt', 'Quotes\WaltDisneyQuotes.txt'];


def ChooseQuoteFromFile(file):
        with open(file) as quoteFile:
                quote = quoteFile.read().splitlines()
                quote = random.choice(quote).partition("##")[0].partition("#")
                with open('Quotes\UsedQuotes.txt', 'a+') as usedQuoteFile:
                        if quote[0] in usedQuoteFile.read():
                                return(False)
                        else:
                                usedQuoteFile.seek(0, 2) #Because Windows sux
                                usedQuoteFile.write(quote[0])
                                return(quote[0], quote[2])
successCount = 0

while(1):
        failCount = 0
        successCount += 1
        quote = ChooseQuoteFromFile(random.choice(fileList))
        while not quote:
                quote = ChooseQuoteFromFile(random.choice(fileList))
                failCount += 1
                if failCount > 200:
                        print("100!")
                        print("Success: "+str(successCount))
                        raw_input()
        failCount = 0
        print(quote[0])
        print("\t-"+str(quote[1]))
