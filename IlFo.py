#! /usr/bin/Python27

import sys
import os
import re
import urllib
import csv
import decimal
from functools import partial

#spamWriter = csv.writer(open('C:\\Users\\TBowland\\Documents\\Python\\Il Fornaio\\' + \
#                             'eggs.csv', 'wb'), delimiter=',', quoting=csv.QUOTE_MINIMAL)

"""
Il Fornaio Scores Generator
This program pulls scores from:
-CitySearch
-Google
-OpenTable
-Trip Advisor
-UrbanSpoon
-Yelp
-Zagat
"""

"""*****CITYSEARCH*****"""        
def CitySearch(urltext): #COMPLETE#
    #No Del Mar, Reston, Seattle has location but no score
    #Score regex
    allinfo = re.search('<img src=\"http://images3\.citysearch\.net/jawr/guide/images/' + \
                        'cb1275124803/assets/guide/images/star_rating_sprites' + \
                        '\.gif\" alt=\"(\d[.\d]*)', urltext)

    #Add digit to score
    if allinfo:
        if len(allinfo.group(1))==1:score = str(allinfo.group(1)) + '.0'
        else:score = allinfo.group(1)
    else:score = 'NO SCORE'
    
    #location = re.search('<meta property=\"og:locality\"\scontent\=\"([\w\s]+)\"/>', urltext)
    location = re.search('<title>(Canaletto)?(?:\sRistorante\sVeneto)?(?:Il Fornaio)?(?:IL Fornaio)?(?:Ilfornaio)?\s(?:-\s[\w\s]+)?-\s([\w\s]+),\s\w\w',urltext)

    #Create location string
    if location.group(1):locationgroup = location.group(1) + ' ' + location.group(2) #If Canaletto, add location to 'Canaletto'
    else:locationgroup = location.group(2) #If 'Il Fornaio' is present, location is just group(2)

    #Create location/score string
    if allinfo:print locationgroup + ' ' + score
    else:print locationgroup + ' NO INFO SON'


"""*****GOOGLE*****"""  
def Google(urltext): #COMPLETE#
    #Rating regex
    allinfo = re.search('g:groups=\"maps\"\sg\:rating_override=\"' + \
                        '(\d\.\d)[\d]+\"\sclass=\"rsw-stars\s\"><',urltext)
    #Location regex
    location = re.search('x-webkit-grammar=\"builtin\:maps\"\svalue=' + \
                         '\"(Canaletto)?(?:il fornaio)?(?:\s)?([\w\s]*)\s*\w*\w*\"', urltext)

    #Create location string
    if location.group(1):locationgroup = location.group(1) + ' ' + location.group(2) #If Canaletto, add location to 'Canaletto'
    else:locationgroup = location.group(2) #If 'Il Fornaio' is present, location is just group(2)

    #States are appended in some cases; this removes them
    locationstate = locationgroup[-3:] #Last three strings will be space letter letter if state included
    locationstateRE = re.search(r'\s\w\w', locationstate)
    if locationstateRE:
        locationgroup = locationgroup[0:-3] #If state included, remove it

    print locationgroup + ' ' + allinfo.group(1)
    

"""*****OPENTABLE*****"""  
def OpenTable(urltext): #COMPLETE#
    #Does not include LV (no OpenTable score for Vegas)
    allinfo = re.search('Overall[\W]+</div><div class="BVRRRatingNormalImage"> ' + \
                        '<img src="http://opentable.ugc.bazaarvoice.com/0938/' + \
                        '(\d)_(\d)/5/rating.gif', urltext)

    #Location regex
    location = re.search('<title>[\s]*(Canaletto)?(?:\sRistorante\sVeneto)?(?:\sRestaurant)?(?:Il Fornaio)?\s(?:-\s[\w\s]+)?- ([\w\s]+)',urltext)

    #Create location string
    if location.group(1):locationgroup = location.group(1) + ' ' + location.group(2) #If Canaletto, add location to 'Canaletto'
    else:locationgroup = location.group(2) #If 'Il Fornaio' is present, location is just group(2)

    print locationgroup + ' ' + allinfo.group(1) + '.' + allinfo.group(2)


