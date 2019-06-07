import csv
from readCollection import getProperty

basicLandNames = [ "Mountain", "Island", "Swamp", "Forest", "Plains"]

def getExcessQualifiers(cardEntry, headers):
    return \
        int(getProperty(cardEntry, "Quantity", headers)) > 4 \
        and not getProperty(cardEntry, "Set", headers).startswith("*") \
        and not getProperty(cardEntry, "Name", headers) in basicLandNames \
        and not getProperty(cardEntry, "Rarity", headers) == "BasicLand" \
        and not getProperty(cardEntry, "Foil", headers) == "1"
        


def findExcessCardsWorthLessThanOneDollar():
    with open("output.csv", "r") as collection:
        headers = None
        excessCards = []
        collectionReader = csv.reader(collection)
        for cardEntry in collectionReader:
            if headers == None:
                headers = cardEntry
                continue
            try:
                if getExcessQualifiers(cardEntry, headers) and float(getProperty(cardEntry, "Price", headers)) < 1.0:
                    cardEntry[1] = str(int(cardEntry[1]) - 4)
                    entryNumber = 0
                    for prop in cardEntry:
                        if "," in prop:
                            cardEntry[entryNumber] = '"' + prop + '"'
                        entryNumber += 1
                    excessCards.append(",".join(cardEntry))
            except ValueError as error:
                print('Failed to process row because of ' +
                      str(error) + '\n' + ", ".join(cardEntry))
        with open("excessCardsWorthLessThanOneDollar.csv", "w") as excessCardsFile:
            excessCardsFile.write(",".join(headers) + '\n')
            for cardEntry in excessCards:
                excessCardsFile.write(cardEntry + '\n')


def findExcessCards():
    with open("output.csv", "r") as collection:
        headers = None
        excessCards = []
        collectionReader = csv.reader(collection)
        for cardEntry in collectionReader:
            if headers == None:
                headers = cardEntry
                continue
            try:
                if int(getProperty(cardEntry, "Quantity", headers)) > 4 and not getProperty(cardEntry, "Set", headers).startswith("*"):
                    cardEntry[1] = str(int(cardEntry[1]) - 4)
                    entryNumber = 0
                    for prop in cardEntry:
                        if "," in prop:
                            cardEntry[entryNumber] = '"' + prop + '"'
                        entryNumber += 1
                    excessCards.append(",".join(cardEntry))
            except ValueError as error:
                print('Failed to process row because of ' +
                      str(error) + '\n' + ", ".join(cardEntry))
        with open("excessCards.csv", "w") as excessCardsFile:
            excessCardsFile.write(",".join(headers) + '\n')
            for cardEntry in excessCards:
                excessCardsFile.write(cardEntry + '\n')


def findValueOfSet(setFileName):
    with open(setFileName, "r") as collection:
        headers = None
        totalValue = 0.0
        numberOfCards = 0
        numberOfRares = 0
        numberOfMythics = 0
        collectionReader = csv.reader(collection)
        for cardEntry in collectionReader:
            if headers == None:
                headers
                headers = cardEntry
                continue
            try:
                totalValue += float(getProperty(cardEntry, "Price", headers)) * \
                    float(getProperty(cardEntry, "Quantity", headers))
                numberOfCards += int(getProperty(cardEntry,
                                                 "Quantity", headers))
                if "MythicRare" in getProperty(cardEntry, "Rarity", headers):
                    numberOfMythics += int(getProperty(cardEntry,
                                                       "Quantity", headers))
                elif "Rare" in getProperty(cardEntry, "Rarity", headers):
                    numberOfRares += int(getProperty(cardEntry,
                                                     "Quantity", headers))
            except Exception as error:
                print(str(error) + " card entry: " + ", ".join(cardEntry))
        print("Total value of " + setFileName + " is ${}, distributed on {} cards of which {} are rares and {} are mythics".format(
            str(totalValue), str(numberOfCards), str(numberOfRares), str(numberOfMythics)))


if __name__ == "__main__":
    findExcessCardsWorthLessThanOneDollar()
    findExcessCards()
    findValueOfSet("excessCardsWorthLessThanOneDollar.csv")
    findValueOfSet("excessCards.csv")
