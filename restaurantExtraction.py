import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import urllib2
import urllib
import ssl
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from config import basedir, RESTAURANTPATH
# link = 'https://www.tripadvisor.com/Restaurants-g294458-Bucharest.html'
link = 'https://www.tripadvisor.com/Restaurant_Review-g294458-d7813701-Reviews-Borsalino-Bucharest.html'

def extractRestaurant(url):
    extractPlacesFuncDict = {
            'foodpanda': [extractFoodPanda, extractDetailsFoodPanda],
            'oliviera': [extractOliviera, extractDetailsOliviera],
            'caserola': [extractCaserola, extractDetailsCaserola],
            'hipmenu': [extractHipMenu, extractDetailsHipMenu],
            'tripadvisor': [extractTripAdvisor, extractDetailsTripAdvisor]
        }
    for key, funcs in extractPlacesFuncDict.items():
        if key in url.lower():
            rest = funcs[0](url)
            details = funcs[1](url)
            return [rest, details]
    print("NOT HERE")
    return extractParticular(url), extractDetailsParticular(url)



def openWebsite(link):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A')]
    return opener.open(link)


def openWebsiteCert(link):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib2.urlopen(link, context=ctx)


def saveImage(imageName, imageLink):
    imagePath = os.path.join(basedir + '/app/', imageName[3:])
    with open(imagePath, 'wb') as myfile:
        myfile.write(urllib2.urlopen(imageLink).read())

# ##############################################################################
# FOODPANDA
# ##############################################################################
def extractFoodPanda(link):
    webpage = openWebsite(link).read()
    nameIndex = webpage.index('"name"') + 8
    firstCommaIndex = webpage[nameIndex:nameIndex+100].index(',')
    name = webpage[nameIndex+1 : nameIndex+firstCommaIndex-1]
    name = re.sub('/', '', name)

    bannerIndex = webpage.index("b-lazy hero-banner")
    httpStart = webpage[bannerIndex:].index("https://") + bannerIndex
    httpStop = webpage[httpStart + 10:].index("https://") + httpStart + 9  # 10 - 1 due to | at the end
    avatarLink = webpage[httpStart : httpStop]
    avatarName = RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())

    saveImage(avatarName, avatarLink)

    return (name, avatarName)

def extractDetailsFoodPanda(link):
    webpage = openWebsite(link).read()
    details = {}
    details['phoneNumber'] = None
    # coords search
    try:
        searchStartParam = 'staticmap?center='
        searchEndParam = '&amp'
        coordsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        coordsEndIndex = webpage[coordsStartIndex:].index(searchEndParam) + coordsStartIndex
        coords = webpage[coordsStartIndex:coordsEndIndex]
        lat, lon = [float(coord) for coord in coords.split(',')]
        details['lat'] = lat
        details['lon'] = lon
    except:
        details['lat'] = None
        details['lon'] = None

    # tags search
    try:
        searchStartParam = '<ul class="vendor-info-main-details-cuisines">'
        searchEndParam = '</ul>'
        tagsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        tagsEndIndex = webpage[tagsStartIndex:].index(searchEndParam) + tagsStartIndex
        tags = [tag.split('>')[1] for tag in webpage[tagsStartIndex:tagsEndIndex].split("<")[1::2]]
        print(tags)
        details['tags'] = tags[1:]
        details['priceRange'] = tags[0]
    except:
        print("not here")
        details['tags'] = None
        details['priceRange'] = None
    print(details)
    # delivery times
    try:
        searchStartParam = '<ul class="vendor-delivery-times">'
        searchEndParam = '</ul>'
        dtStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        dtEndIndex = webpage[dtStartIndex:].index(searchEndParam) + dtStartIndex
        deliveryTimes = webpage[dtStartIndex:dtEndIndex].split()
        deliveryTimes = [int(time.split(':')[0]) + int(time.split(':')[1]) / 100 for time in [deliveryTimes[7], deliveryTimes[9]]]
        details['workingHours'] = str(deliveryTimes[0]) + ' - ' + str(deliveryTimes[1])
    except:
        details['workingHours'] = None

    # address
    try:
        searchStartParam = '<p class="vendor-location">'
        searchEndParam = '</p>'
        addrStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        addrEndIndex = webpage[addrStartIndex:].index(searchEndParam) + addrStartIndex
        address = webpage[addrStartIndex:addrEndIndex]
        details['address'] = address
    except:
        details['address'] = None

    return details


