import pygame
import requests
from pygame.locals import*
import random
import time

pygame.init()

oneShot = True

########################
##   PYGAME GLOBALS   ## 
######################## 
fontString_quote        = "Frenchscript"
fontSize_quote          = 40
fontString_time         = "Frenchscript"
fontSize_time           = 120
windowWidth             = 640
windowHeight            = 480
quoteFont               = pygame.font.SysFont(fontString_quote, fontSize_quote)
timeFont                = pygame.font.SysFont(fontString_time, fontSize_time)
mainLoopRunning         = True
leftSideBuffer          = 20
rightSideBuffer         = 20
screen = pygame.display.set_mode((windowWidth, windowHeight))

white      = (255, 255, 255)
black      = (0,0,0)
red        = (255, 0, 0)
green      = (0, 255, 0)
blue       = (0, 0, 255)


#############################
##   WEATHER API GLOBALS   ## 
#############################
apiKey              = '990fcb6fd80b09ec27085720df721f3c'
weatherCity         = "Starkville"
weatherAddress      = "http://api.openweathermap.org/data/2.5/weather?q="+weatherCity+"&APPID="+apiKey
timeZoneOffset      = 5
cloudCoverIdx       = 1

#############################
##   QUOTE FILES GLOBALS   ##
#############################
quoteFileList      = ['Quotes\BeatlesQuotes.txt', 'Quotes\MiscDisneyCharQuotes.txt', 'Quotes\MiscQuotes.txt', 'Quotes\WaltDisneyQuotes.txt'];
slicedQuote        = []

###############################
##   WEATHER API FUNCTIONS   ## 
###############################
#Return --> [<requested status as string>]
def GetWeatherStatus(address, status):
		weatherStatusMaster = requests.get(address)
		if status == "sky":
				return(weatherStatusMaster.json()['weather'][0]['main'])
		elif status == "temp":
				return(weatherStatusMaster.json()['main']['temp'])
		elif status == "cloudCover":
				return(weatherStatusMaster.json()['clouds']['all'])
		elif status == "sunset":
				return(weatherStatusMaster.json()['sys']['sunset'])
		elif status == "sunrise":
				return(weatherStatusMaster.json()['sys']['sunrise'])


#Return --> [addressOfWeatherIcon, cloudCoverDescription]
def GetWeatherIcon(cloudCover, time=None, sunrise=None, sunset=None):
		day = False
		night = False
		if time >= sunrise and time <= sunset:
				day = True
				night = False
		elif time >= sunset and time <= sunrise:
				day = False
				night = True
		if day:
				if cloudCover < 25:
						cloudCoverDescription = "clear"
						weatherIcon = "WeatherIcons\\ClearSun.png"

				elif cloudCover >= 25 and cloudCover < 50:
						cloudCoverDescription = "partly cloudy"
						weatherIcon = "WeatherIcons\\PartlyCloudySun.png"

				elif cloudCover >= 50 and cloudCover < 75:
						cloudCoverDescription = "mostly cloudy"
						weatherIcon = "WeatherIcons\\PartlyCloudySun.png"

				elif cloudCover >= 75:
						cloudCoverDescription = "very cloudy"
						weatherIcon = "WeatherIcons\\MostlyCloudy.png"
		elif night:
				if cloudCover < 25:
						cloudCoverDescription = "clear"
						weatherIcon = "WeatherIcons\\ClearMoon.png"

				elif cloudCover >= 25 and cloudCover < 50:
						cloudCoverDescription = "partly cloudy"
						weatherIcon = "WeatherIcons\\PartlyCloudyMoon.png"

				elif cloudCover >= 50 and cloudCover < 75:
						cloudCoverDescription = "mostly cloudy"
						weatherIcon = "WeatherIcons\\PartlyCloudyMoon.png"

				elif cloudCover >= 75:
						cloudCoverDescription = "very cloudy"
						weatherIcon = "WeatherIcons\\MostlyCloudy.png"

		return(weatherIcon, cloudCoverDescription)

#Return --> TemperatureInFahrenheit(int)[default]
def ConvertKelvinToFahrenheit(tempInKelvin, castAsInt=True):
		if castAsInt:
				return(int((1.8*tempInKelvin)-459.67))
		else:
				return((1.8*tempInKelvin)-459.67)


###############################
##   QUOTE FILES FUNCTIONS   ## 
###############################
#Return --> [RandomQuote, AuthorOfRandomQuote]
def GetRandomQuoteFromFile(fileToAccess):
		with open(fileToAccess) as quoteFile:
				quote = quoteFile.read().splitlines()
				quote = random.choice(quote).partition("##")[0].partition("#")
				with open('Quotes\\UsedQuotes.txt', 'a+') as usedQuoteFile:
						if quote[0] in usedQuoteFile.read():
								return(quote[0], quote[2])
						else:
								usedQuoteFile.seek(0, 2) #Because Windows sux
								usedQuoteFile.write(quote[0])
								return(quote[0], quote[2])


