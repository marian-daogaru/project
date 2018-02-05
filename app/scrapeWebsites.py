import os
from app import app, db
import numpy as np
from restaurantExtraction import extractRestaurant, openWebsite, extractDetailsTripAdvisor,  extractDetailsFoodPanda
from .models import Restaurant, Media, RestaurantDetails

# defaultLink = '/Restaurants-g294458-oa{}-Bucharest.html#EATERY_LIST_CONTENTS'
# # defaultLink = '/Restaurants-g294458-oa1650-Bucharest.html#EATERY_LIST_CONTENTS'
# tripLink = 'https://www.tripadvisor.com'

def cityAllRestaurantsTripAdvisor(cityLink=None):
    if cityLink is None:
        cityLink = '/Restaurants-g294458-oa{}-Bucharest.html#EATERY_LIST_CONTENTS'
    else:
        cityLinkParts = cityLink.split('-')
        cityLink = '-'.join(cityLinkParts[:2]) + '-oa{}-' + '-'.join(cityLinkParts[2:])
    # defaultLink = '/Restaurants-g294458-oa1650-Bucharest.html#EATERY_LIST_CONTENTS'
    tripLink = 'https://www.tripadvisor.com'
    path = tripLink + cityLink.format(0)
    webpage = openWebsite(path).read()
    searchStart = '<div class="pageNumbers">'
    searchStop = '</div>'
    indexStart = webpage.index(searchStart)
    indexStop = webpage[indexStart:].index(searchStop) + indexStart

    data = webpage[indexStart : indexStop].split('data-page-number="')[-1]

    pageNo = int(data.split('"')[0])

    print(pageNo, '2222', data)

    try:
        for pageNumber in range(pageNo):
            print('Page number is at {} !!!'.format(pageNumber))
            path = tripLink + cityLink.format(pageNumber * 30)
            webpage = openWebsite(path).read()
            searchStart = '<div id="EATERY_SEARCH_RESULTS">'
            searchStop = '<div class="deckTools btm">'
            indexStart = webpage.index(searchStart)
            indexStop = webpage[indexStart:].index(searchStop) + indexStart
            rests = webpage[indexStart : indexStop].split('listing rebrand')[1:]
            for rest in rests:
                searchStart = '<a target="_blank" href="'
                searchStop = '" class'
                indexStart = rest.index(searchStart) + len(searchStart)
                indexStop = rest[indexStart:].index(searchStop) + indexStart
                localLink = tripLink + rest[indexStart : indexStop]
                print(localLink)
                if Restaurant.query.filter_by(website = localLink).first() is None:
                    restaurant, details = extractRestaurant(localLink)
                    Restaurant.addToDatabase(restaurant[0],
                                                  localLink,
                                                  restaurant[1],
                                                  details)
                else:
                    id = Restaurant.query.filter_by(website = localLink).first().id
                    details = extractDetailsTripAdvisor(localLink)
                    restDetails = RestaurantDetails.addToDatabase(id, details)

    except Exception as e:
        print(e)
        print('finish')
    print("ACTUAL FINISH")


def cityAllRestaurantsFoodpanda(cityLink):
    fpLink = 'https://www.foodpanda.ro'
    webpage = openWebsite(cityLink).read()
    searchStart = 'class="vendor-list'
    searchStop = 'restaurants__city-bottom-info js-city-bottom-info'
    indexStart = webpage.index(searchStart)
    indexStop = webpage[indexStart:].index(searchStop) + indexStart

    pathsList = [path.split('"')[0] for path in webpage[indexStart : indexStop].split('<a href="')[1:]]

    for path in pathsList:
        localLink = fpLink + path
        print(localLink)
        if Restaurant.query.filter_by(website = localLink).first() is None:
            print('here 1')
            restaurant, details = extractRestaurant(localLink)
            Restaurant.addToDatabase(restaurant[0],
                                          localLink,
                                          restaurant[1],
                                          details)
        else:
            print(' here 2 {}')
            id = Restaurant.query.filter_by(website = localLink).first().id
            details = extractDetailsFoodPanda(localLink)
            restDetails = RestaurantDetails.addToDatabase(id, details)
    print(pathsList)
    return 0


print('hello 12 ')
# with open('url.txt', 'wb') as myfile:
#     print('hey!')
#     myfile.write(openWebsite('https://www.foodpanda.ro/city/bucharest').read())
print("HELLO2222!!")
# print(cityAllRestaurantsFoodpanda('https://www.foodpanda.ro/city/bucharest'))