# ##############################################################################
# OLIVIERA
# ##############################################################################
def extractOliviera(link):
    webpage = openWebsite(link).read()
    nameIndex = webpage.index('meta property="og:title" content="') + 34
    firstBraketIndex = webpage[nameIndex:].index('>') + nameIndex - 1  # exclude the "
    name = webpage[nameIndex : firstBraketIndex]
    name = re.sub('/', '', name)

    httpStart = firstBraketIndex + 42  # \n\t\t<meta property="og:image" content=" length
    httpStop = webpage[httpStart:].index('">') + httpStart
    avatarLink = webpage[httpStart : httpStop]
    avatarName = RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())

    # this is different because we are using certificate authentification
    with open(os.path.join(basedir + '/app/', avatarName[3:]), 'wb') as myfile:
        myfile.write(openWebsiteCert(avatarLink).read())

    return name, avatarName

def extractDetailsOliviera(link):
    link = '/'.join(link.split('/')[:-1]) + '/profile'
    webpage = openWebsite(link).read()
    details = {}
    details['priceRange'] = ''
    details['workingHours'] = ''
    details['phoneNumber'] = ''

    """LOCATION IS NOT VERY NICE TO GET, ALMOST IMPOSSIBLE"""
    """UPDATE: NEVER SAY NEVER BOY!"""
    # coords search
    try:
        searchStartParam = '&quot;lat&quot;:'
        searchEndParam = ',&quot;average_food'
        coordsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        coordsEndIndex = webpage[coordsStartIndex:].index(searchEndParam) + coordsStartIndex
        coords = webpage[coordsStartIndex:coordsEndIndex]
        lat, lon = [float(coord) for coord in coords.split(',&quot;lng&quot;:')]
        details['lat'] = lat
        details['lon'] = lon
    except:
        details['lat'] = None
        details['lon'] = None

    # tags search
    try:
        searchStartParam = '&quot;cuisines&quot;:'
        searchEndParam = ',&quot;pictures'
        tagsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        tagsEndIndex = webpage[tagsStartIndex:].index(searchEndParam) + tagsStartIndex
        tags = [tag.split(',')[0] for tag in webpage[tagsStartIndex:tagsEndIndex].replace('&quot;','').split('name:')[1:]]
        details['tags'] = tags
    except:
        details['tags'] = ''

    # address
    try:
        searchStartParam = 'has_special_promotion&quot'
        searchEndParam = '&quot;,&quot;promotions'
        addrStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        addrEndIndex = webpage[addrStartIndex:].index(searchEndParam) + addrStartIndex
        address = webpage[addrStartIndex:addrEndIndex].split('&quot;address&quot;:&quot;')[-1]
        details['address'] = address
    except:
        details['address'] = ''
    return details


# ##############################################################################
# HIPMENU
# ##############################################################################
def extractHipMenu(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('<div class="top-bar-name"><span>') + 32
    nameIndexStop = webpage[nameIndexStart:].index("</span>") + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]
    name = re.sub('/', '', name)

    logoIndex = webpage.index('id="logoInfo"')
    httpStart = webpage[logoIndex:].index("https://") + logoIndex
    httpStop = webpage[httpStart:].index('">') + httpStart
    avatarLink = webpage[httpStart : httpStop]
    avatarName = RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())

    saveImage(avatarName, avatarLink)

    return name, avatarName

def extractDetailsHipMenu(link):
    webpage = openWebsite(link).read()
    details = {}
    details['workingHours'] = ''
    details['address'] = ''
    details['tags'] = ''
    details['priceRange'] = ''
    details['phoneNumber'] = ''

    """not quite :( """
    # coords search
    try:
        searchStartParam = 'staticmap?center='
        searchEndParam = '&amp'
        coordsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        coordsEndIndex = webpage[coordsStartIndex:].index(searchEndParam) + coordsStartIndex
        coords = webpage[coordsStartIndex:coordsEndIndex]
        lat, lon = [float(coord) for coord in coords.split(',')]
        details['lat'] = lat
        details['lon'] = lon
    except:
        details['lat'] = None
        details['lon'] = None

    return details

# ##############################################################################
# CASEROLA
# ##############################################################################
def extractCaserola(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('h1 itemprop="name"') + 19
    nameIndexStop = webpage[nameIndexStart:].index('</h1>') + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]
    name = re.sub('/', '', name)

    logoIndex = webpage.index('restaurant-logo')
    httpStart = webpage[logoIndex:].index("/images") + logoIndex
    httpStop = webpage[httpStart:].index('" alt=') + httpStart
    avatarLink = 'https://caserola.ro' + webpage[httpStart : httpStop]
    avatarName = RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())

    with open(os.path.join(basedir + '/app/', avatarName[3:]), 'wb') as myfile:
        myfile.write(openWebsite(avatarLink).read())

    return name, avatarName

