from bs4 import BeautifulSoup
import urllib2, random, xlsxwriter

print "\nHopCat Tapper created by Nicholas Tesija\n"
print "For location formats please visit https://hopcat.com and choose a location. \nThe string following 'hopcat.com' will be submitted below\n"

location = raw_input("Please enter a location (ex. ann-arbor, east-lansing): ")

gettingFilename = True
while gettingFilename:
	fileName = raw_input("Please enter a filename for the spreadsheet: ")
	if len(fileName) > 0:
		fileName = "".join(fileName.split())
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
	randomHex = lambda: random.randint(100,255)
	currentColor = '#%02X%02X%02X' % (randomHex(),randomHex(),randomHex())
	
	#Beer information is 8 indicies apart
	for i in range (0, len(beers) / 8):
		#Starting index for beer information
		ind = i * 8
		
		#Beer Name and Price are on same line
		namePrice = beers[ind + 3].split(u'\u2013')
		name = namePrice[0].strip()
		price = float(namePrice[1].strip().replace('$', '').replace('%', ''))
		
		ABV = beers[ind + 6].split()
		ABV = float(ABV[0].strip().replace('(', '').replace(')', '').replace('%', '').replace(',', '.'))
		
		volString = beers[ind + 9].split()
		volume = 0
		try:
			if len(volString) == 4:
				#If the glass name has two words (Mini Snifter, Wine Glass, etc) 
				volume = float(volString[2].strip())
			else:
				volume = float(volString[1].strip())
		except:
			#if there is no volume, default to tulip (13 oz.)
			volume = 13
			
		ppv = float(((ABV * .1) * volume) / price)
		beerData.append([name, price, ABV, volume, currentType, currentColor, ppv])

beerData = sorted(beerData, key=lambda beer: beer[6], reverse=True)

workbook = xlsxwriter.Workbook('{}.xlsx'.format(fileName))
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})
worksheet.write('A1', 'Type', bold)
worksheet.write('B1', 'Name', bold)
worksheet.write('C1', 'Price', bold)
worksheet.write('D1', 'ABV', bold)
worksheet.write('E1', 'Volume', bold)
worksheet.write('F1', 'Alcohol Amount per Price', bold)

worksheet.set_column(0, 1, 25)
worksheet.set_column(5, 5, 25)

for i in range (0, len(beerData)):
	rowNum = str(i + 2)
	typeCell = workbook.add_format({'bg_color': beerData[i][5], 'bold': True})
	worksheet.write('A' + rowNum, beerData[i][4], typeCell)
	worksheet.write('B' + rowNum, beerData[i][0])
	worksheet.write('C' + rowNum, beerData[i][1])
	worksheet.write('D' + rowNum, beerData[i][2])
	worksheet.write('E' + rowNum, beerData[i][3])
	worksheet.write('F' + rowNum, beerData[i][6])

workbook.close()
print "Scraping Complete, workbook saved as {}.xlsx".format(fileName)
