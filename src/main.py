import os                                                              
import subprocess
import sys
import json


if len(sys.argv)!=2:
	print ("Usage python main.py $city-Name \nCity-Name should be hyphen(-) seperated if it is of more than one word, first word capitalised cased")
else:
	cityName = sys.argv[1]
	cityNameText = sys.argv[1].replace('-',' ')
	code =''
	#get city code
	os.chdir('citycode')
	json_data = open('citycode.json')
	data = json.load(json_data)
	for d in data:
		if d['city']==cityNameText:
			code = d['code']
	if(code==''):
		print "No such city found, please check with citycode.json or the usage\nUsage python main.py $city-Name \nCity-Name should be hyphen(-) seperated if it is of more than one word, first word capitalised cased"
	else:
		# link.py
		os.chdir('..\hotels')
		proc = subprocess.Popen('scrapy crawl link -o reviews.json',stdin=subprocess.PIPE,shell=True)
		proc.stdin.write(cityName+'_'+code)
		proc.stdin.close()
		retcode = proc.wait()
		# copy
		subprocess.call('copy sentiment.py ..\stanford-corenlp-full-2014-10-31', shell=True)
		subprocess.call('copy reviews.json ..\stanford-corenlp-full-2014-10-31', shell=True)
		subprocess.call('del reviews.json', shell=True)
		subprocess.call('md ..\\'+cityName, shell=True)

		# go to stanford
		os.chdir('..\stanford-corenlp-full-2014-10-31')
		proc4 = subprocess.Popen('python sentiment.py', shell=True)
		retcode4 = proc4.wait()
		# copy reviews
		subprocess.call('del sentiment.py',shell=True)
		subprocess.call('copy rate.csv ..\\'+cityName, shell=True)
		subprocess.call('copy rate.txt ..\\'+cityName, shell=True)
		subprocess.call('copy reviews.json ..\\'+cityName, shell=True)
		subprocess.call('del rate.csv',shell=True)
		subprocess.call('del rate.txt',shell=True)
		subprocess.call('del reviews.json',shell=True)
