# HopCat Tapper

The HopCat Tapper is used to find out how to get the most bang for your buck at HopCat. As a college student, I wanted to make a program that helped users living on a budget find a way to get the most out of their beers.

**Note:** *This only checks for beers on tap, no bottles currently*

**PLEASE DRINK RESPONSIBLY**

## Getting Started
First install the requirements by running:

`sudo pip3 install -r requirements.txt`

Then run the program with:

`python3 tapper.py`



## Required Input
### Location
For the locations, check out https://hopcat.com and select a location from the dropdown, the location that you need to input should be the string after the last '/' in the url
Examples:

`ann-arbor`

`detroit`

`east-lansing`

`chicago`

**Note:** *Currently the HopCat website will not 404 if a user tries to view a beer list for an incorrect city name. If the Excel sheet is empty, it is possible that you may have mis-typed the location.*

### Filename
Filename must not be blank, any whitespace in the filename will be removed



## Output
If everything works properly, you should have an Excel document in the project folder with the name you gave it.
The top-most beer will be have the most alcohol for the amount you will pay.
The `Type` column will be what type of beer it is.