"""*****TRIPADVISOR*****"""  
def TripAdvisor(urltext): #COMPLETE#
    #Rating regex
    allinfo = re.search('<img class=\"sprite-ratings\"\sproperty=\"v\:average\"\s' + \
                        'src=\"http://c1\.tacdn\.com/img2/x\.gif\"\salt="(\d\.\d)',urltext)

    #Location regex
    location = re.search('<title>(?:Il\sFornaio)?(Canaletto)?,\s([\w\s]+)\s-\sRestaurant', urltext)

    #Create location string
    if location.group(1):locationgroup = location.group(1) + ' ' + location.group(2) #If Canaletto, add location to 'Canaletto'
    else:locationgroup = location.group(2) #If 'Il Fornaio' is present, location is just group(2)

    #Create location/score string
    if allinfo.group(1):print locationgroup + ' ' + allinfo.group(1)
    else:print locationgroup + ' NO INFO SON'
    
        
"""*****URBANSPOON*****"""  
def UrbanSpoon(urltext):#COMPLETE#
    #Rating regex
    allinfo = re.search('[\"\'](?:average\s)?(?:digits\s)?percent-text rating(?:\saverage)?\\\["\']>(\d\d)', urltext)

    #Location regex
    location = re.search('<title>(Canaletto)?(?:Il\sFornaio)?[\s\w\/]+(?:-[\/\w\s]*)?-\s([\w\s]+)(?:[-\w]+)?\s\|', urltext)

    #Create location string
    if location.group(1):locationgroup = location.group(1) + ' ' + location.group(2) #If Canaletto, add location to 'Canaletto'
    else:locationgroup = location.group(2) #If 'Il Fornaio' is present, location is just group(2)

    #Create location/score string
    if allinfo:print locationgroup + ' ' + str(round(decimal.Decimal(allinfo.group(1)) / decimal.Decimal('20'),1))
    else:print locationgroup + ' NO INFO SON'


"""*****YELP*****"""  
def Yelp(urltext):#COMPLETE#
    #Rating regex
    allinfo = re.search('<div id=\"bizRating\">[\W]*<div class=\"rating">[\W]*<span\s' + \
                        'class=\"star-img\sstars_\d[_\w]*\"><img\sclass=\"rating\saverage\"\s' + \
                        'width=\"[\d]+\"\sheight=\"[\d]+\"\stitle=\"(\d\.\d)', urltext)
    
    #Location regex                    
    location = re.search('<title>(Il\sFornaio)?(\sRestaurant \& Bakery)?(Canaletto)?\s[-\s\w]*-+\s*([\w\s]+),\s\w\w</title>', urltext)

    #Create location string
    if location.group(1):locationgroup = location.group(4) #If 'Il Fornaio' is present, location is just group(4)
    else:locationgroup = location.group(3) + ' ' + location.group(4) #If Canaletto, add location to 'Canaletto'

    #Create location/score string
    if allinfo.group(1):print locationgroup + ' ' + allinfo.group(1)
    else:print locationgroup + ' NO INFO SON'


############################
def wget(url, FuncToCall):
    try:
        ufile = urllib.urlopen(url)
        if ufile.info().gettype() == 'text/html':
            text = ufile.read()
            #OpenTable(text)
            #UrbanSpoon(text)
            #CitySearch(text)
            #TripAdvisor(text)
            #Google(text)
            #Yelp(text)
            globals()[FuncToCall](text)
    except IOError:
        print 'URL skipped.'


def GetFile(URLtoOpen, FuncToCall):
    """Very cool code! Let's you pass a string as a function."""
    #globals()['FuncToCall']('donkey')

    #Open the txt and pass each line as the URL to check
    OTFile = open(URLtoOpen,'rU')
    print '*' * 10 + FuncToCall + '*' * 10
    for line in OTFile:
        #'line' is the URL; 'FuncToCall' is the str function to call
        wget(line, FuncToCall)    


def main():
    """MAIN FUNCTION"""
    #Pull all text files from subdir /URL_Files.
    #Create a path based on the current file dir and the 'URL_Files' folder
    path = os.path.join(os.getcwd(), 'URL_Files')
    file_list = os.listdir(os.getcwd() + '\\URL_Files')

    """
    #Pass each file and its corresponding function to wget.
    #Corresponding function name is the pre-txt part of filename
    """
    for filer in file_list:
        filer = os.path.join(path, filer)
        GetFile(filer, str(re.search(r'([\w]+)\.txt', filer).group(1)))


if __name__ == '__main__':
    main()
