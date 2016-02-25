import json
import csv
import subprocess
import sys
from pyparsing import *
from compiler.ast import flatten
errorCount=0

# Takes pyparsed string nested array and returns the string inside it.
def nodeStr(r):
	
	return ' '.join(x for x in flatten(r) if not x.isdigit())

# Takes a string and returns the number of features it has (in array form)
def getNumFeatures(s):

	#Array value
	#1
	locArr = ["location","position","place","property","situation","site","locality","locale","spot","whereabouts","whereabout","scene","setting","area","environment","venue","address","view","sight","beach"]

	#2
	roomArr = ["rooms","beds","matress","bed","blanket","furniture","window","room","toilet","washroom","sofa","windows","bath","door","air-conditioning","ac"]

	#3
	foodArr = ["breakfast","food","dinner","lunch","restaurant","drinks","buffet"]

	#4
	serviceArr = ["room service","service","reception","staff","receptionist","room-service"]

	#5
	cleanArr = ["clean","cleanliness","fresh","freshness","sanitation","neat","neatness","dirt","dirty","dust","dusty","cleaning"]

	# general array -> is not evaluated, just for classification
	#6
	generalArr = ["hotel","hotels","resort","resorts","house","guesthouse","inn","motel"]

	featuresArray =[]
	sar = s.split('.')
	for review in sar:
		if review:
			if(any(x in review for x in locArr)):
				featuresArray.append(1)
	for review in sar:
		if review:
			if(any(x in review for x in roomArr)):
				featuresArray.append(2)
	for review in sar:
		if review:
			if(any(x in review for x in foodArr)):
				featuresArray.append(3)
	for review in sar:
		if review:
			if(any(x in review for x in serviceArr)):
				featuresArray.append(4)
	for review in sar:
		if review:
			if(any(x in review for x in cleanArr)):
				featuresArray.append(5)
	for review in sar:
		if review:
			if(any(x in review for x in generalArr)):
				featuresArray.append(6)
	return featuresArray

# returns pyparsed nested string array for given string.
def getParseString(s):
	enclosed = Forward()
	nestedParens = nestedExpr('(', ')', content=enclosed) 
	enclosed << (Word(alphanums+'.') | ',' | nestedParens)
	return enclosed.parseString(s).asList()
	
# returns dictionary specifying features and corresponding node from the parsed sentiment tree, if any
def getFeatureNodeList(s):
	totalR = getParseString(s)
	fatherR = totalR
	tempR = totalR[0]
	numSingleFeature = 0
	numTotalFeature = len(getNumFeatures(nodeStr(totalR)))
	numPreviousFeature = numTotalFeature
	featureNodeList = {0 : [0], 1 : [], 2 : [], 3 : [], 4 : [], 5 : []}
	while 1:
		try:
			numFeatures = len(getNumFeatures(nodeStr(tempR)))
			if(numPreviousFeature-numFeatures > 1):
				raise Exception("Two feature in one phrase")
			if(numFeatures==0):
				break
			elif (numFeatures==1):
				for x in getNumFeatures(nodeStr(tempR)):
					if x!=6:
						featureNodeList[x].append(int(tempR[0]))
				tempR = fatherR[2]
				numSingleFeature += 1
				if(numSingleFeature==numTotalFeature):
					break
			else:
				fatherR = tempR
				tempR=tempR[1]
			# print('\n')
		except Exception as e:
			errorCount+=1
			# print ('Feature-Aspect Based method failed. Try normal ') #debug
			# print e
			# print getNumFeatures(nodeStr(totalR))
			for x in getNumFeatures(nodeStr(totalR)):
				if x!=6:
					featureNodeList[x].append(0)
			break
	return featureNodeList


