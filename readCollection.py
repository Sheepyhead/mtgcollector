import csv
import sys
from dataclasses import dataclass
from enum import Enum


class Condition(Enum):
    NM = "NM"
    LP = "LP"
    MP = "MP"
    HP = "HP"
    D = "D"
    UK = "UK"
    UNDEFINED = "Undefined"


def getProperty(row, propertyName, headers):
    "This gets the given property from the given row, if it exists"
    try:
        return row[headers.index(propertyName)]
    except IndexError:
        print("Property not found for row: [" + ", ".join(row) +
              "], property: " + propertyName + ", with headers: [" + ", ".join(headers) + "]")


def mapCondition(inputCondition):
    "This maps alternate condition names to local format"
    if (inputCondition == "Near Mint"):
        return Condition.NM
    if (inputCondition == "Mint"):
        return Condition.NM
    if (inputCondition == "Good (Lightly Played)"):
        return Condition.LP
    if (inputCondition == "Played"):
        return Condition.MP
    if (inputCondition == "Heavily Played"):
        return Condition.HP
    if (inputCondition == "Poor"):
        return Condition.D
    if (inputCondition == ""):
        return Condition.UK
    raise ValueError("Attempted to map unknown condition \"" +
                     inputCondition + "\"")


def mapEdition(inputEdition, editions):
    "Maps alternate edition names to three-letter acronym using editions.txt"

    rowList = []

    for editionMapping in editions:
        rowList.append("=".join(editionMapping))
        if inputEdition == editionMapping[0]:
            return editionMapping[1]

    raise ValueError("Attempted to map unknown edition: \"" +
                     inputEdition + "\"")


def readCollection(inputFile="input.csv", outputFile="output.csv"):
    "Converts a deckbox.org collection into my own format described in the readme"
    with open(inputFile, newline='\n') as collectionFile:
        with open(outputFile, 'w', newline='\n') as writeFile:
            with open("editions.txt") as editionsFile:
                collectionReader = csv.reader(collectionFile)
                headers = next(collectionReader, None)
                fileWriter = csv.writer(writeFile, delimiter=',')
                targetHeaders = ["Card Name", "Quantity", "Condition", "Set", "Foil",
                                 "Promo", "Language", "Price", "Last Changed", "Tradelist Quantity", "Notes"]
                fileWriter.writerow(targetHeaders)
                editionsReader = csv.reader(editionsFile, delimiter='=')
                editionsMap = []
                for edition in editionsReader:
                    editionsMap.append(edition)
                for row in collectionReader:
                    if len(row) == 0:
                        continue
                    newRow = [None] * 10
                    newRow[0] = getProperty(row, 'Name', headers)
                    newRow[1] = getProperty(row, 'Count', headers)
                    newRow[2] = mapCondition(getProperty(
                        row, 'Condition', headers)).value
                    newRow[3] = mapEdition(getProperty(
                        row, 'Edition', headers), editionsMap)
                    newRow[4] = 1 if getProperty(
                        row, 'Foil', headers) == "foil" else 0
                    newRow[5] = getProperty(row, "Language", headers)
                    newRow[6] = None
                    newRow[7] = getProperty(row, 'Last Updated', headers)
                    newRow[8] = getProperty(row, 'Tradelist Count', headers)
                    newRow[9] = None
                    fileWriter.writerow(newRow)

inputFile = "input.csv"
outputFile = "output.csv"
index = 0
for arg in sys.argv:
    if (arg == "" or index == 0):
        index += 1
        continue
    if (arg.find('=') > -1):
        splitArg = arg.split('=')
        if (splitArg[0] == "inputFile"):
            inputFile = splitArg[1]
        elif (splitArg[0] == "outputFile"):
            outputFile = splitArg[1]
    elif (index == 1):
        inputFile = arg
    elif (index == 2):
        outputFile = arg
    index += 1
if len(sys.argv) == 1:
    inputFile = input("Please type the name of the csv file to import: ")
    outputFile = input("Please type the name of the csv file to export to: ")

print("Reading collection from file \"" + inputFile + "\", writing collection to file \"" + outputFile + "\"")
try: 
    readCollection(inputFile, outputFile)
except FileNotFoundError as error:
    print(str(error).split(']')[1][1:]) # Remove the [Errno 2] part of the error message