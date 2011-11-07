#!/usr/bin/python2.6

import ast

def CSVOutput(dicter):
    #Read output from main function
    #filer = open('Dict_Output.txt', 'rU')
    #filer = filer.read()
    #filer = ast.literal_eval(filer)

    """SITES"""
    sites = []

    #Cycle through each restaurant, pulling the sites and adding to master list.
    for restaurants in dicter.values():
       for site in restaurants:
           if site in sites:
               pass
           else:
               sites.append(site)

    #Sort the list
    sites = sorted(sites)


    """LOCATIONS"""
    locations = []

    #Cylcle through each location, adding it to the master list.
    for index, location in enumerate(dicter):
        locations.append(location)

    #Sort the list
    locations = sorted(locations)


    """RESTAURANT/LOCATION"""
    master_list = []

    #For each restaurant/location, create a list in the following format:
    #['Santa Monica', '2.5', '4.0, '4.6', ...]

    for index, location in enumerate(locations):
        #Individual location list
        list_name = [location]

        #Lookup the corresponding site score in the location dict
        for site in sites:
            list_name.append(dicter[location][site])

        #Add the list to the master lsit
        master_list.append(list_name)


    #Sort the master list
    master_list = sorted(master_list)

    #Add 'Restaurant/Location' placeholder to the beginning of the sites list
    sites.insert(0, 'Restaurant/Location')


    #print sites
    #for stuff in master_list:
    #    print stuff

    master_list.insert(0, sites)

    return master_list

def main():
    pass

if __name__ == '__main__':
    main()