with open("reviews.json") as json_file:		#Edit here -> write file name
	city = json.load(json_file)
	i=0
	fp = csv.writer(open("rate.csv", "wb+"))		#Edit here -> output file name
	fp.writerow(["title","location","region","stars","amenities","start price","end price","total normalised rating","total rating","total count","total very positive rating count","total positive rating count","total negative rating count","total very negative rating count","total very positive reviews","total positive reviews","total negative reviews","total very negative reviews","location rating","location count","location very positive rating count","location positive rating count","location negative rating count","location very negative rating count","location very positive reviews","location positive reviews","location negative reviews","location very negative reviews","room rating","room count","room very positive rating count","room positive rating count","room negative rating count","room very negative rating count","room very positive reviews","room positive reviews","room negative reviews","room very negative reviews","food rating","food count","food very positive rating count","food positive rating count","food negative rating count","food very negative rating count","food very positive reviews","food positive reviews","food negative reviews","food very negative reviews","service rating","service count","service very positive rating count","service positive rating count","service negative rating count","service very negative rating count","service very positive reviews","service positive reviews","service negative reviews","service very negative reviews","cleanliness rating","cleanliness count","cleanliness very positive rating count","cleanliness positive rating count","cleanliness negative rating count","cleanliness very negative rating count","cleanliness very positive reviews","cleanliness positive reviews","cleanliness negative reviews","cleanliness very negative reviews"])
	# ,"count","error percentage"
	while i in range(len(city)):
		featureCount = {0: 0, 1:0, 2:0, 3:0, 4:0, 5:0}
		featureRate = {0: 0, 1:0, 2:0, 3:0, 4:0, 5:0}
		# featureSwitch = {0: 'General', 1: 'Location', 2: 'Room', 3: 'food', 4: 'Service', 5: 'Cleanliness'}		#Debug
		featureVPA = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
		featurePA = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
		featureNA = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
		featureVNA = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
		featureVPC = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
		featurePC = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
		featureNC = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
		featureVNC = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
		ratetotalsum=0
		ratetotalcount=0
		count = 0
		reviews = city[i]["tripadvisorR"]+[" . "]+city[i]["holidayiqR"]
		Rstr = ''.join(reviews)
		RarrayT = Rstr.split('.')
		Rarray = [x.encode('utf-8').strip().lower().translate(None,'`:[]|!/(){}-+=1234567890<>_\"\'') for x in RarrayT if x !='']
		Rarray = filter(None,Rarray)
		for reviewString in Rarray:
			if reviewString:
				# All
				proc = subprocess.Popen(
				    'java -cp "*" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -stdin -output probabilities',stdout=subprocess.PIPE,
				    stdin=subprocess.PIPE, shell=True)
				proc.stdin.write(reviewString)
				proc.stdin.close()
				result = proc.stdout.read()
				results = result.replace('\r',' ').strip().split('\n')
				try:
					count +=1
					for key,val in getFeatureNodeList(results[0]).items():
						if val:
							tempScore = [x for x  in results[val[0]+1].strip().split(' ') if x][1:]
							score = float(tempScore[0])*1+float(tempScore[1])*3.25+float(tempScore[2])*5.5+float(tempScore[3])*7.75+float(tempScore[4])*10
							featureCount[key]+=1
							featureRate[key]+=score
							stringParsed =  nodeStr(getParseString(results[0]))
							if (score>6.0 or score<5.0):
								ratetotalcount+=1
								ratetotalsum+=score
							if(score>7.75):
								featureVPA[key].append(stringParsed)
								featureVPC[key] += 1
							elif (score>5.5):
								featurePA[key].append(stringParsed)
								featurePC[key] += 1
							elif (score>3.25):
								featureNA[key].append(stringParsed)
								featureNC[key] += 1
							else:
								featureVNA[key].append(stringParsed)
								featureVNC[key] += 1
				except:
					errorCount +=1
		if count!=0:
			errorP = errorCount/count
		else:
			errorP=0
		rateTS = ratetotalsum/ratetotalcount if ratetotalcount!=0 else 'NA'
		rateT = featureRate[0]/featureCount[0] if featureCount[0]!=0 else 'NA'
		rateL = featureRate[1]/featureCount[1] if featureCount[1]!=0 else 'NA'
		rateR = featureRate[2]/featureCount[2] if featureCount[2]!=0 else 'NA'
		rateF = featureRate[3]/featureCount[3] if featureCount[3]!=0 else 'NA'
		rateS = featureRate[4]/featureCount[4] if featureCount[4]!=0 else 'NA'
		rateC = featureRate[5]/featureCount[5] if featureCount[5]!=0 else 'NA'


		
		region = city[i]["location"].split(',')
		if len(region)>2:
			region = region[-3]
		elif len(region)>1:
			region = region[-2]
		else:
			region ='NA'
		if not region:
			region="NA"
		aStr = ', '.join(city[i]["amenities"][1::2]).replace('\n','')
		if city[i]["price"]:
			a=[x.encode('UTF8') for x in city[i]["price"]][0].split('-')
			b = [x.strip()[3:].replace(',','') for x in a]
		else:
			b=['NA','NA']
		if city[i]["stars"]:
			starsString = city[i]["stars"][1].encode('utf-8').strip().split()[0]
		else:
			starsString ='NA'
		if city[i]["location"]:
			locString = city[i]["location"]
		else:
			locString='NA'
		fp.writerow([city[i]["title"],locString,region,starsString,aStr,b[0],b[1],rateTS,rateT,featureCount[0],featureVPC[0],featurePC[0],featureNC[0],featureVNC[0],featureVPA[0],featurePA[0],featureNA[0],featureVNA[0],rateL,featureCount[1],featureVPC[1],featurePC[1],featureNC[1],featureVNC[1],featureVPA[1],featurePA[1],featureNA[1],featureVNA[1],rateR,featureCount[2],featureVPC[2],featurePC[2],featureNC[2],featureVNC[2],featureVPA[2],featurePA[2],featureNA[2],featureVNA[2],rateF,featureCount[3],featureVPC[3],featurePC[3],featureNC[3],featureVNC[3],featureVPA[3],featurePA[3],featureNA[3],featureVNA[3],rateS,featureCount[4],featureVPC[4],featurePC[4],featureNC[4],featureVNC[4],featureVPA[4],featurePA[4],featureNA[4],featureVNA[4],rateC,featureCount[5],featureVPC[5],featurePC[5],featureNC[5],featureVNC[5],featureVPA[5],featurePA[5],featureNA[5],featureVNA[5]])
		# ,count,errorP

		with open("rate.txt", "w") as outfile:
			json.dump({'title': city[i]["title"], 'location':locString, 'region':region, 'star rating':starsString, 'amenities':aStr, 'start price':b[0], 'end price':b[1], 'normalised total rating':rateTS, 'total rating':rateT, 'number of total rating':featureCount[0], 'location rating':rateL, 'number of location rating':featureCount[1], 'room rating':rateR, 'number of room rating':featureCount[2], 'food rating':rateF, 'number of food rating':featureCount[3], 'service rating':rateS, 'number of service rating':featureCount[4], ' cleanliness rating':rateC, 'number of  cleanliness rating':featureCount[5], }, outfile, indent=4)

		i=i+1 #debug for single loop
		# break #debug for single loop