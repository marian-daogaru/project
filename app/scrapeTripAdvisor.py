import os
from app import app, db
import numpy as np
from restaurantExtraction import extractRestaurant, openWebsite, extractDetailsTripAdvisor
from .models import Restaurant, Media, RestaurantDetails

defaultLink = '/Restaurants-g294458-oa{}-Bucharest.html#EATERY_LIST_CONTENTS'
# defaultLink = '/Restaurants-g294458-oa1650-Bucharest.html#EATERY_LIST_CONTENTS'
tripLink = 'https://www.tripadvisor.com'

def cityAllRestaurants(cityLink=defaultLink):
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
                # id = Restaurant.query.filter_by(website = localLink).first().id
                # details = extractDetailsTripAdvisor(localLink)
                # restDetails = RestaurantDetails.addToDatabase(id, details)

    except Exception as e:
        print(e)
        print('finish')
    print("ACTUAL FINISH")



# with open('url.txt', 'wb') as myfile:
#     myfile.write(openWebsite(tripLink + defaultLink.format(0)).read())
print("HELLO2222")
# print(cityAllRestaurants())
