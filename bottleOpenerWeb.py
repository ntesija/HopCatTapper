from bs4 import BeautifulSoup
import urllib3, random, math, certifi

def getBottleOpenerData(cityName):
    location = cityName

    #beerData = [ [name, price, ABV, Volume, type, color (for chart)] ]
    beerData = []

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    response = http.request('GET', 'https://hopcat.com/beer-bottles/{}'.format(location))
    html = response.data

    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('div', 'view-order-beers'):
        beers = link.get_text()
        beers = beers.splitlines()

        currentType = beers[1]
        #Create a radom color for the spreadsheet
        randomHex = lambda: random.randint(100,255)
        currentColor = '#%02X%02X%02X' % (randomHex(),randomHex(),randomHex())
        
        #Beer information is 8 indicies apart
        for i in range (0, math.floor(len(beers) / 8)):
            #Starting index for beer information
            ind = i * 8
            
            #Beer Name and Price are on same line.
            #For bottles, the first line may contain the volume as well
            namePrice = beers[ind + 3].split(u'\u2013')
            name = namePrice[0].strip()
            if(len(name) == 0):
                continue

            volume = 0
            if "oz" in name:
                nameVol = name.split()
                #try/except in case there is a space between the amount and the word "can"
                try:
                    volume = float(nameVol[len(nameVol) - 1].strip().replace('(', '').replace(')', '').replace('oz', ''))
                except:
                    volume = float(nameVol[len(nameVol) - 2].strip().replace('(', '').replace(')', '').replace('oz', ''))

            if "ml" in name:
                nameVol = name.split()
                #try/except in case there is a space between the amount and "ml"
                try:
                    volume = float(nameVol[len(nameVol) - 1].strip().replace('(', '').replace(')', '').replace('ml', ''))
                except:
                    volume = float(nameVol[len(nameVol) - 2].strip().replace('(', '').replace(')', '').replace('ml', ''))

                #Convert to oz
                volume = volume / 29.5735296875

            price = float(namePrice[1].strip().replace('$', '').replace('%', ''))

            ABV = beers[ind + 6].split()
            #To fix situation where "( %5.0)"
            ABV_ind = 0 if len(ABV[0]) > 1 else 1
            ABV = (ABV[ABV_ind].strip().replace('(', '').replace(')', '').replace('%', '').replace(',', '.').replace('ABV', '').replace('<', ''))
            ABV = float(ABV)
            if volume == 0:
                volString = beers[ind + 9].split()
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
            beerData.append({
                'name': name,
                'price': price,
                'ABV': ABV,
                'volume': volume,
                'currentType': currentType + " (Bottle)",
                'currentColor': currentColor,
                'ppv': ppv
            })

    beerData = sorted(beerData, key=lambda beer: beer['ppv'], reverse=True)
    
    return beerData