##########################
##   PYGAME Functions   ## 
##########################
#Return--> [SlicedQuote, foundEndOfString(bool), indexOfLastSpaceFound]
def SliceQuote(fullQuote, newSize, prevIdx=0):
		idx = prevIdx
		idxOfLastSpaceFound = 0
		foundEndOfString = False
		while quoteFont.size(fullQuote[0][prevIdx:idx])[0] < (windowWidth - leftSideBuffer - rightSideBuffer) and idx < len(fullQuote[0]):
				if fullQuote[0][idx] == " ":
						idxOfLastSpaceFound = idx
				idx += 1
		if idx >= len(fullQuote[0]):
				foundEndOfString = True
				return([fullQuote[0][prevIdx:], foundEndOfString, idxOfLastSpaceFound+1])
		return([fullQuote[0][prevIdx:idxOfLastSpaceFound], foundEndOfString, idxOfLastSpaceFound+1])


def RetrieveAndSliceQuote():
    global fontSize_quote
    global quoteFont
    fontTooLarge = True
    unslicedQuote = GetRandomQuoteFromFile(random.choice(quoteFileList))
    fontSize_quote = 40     #This is the default value
    while fontTooLarge:
        #raw_input()
        slicedQuote = []
        fontTooLarge = False
        result = SliceQuote(unslicedQuote, False)
        slicedQuote.append(result[0])
        while not result[1]:
            result = SliceQuote(unslicedQuote, False, result[2])
            slicedQuote.append(result[0])
        #len(slicedQuote) = number of lines the quote has been broken in to
        #quoteFont.size(unslicedQuote[0])[1] is the vertical height of the font
        if len(slicedQuote)*quoteFont.size(unslicedQuote[0])[1] > (windowHeight/4 - 20):
            #print("Quote too long!")
            #print("Length of quote: "+str(len(slicedQuote)))
            #print("Height of quote: "+str(quoteFont.size(unslicedQuote[0])[1]))
            #print("Product:         "+str(len(slicedQuote)*quoteFont.size(unslicedQuote[0])[1]))
            #print("Space allotted:  "+str((windowHeight/4 - 20)))
            #print("Quote: "+str(slicedQuote))
            fontSize_quote -= 1
            quoteFont = pygame.font.SysFont(fontString_quote, fontSize_quote)
            fontTooLarge = True
            if fontSize_quote == 0:
                print("Error! Quote too long to fit on screen!")
                break
    return([slicedQuote, unslicedQuote[1]])

def DisplayQuote(screen, slicedQuote, location):
		if location == "top":
				for i in range(len(slicedQuote[0])):
						screen.blit(quoteFont.render(slicedQuote[0][i], True, black), (20, i*quoteFont.size(slicedQuote[0][i])[1]))
				screen.blit(quoteFont.render(slicedQuote[1], True, black), (windowWidth-40-quoteFont.size(slicedQuote[1])[0], (i+1)*quoteFont.size(slicedQuote[0][i])[1]))
		elif location == "bottom":
				for i in range(len(slicedQuote[0])):
						screen.blit(quoteFont.render(slicedQuote[0][i], True, black), (20, windowHeight-(((len(slicedQuote)-i))*quoteFont.size(slicedQuote[0][i])[1])-quoteFont.size(slicedQuote[1])[1]))
				screen.blit(quoteFont.render(slicedQuote[1], True, black), (windowWidth-40-quoteFont.size(slicedQuote[1])[0], windowHeight-quoteFont.size(slicedQuote[0][i])[1]))

def UpdateTime():
    return(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)

weatherStatus = [GetWeatherStatus(weatherAddress, "sky"), GetWeatherStatus(weatherAddress, "temperature")]
weatherIcon = GetWeatherIcon(weatherStatus[0])
#print(RetrieveAndSliceQuote())
slicedQuote = RetrieveAndSliceQuote()
print(slicedQuote)
print(slicedQuote[1])
#allFonts = pygame.font.get_fonts()
#print(allFonts)
#print(allFonts[45])
#print(len(allFonts))
currentTime = UpdateTime()
tempTime = [-1, -1, -1]
while mainLoopRunning:
    if not oneShot:
        print("Functionality not implemented yet")
        mainLoopRunning = False
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                mainLoopRunning = False
        screen.fill(white)




        DisplayQuote(screen, slicedQuote, "bottom")

        pygameWeatherIcon = pygame.image.load(weatherIcon[0])
        screen.blit(pygameWeatherIcon, (0.6*windowWidth, 0.1*windowHeight))

        tempTime = UpdateTime()
        if tempTime != currentTime:
            currentTime = tempTime
            print(timeFont.size(timeString)[0])
        timeString = str(currentTime[0])+":"+str(currentTime[1])+":"+str(currentTime[2])

        screen.blit(timeFont.render(timeString, True, black), (50, -40))

        pygame.display.flip()

        """
        for i in range(len(allFonts)):
                if i % 12 == 0:
                        pygame.display.flip()
                        raw_input()
                        screen.fill(white)
                if i == 45:
                        i = 46
                quoteFont = pygame.font.SysFont(allFonts[i], 30)
                screen.blit(quoteFont.render("text", True, (0,0,0)), (20,40*i))
                del quoteFont
        """

pygame.quit()
