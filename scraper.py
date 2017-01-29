from bs4 import BeautifulSoup
import urllib2
import xlsxwriter

#beerData = [ [name, price, ABV, Volume, type] ]
beerData = []

response = urllib2.urlopen('https://hopcat.com/beer/ann-arbor')
html = response.read()

soup = BeautifulSoup(html, 'html.parser')

currentType = ''
for link in soup.find_all('div', 'view-order-beers'):
	#beers = BeautifulSoup(link, 'html.parser')
	beers = link.get_text()
	beers = beers.splitlines()
	currentType = beers[1]
	print currentType
	print beers
	for i in range (0, len(beers) / 8):
		ind = i * 8
		namePrice = beers[ind + 3].split(u'\u2013')
		name = namePrice[0].strip()
		price = namePrice[1].strip().replace('$', '').replace('%', '')
		ABV = beers[ind + 6].split()
		ABV = ABV[0].strip().replace('(', '').replace(')', '').replace('%', '').replace(',', '.')
		
		volString = beers[ind + 9].split()
		volume = 0
		if len(volString) == 4:
			volume = volString[2].strip()
		else:
			volume = volString[1].strip()
			
		beerData.append([name, float(price), float(ABV), float(volume), currentType])
		


#print beerData

workbook = xlsxwriter.Workbook('hopcatBeers.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Type')
worksheet.write('B1', 'Name')
worksheet.write('C1', 'Price')
worksheet.write('D1', 'ABV')
worksheet.write('E1', 'Volume')
worksheet.write('F1', 'Alcohol Amount per Price')

for i in range (0, len(beerData)):
	rowNum = str(i + 1)
	worksheet.write('A' + rowNum, beerData[i][4])
	worksheet.write('B' + rowNum, beerData[i][0])
	worksheet.write('C' + rowNum, beerData[i][1])
	worksheet.write('D' + rowNum, beerData[i][2])
	worksheet.write('E' + rowNum, beerData[i][3])
	worksheet.write('F' + rowNum, '=((D{} * 0.1) * E{}) / C{}'.format(rowNum, rowNum, rowNum))

workbook.close()
print "Scraping Complete, workbook saved as hopcatBeers.xlsx"
