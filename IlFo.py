#! /usr/bin/python26

import sys
import os
import re
import urllib
import csv
import decimal
import DictCode

"""
---IL FORNAIO RATINGS PULLER---
This program pulls scores from:
-CitySearch
-Google
-OpenTable
-Trip Advisor
-UrbanSpoon
-Yelp

In order to run it properly, make sure that IlFo.py and DictCode.py are
in the same folder, and that URL_Files is a subfolder.

The program will look at all files in the URL_Files folder, going through
each one and pulling the reviews for that site. The 'Restaurant List' contains
all of the restaurants and is used to create the keys in rest_dict.

The output is saved as Scores_CSV.csv in the same folder as this file.
Additionally, output will print to the console so progress can be checked.
"""

########
    
"""CREATE MASTER DICT THAT WILL HOLD ALL INFO"""
rest_list = open('Restaurant_List.txt', 'rU')
rest_list = rest_list.readlines()

#Populate all of the restaurant names, and for each name add the empty site_dict
rest_dict = {}
for rest in rest_list:
    if rest[-1:] == '\n':
        rest_dict[rest[:-1]] = {}
    else: rest_dict[rest] = {} 

########

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
    location = re.search('<title>(Canaletto)?(?:\sRistorante\sVeneto)?(?:Il Fornaio)?'
                         '(?:IL Fornaio)?(?:Ilfornaio)?\s(?:-\s[\w\s]+)?-\s([\w\s]+),\s\w\w',urltext)

    #Create location string
    #If Canaletto, add location to 'Canaletto'
    if location.group(1):locationgroup = location.group(1) + ' ' + location.group(2)

    #If 'Il Fornaio' is present, location is just group(2)
    else:locationgroup = location.group(2) 

    #This isn't super clean, but Carmel prints as 'Carmel-By-The-Sea'. This converts it to 'Carmel'.
    if locationgroup == 'Carmel By the Sea':locationgroup = 'Carmel'
    
    #Create location/score string
    if allinfo:rest_dict[locationgroup]['CitySearch'] = score
    else:rest_dict[locationgroup]['CitySearch'] = 'N/A'

    print locationgroup + ' ' + str(score)


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

    #Sentence case the location (it pulls as all lowercase)
    locationgroup = locationgroup.title()

    #Create location/score string
    if allinfo:rest_dict[locationgroup]['Google'] = allinfo.group(1)
    else:rest_dict[locationgroup]['Google'] = 'N/A'

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

    #Create location/score string
    if allinfo:rest_dict[locationgroup]['OpenTable'] = allinfo.group(1) + '.' + allinfo.group(2)
    else:rest_dict[locationgroup]['OpenTable'] = 'N/A'

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
    if allinfo.group(1):
        rest_dict[locationgroup]['TripAdvsior'] = allinfo.group(1)
        print locationgroup + ' ' + allinfo.group(1)
    else:
        rest_dict[locationgroup]['TripAdvisor'] = 'N/A'
        print locationgroup + ' N/A'


        
"""*****URBANSPOON*****"""  
def UrbanSpoon(urltext):#COMPLETE#
    #Rating regex
    allinfo = re.search('[\"\'](?:average\s)?(?:digits\s)?percent-text rating'
                        '(?:\saverage)?\\\["\']>(\d\d)', urltext)

    #Location regex
    location = re.search('<title>(Canaletto)?(?:Il\sFornaio)?[\s\w\/]+'
                         '(?:-[\/\w\s]*)?-\s([\w\s]+)(?:[-\w]+)?\s\|', urltext)

    #Create location string
    if location.group(1):locationgroup = location.group(1) + ' ' + location.group(2) #If Canaletto, add location to 'Canaletto'
    else:locationgroup = location.group(2) #If 'Il Fornaio' is present, location is just group(2)

    #Create location/score string
    if allinfo:
        rest_dict[locationgroup]['UrbanSpoon'] = str(round(decimal.Decimal(allinfo.group(1)) / decimal.Decimal('20'),1))
        print locationgroup + ' ' + str(round(decimal.Decimal(allinfo.group(1)) / decimal.Decimal('20'),1))
    else:
        rest_dict[locationgroup]['UrbanSpoon'] = 'N/A'
        print locationgroup + ' N/A'



"""*****YELP*****"""  
def Yelp(urltext):#COMPLETE#
    #Rating regex
    allinfo = re.search('<div id=\"bizRating\">[\W]*<div class=\"rating">[\W]*<span\s' + \
                        'class=\"star-img\sstars_\d[_\w]*\"><img\sclass=\"rating\saverage\"\s' + \
                        'width=\"[\d]+\"\sheight=\"[\d]+\"\stitle=\"(\d\.\d)', urltext)
    
    #Location regex                    
    location = re.search('<title>(Il\sFornaio)?(\sRestaurant \& Bakery)?(Canaletto)?\s[-\s\w]*-+'
                         '\s*([\w\s]+),\s\w\w</title>', urltext)

    #Create location string
    if location.group(1):locationgroup = location.group(4) #If 'Il Fornaio' is present, location is just group(4)
    else:locationgroup = location.group(3) + ' ' + location.group(4) #If Canaletto, add location to 'Canaletto'

    #Create location/score string
    if allinfo.group(1):
        rest_dict[locationgroup]['Yelp'] = allinfo.group(1)
        print locationgroup + ' ' + allinfo.group(1)
    else:
        rest_dict[locationgroup]['Yelp'] = 'N/A'
        print locationgroup + ' N/A'



############################
def wget(url, FuncToCall):
    try:
        ufile = urllib.urlopen(url)
        if ufile.info().gettype() == 'text/html':
            text = ufile.read()
            #To test individual this format: UrbanSpoon(text)
            globals()[FuncToCall](text)
    except IOError:
        """
        In the .txt, each line is a URL. In cases where there is a known
        missing score, the line will just be the location.
        Store this value and 'N/A' in the master dictionary.
        """
        rest_dict[url[:-1]][FuncToCall] = 'N/A'

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

    """
    #CSV#
    #Now that the main dict has been created, generate the CSV.
    """
    #Writes the dictionary to a file as text (for debugging/testing)
    #dict_output = open('Dict_Output.txt', 'w')
    #dict_output = dict_output.write(str(rest_dict))
    #dict_output.close()

    #Run DictCode to convert rest_dict into a list of lists that can
    #be easily parsed by the CSV writer
    score_output = DictCode.CSVOutput(rest_dict)

    #Generate CSV
    scores_csv = open('Scores_CSV.csv', 'wt')
    scores_csv_w = csv.writer(scores_csv, lineterminator='\n')

    #Write each line as a row
    for line in score_output:
        scores_csv_w.writerow(line)

    scores_csv.close()

if __name__ == '__main__':
    main()
