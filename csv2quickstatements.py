#!/usr/bin/python3.4
# -*-coding:utf-8 -*
# This code is released under WTFPL Version 2 (http://www.wtfpl.net/)

"""Transforms a (specific for now) CSV file into a bunch of Wikidata element statements that can be feed to http://tools.wmflabs.org/wikidata-todo/quick_statements.php"""

"""Syntax sample: 
Q4115189 TAB P31 TAB Q1 TAB P580 TAB +00000001840-01-01T00:00:00Z/11 TAB S143 TAB Q48183

("Sandbox item" is an "instance of" "universe", qualifier "start date"=1840, sourced as "imported from" "German Wikipedia")"""

import csv

def readCSVFile(filename,sortKey):
	"""Lit le fichier source et retourne le résultat sous forme d'un dictionnaire d'éléments indexés d'après la première colonne."""
	reader = csv.DictReader(open(filename))
	result = {}
	for row in reader:
		key = row.pop(sortKey)
		if key in result:
			# implement your duplicate row handling here
			pass
		result[key] = row
	return result

def constructLine(theElement,sourceProperty="",sourceValue=""):
	
	returnString=""

	for key,value in theElement.items():
		elements=[]

		if not theElement['qID']:
			theElement['qID'] = "QIDàdéfinir"

		if "|" in key:
			#On ne parcourt que les clefs comportant un numéro de propriété
			theProperty=key.split("|")
			theProperty=theProperty[0].upper()

			theValue=""
			if "|" in value:
				theValue=value.split("|")
				theValue=theValue[0].upper()
			else:
				theValue=value

			# qualifiers
			theQualifiers=[]
			if theProperty == "P528":
				# If catalog number, specify the catalog. TODO: make it more generic
				theQualifiers.append("P972")
				theQualifiers.append("Q17438869")


			# append to the elements list and transform to a string.

			if theProperty and theValue:
				#We only construct a line if both the property and its value are not empty
				elements.append(theElement['qID'])
				elements.append(theProperty)
				elements.append(theValue)

				if theQualifiers:
					for i in theQualifiers:
						elements.append(i)

				if sourceProperty and sourceValue:
					elements.append(sourceProperty)
					elements.append(sourceValue)

				returnString += "	".join(elements) + "\n"

	return returnString








bodyList = readCSVFile("serenityverse_bodies.csv",'Astre')
#print (next (iter (bodyList.keys())))
#print (next (iter (bodyList.values())))

#constructLine(next (iter (bodyList.values())),"S143","Q17438869")

fullString=""
for i in bodyList.values():
	fullString +=constructLine(i,"S143","Q17438869")

print(fullString)