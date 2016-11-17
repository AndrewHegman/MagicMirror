import pygame
import requests
from pygame.locals import*
import random

##pygame.init()
#myfont = pygame.font.SysFont("monospace", 15)
##font = pygame.font.SysFont("monospace", 60)

##fileList = ['Quotes\BeatlesQuotes.txt', 'Quotes\MiscDisneyCharQuotes.txt', 'Quotes\MiscQuotes.txt', 'Quotes\WaltDisneyQuotes.txt'];
##white = (255, 255, 255)
##w = 640
##h = 480
screen = pygame.display.set_mode((w, h))
screen.fill((white))
##running = 1

##APIKEY = '990fcb6fd80b09ec27085720df721f3c'
#CITY = raw_input("City: ")
##CITY = "Memphis"
##ADDRESS = "http://api.openweathermap.org/data/2.5/weather?q="+CITY+"&APPID="+APIKEY
##r = requests.get(ADDRESS)
skyStatus = r.json()['weather'][0]['main']
currentTemp = r.json()['main']['temp']
cloudCover = r.json()['clouds']['all']
#GetCloudIcon(cloudCover)

def GetCloudIcon(cloudCover):
	if cloudCover < 25:
		#print("Clear sky")
		cloudCoverStr = "clear"
		weatherIcon = "WeatherIcons\ClearSun.png"
	elif cloudCover >= 25 and cloudCover < 50:
		#print("Partly cloudy")
		cloudCoverStr = "partly cloudy"
		weatherIcon = "WeatherIcons\PartlyCloudySun.png"
	elif cloudCover >= 50 and cloudCover < 75:
		#print("Mostly cloudy")
		cloudCoverStr = "mostly cloudy"
		weatherIcon = "WeatherIcons\PartlyCloudySun.png"
	elif cloudCover >= 75:
		#print("Very cloudy")
		cloudCoverStr = "very cloudy"
		weatherIcon = "WeatherIcons\MostlyCloudy.png"
	return(weatherIcon)

#print("Current temperature is "+str(int((1.8*currentTemp)-459.67))+"F with "+cloudCoverStr+" skies")

def ChooseQuoteFromFile(file):
	with open(file) as quoteFile:
		quote = quoteFile.read().splitlines()
		quote = random.choice(quote).partition("##")[0].partition("#")
		with open('Quotes\UsedQuotes.txt', 'a+') as usedQuoteFile:
			if quote[0] in usedQuoteFile.read():
				return(quote[0], quote[2])
			else:
				usedQuoteFile.seek(0, 2) #Because Windows sux
				usedQuoteFile.write(quote[0])
				return(quote[0], quote[2])



def DrawText(text, prevIdx=0):
        idx = prevIdx
        idxOfLastSpace = 0
        foundEndOfString = False
        while font.size(text[0][prevIdx:idx])[0] < (w-20-20) and idx < len(text[0]):
                if text[0][idx] == " ":
                        idxOfLastSpace = idx
                idx += 1
                
        if idx >= len(text[0]):
                foundEndOfString = True
                return([text[0][prevIdx:], foundEndOfString, idxOfLastSpace+1])
        return([text[0][prevIdx:idxOfLastSpace], foundEndOfString, idxOfLastSpace+1])
                

quote = ["This is a really really long string, hopefully it will be long enough", "f"]
#quote = ["Short string", "F"]

quoteArray = []
result = DrawText(quote)
quoteArray.append(result[0])
print(len(quote[0]))
print(result)
while not result[1]:
        result = DrawText(quote, result[2])
        quoteArray.append(result[0])
        print(result)

print(quoteArray)
GetCloudIcon(cloudCover)

#quote = ChooseQuoteFromFile(random.choice(fileList))


        
#text = font.render(quote[0], True, (0,0,0))
while running:
	
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
	weatherIcon = GetCloudIcon(r.json()['clouds']['all'])
	#r.json()['clouds']['all']
	img = pygame.image.load(weatherIcon)
	screen.fill((white))
	#screen.blit(img,(0,0))
	for i in range(len(quoteArray)):
		screen.blit(font.render(quoteArray[i], True, (0,0,0)), (20,i*font.size(quoteArray[i])[1]))
	pygame.display.flip()
pygame.quit()