def extractDetailsCaserola(link):
    details = {}
    details['workingHours'] = ''
    details['address'] = ''
    details['tags'] = ''
    details['priceRange'] = ''
    details['phoneNumber'] = ''
    details['lat'] = None
    details['lon'] = None
    return details


# ##############################################################################
# TRIPADVISOR
# ##############################################################################
def extractTripAdvisor(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('"name" : "') + len('"name" : "')
    nameIndexStop = webpage[nameIndexStart:].index('",') + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]
    name = re.sub('/', '', name)
    name = re.sub('_', ' ', name)

    httpStart = webpage.index('"image" : "') + len('"image" : "')
    httpStop = webpage[httpStart:].index('",') + httpStart
    avatarLink = webpage[httpStart : httpStop]
    avatarName =  RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())

    saveImage(avatarName, avatarLink)
    return name, avatarName

def extractDetailsTripAdvisor(link):
    webpage = openWebsite(link).read()
    details = {}
    # coords search
    try:
        searchStartParam = 'center='
        searchEndParam = '&maptype'
        coordsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        coordsEndIndex = webpage[coordsStartIndex:].index(searchEndParam) + coordsStartIndex
        coords = webpage[coordsStartIndex:coordsEndIndex]
        lat, lon = [float(coord) for coord in coords.split(',')]
        details['lat'] = lat
        details['lon'] = lon
    except:
        details['lat'] = None
        details['lon'] = None

    # tags search
    try:
        searchStartParam = 'CUISINES '
        searchEndParam = '">'
        tagsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        searchStartParam = 'data-content="'
        tagsStartIndex += webpage[tagsStartIndex:].index(searchStartParam) + len(searchStartParam)
        tagsEndIndex = webpage[tagsStartIndex:].index(searchEndParam) + tagsStartIndex
        tags = webpage[tagsStartIndex : tagsEndIndex].split(", ")
        details['tags'] = tags
    except:
        details['tags'] = ''

    #priceRange
    try:
        searchStartParam = '"priceRange" : "'
        searchEndParam = '",'
        priceStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        priceEndIndex = webpage[priceStartIndex:].index(searchEndParam) + priceStartIndex
        details['priceRange'] = webpage[priceStartIndex : priceEndIndex]
    except:
        details['priceRange'] = ''

    # delivery times
    try:
        searchStartParam = '<div class="timeRange" style="white-space: nowrap;">'
        searchEndParam = '</div>'
        dtStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        dtEndIndex = webpage[dtStartIndex:].index(searchEndParam) + dtStartIndex
        deliveryTimes = webpage[dtStartIndex:dtEndIndex]
        details['workingHours'] = deliveryTimes
    except:
        details['workingHours'] = ''

    # address
    try:
        searchStartParam = '"streetAddress" : "'
        searchEndParam = '",'
        addrStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        addrEndIndex = webpage[addrStartIndex:].index(searchEndParam) + addrStartIndex
        address = webpage[addrStartIndex:addrEndIndex]
        details['address'] = str(address)
    except:
        details['address'] = ''

    # phone Number
    try:
        searchStartParam = 'data-phonenumber="'
        searchEndParam = '" dat'
        phoneStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        phoneEndIndex = webpage[phoneStartIndex:].index(searchEndParam) + phoneStartIndex
        phoneNumber = webpage[phoneStartIndex : phoneEndIndex]
        details['phoneNumber'] = phoneNumber
    except:
        details['phoneNumber'] = ''

    return details


# ##############################################################################
# GENERAL
# ##############################################################################
def captureImage(link, imageName):
    imagePath = os.path.join(basedir + '/app/', imageName[3:])
    print(link, imagePath, "$%^")
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)
    driver.get(link)
    driver.save_screenshot(imagePath)
    driver.close()

def extractParticular(link):
    """this is for any other website"""
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('<title>') + 7
    nameIndexStop = webpage[nameIndexStart:].index('</title>') + nameIndexStart - 1
    name = webpage[nameIndexStart : nameIndexStop].split('-')[0]
    name = " ".join(name.split())
    name = re.sub('/', '', name)

    avatarName = RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())
    captureImage(link, avatarName)

    return name, avatarName


def extractDetailsParticular(link):
    details = {}
    details['workingHours'] = ''
    details['address'] = ''
    details['tags'] = ''
    details['priceRange'] = ''
    details['phoneNumber'] = ''
    details['lat'] = None
    details['lon'] = None
    return details


# with open('url.txt', 'wb') as myfile:
#     myfile.write(openWebsite(link).read())

# print(extractDetailsTripAdvisor(link))
