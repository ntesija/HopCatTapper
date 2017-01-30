from bs4 import BeautifulSoup
import urllib2, random
import xlsxwriter

print "\nHopCat Tapper created by Nicholas Tesija\n"
print "For location formats please visit https://hopcat.com and choose a location. \nThe string following 'hopcat.com' will be submitted below\n"

location = raw_input("Please enter a location (ex. ann-arbor, east-lansing): ")

gettingFilename = True
while gettingFilename:
	fileName = raw_input("Please enter a filename for the spreadsheet: ")
	if len(fileName) > 0:
		break
	print "\nFilename cannot be blank\n"

#beerData = [ [name, price, ABV, Volume, type, color (for chart)] ]
beerData = []

response = urllib2.urlopen('https://hopcat.com/beer/{}'.format(location))
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

for link in soup.find_all('div', 'view-order-beers'):
	beers = link.get_text()
	beers = beers.splitlines()

	currentType = beers[1]
	
	#Create a radom color for the spreadsheet
	randomHex = lambda: random.randint(0,255)
	currentColor = '#%02X%02X%02X' % (randomHex(),randomHex(),randomHex())
	for i in range (0, len(beers) / 8):
		#Starting index for beer information
		ind = i * 8
		
		#Beer Name and Price are on same line
		namePrice = beers[ind + 3].split(u'\u2013')
		name = namePrice[0].strip()
		price = namePrice[1].strip().replace('$', '').replace('%', '')
		
		ABV = beers[ind + 6].split()
		ABV = ABV[0].strip().replace('(', '').replace(')', '').replace('%', '').replace(',', '.')
		
		volString = beers[ind + 9].split()
		volume = 0
		try:
			if len(volString) == 4:
				#If the glass name has two words (Mini Snifter, Wine Glass, etc) 
				volume = volString[2].strip()
			else:
				volume = volString[1].strip()
		except:
			#if there is no volume, default to tulip (13 oz.)
			volume = "13"
			
		beerData.append([name, float(price), float(ABV), float(volume), currentType, currentColor])

workbook = xlsxwriter.Workbook('{}.xlsx'.format(fileName))
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Type')
worksheet.write('B1', 'Name')
worksheet.write('C1', 'Price')
worksheet.write('D1', 'ABV')
worksheet.write('E1', 'Volume')
worksheet.write('F1', 'Alcohol Amount per Price')

for i in range (0, len(beerData)):
	rowNum = str(i + 2)
	format = workbook.add_format({'bg_color': beerData[i][5]})
	worksheet.write('A' + rowNum, beerData[i][4], format)
	worksheet.write('B' + rowNum, beerData[i][0])
	worksheet.write('C' + rowNum, beerData[i][1])
	worksheet.write('D' + rowNum, beerData[i][2])
	worksheet.write('E' + rowNum, beerData[i][3])
	worksheet.write('F' + rowNum, '=((D{} * 0.1) * E{}) / C{}'.format(rowNum, rowNum, rowNum))

workbook.close()
print "Scraping Complete, workbook saved as {}.xlsx".format(fileName)
