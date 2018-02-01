import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import urllib2
import urllib
import ssl
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# from config import basedir, RESTAURANTPATH
# link = 'https://www.tripadvisor.com/Restaurants-g294458-Bucharest.html'
link = 'https://www.tripadvisor.com/Restaurant_Review-g294458-d7747651-Reviews-La_Pescaria_Dorobantilor-Bucharest.html'

def extractRestaurant(url):
    extractPlacesFuncDict = {
            'foodpanda': extractFoodPanda,
            'oliviera': extractOliviera,
            'caserola': extractCaserola,
            'hipmenu': extractHipMenu,
            'tripadvisor': extractTripAdvisor,
        }
    for key, func in extractPlacesFuncDict.items():
        if key in url.lower():
            return func(url)
    return extractParticular(url)



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
        details['tags'] = tags[1:]
        details['priceRange'] = rags[0]
    except:
        details['tags'] = None
        details['pricerange'] = None

    # delivery times
    try:
        searchStartParam = '<ul class="vendor-delivery-times">'
        searchEndParam = '</ul>'
        dtStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        dtEndIndex = webpage[dtStartIndex:].index(searchEndParam) + dtStartIndex
        deliveryTimes = webpage[dtStartIndex:dtEndIndex].split()
        deliveryTimes = [int(time.split(':')[0]) + int(time.split(':')[1]) / 100 for time in [deliveryTimes[7], deliveryTimes[9]]]
        details['workingHours'] = deliveryTimes
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
    searchStartParam = '&quot;cuisines&quot;:'
    searchEndParam = ',&quot;pictures'
    tagsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    tagsEndIndex = webpage[tagsStartIndex:].index(searchEndParam) + tagsStartIndex
    tags = [tag.split(',')[0] for tag in webpage[tagsStartIndex:tagsEndIndex].replace('&quot;','').split('name:')[1:]]

    # address
    searchStartParam = 'has_special_promotion&quot'
    searchEndParam = '&quot;,&quot;promotions'
    addrStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    addrEndIndex = webpage[addrStartIndex:].index(searchEndParam) + addrStartIndex
    address = webpage[addrStartIndex:addrEndIndex].split('&quot;address&quot;:&quot;')[-1]
    print(address)
    return {'lat': lat,
            'lon': lon,
            'tags': tags,
            'address': str(address)
            }

def extractHipMenu(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('<div class="top-bar-name"><span>') + 32
    nameIndexStop = webpage[nameIndexStart:].index("</span>") + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]

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

    return 0


def extractCaserola(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('h1 itemprop="name"') + 19
    nameIndexStop = webpage[nameIndexStart:].index('</h1>') + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]

    logoIndex = webpage.index('restaurant-logo')
    httpStart = webpage[logoIndex:].index("/images") + logoIndex
    httpStop = webpage[httpStart:].index('" alt=') + httpStart
    avatarLink = 'https://caserola.ro' + webpage[httpStart : httpStop]
    avatarName = RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())

    with open(os.path.join(basedir + '/app/', avatarName[3:]), 'wb') as myfile:
        myfile.write(openWebsite(avatarLink).read())

    return name, avatarName

def extractTripAdvisor(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('"name" : "') + len('"name" : "')
    nameIndexStop = webpage[nameIndexStart:].index('",') + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]

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
    # # tags search
    # searchStartParam = '<ul class="vendor-info-main-details-cuisines">'
    # searchEndParam = '</ul>'
    # tagsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    # tagsEndIndex = webpage[tagsStartIndex:].index(searchEndParam) + tagsStartIndex
    # tags = [tag.split('>')[1] for tag in webpage[tagsStartIndex:tagsEndIndex].split("<")[1::2]]
    #
    # # delivery times
    # searchStartParam = '<ul class="vendor-delivery-times">'
    # searchEndParam = '</ul>'
    # dtStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    # dtEndIndex = webpage[dtStartIndex:].index(searchEndParam) + dtStartIndex
    # deliveryTimes = webpage[dtStartIndex:dtEndIndex].split()
    # deliveryTimes = [int(time.split(':')[0]) + int(time.split(':')[1]) / 100 for time in [deliveryTimes[7], deliveryTimes[9]]]
    #
    # address
    try:
        searchStartParam = '"street-address">'
        searchEndParam = '</span>'
        addrStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        addrEndIndex = webpage[addrStartIndex:].index(searchEndParam) + addrStartIndex
        address = webpage[addrStartIndex:addrEndIndex]

        searchStartParam = '"locality">'
        searchEndParam = '</span>'
        addrStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
        addrEndIndex = webpage[addrStartIndex:].index(searchEndParam) + addrStartIndex
        address = address + ", " + webpage[addrStartIndex:addrEndIndex]

        details['address'] = str(address)
    except:
        details['address'] = None
    print(lat, lon, address)

    # return {'lat': lat,
    #         'lon': lon,
    #         'tags': tags,
    #         'deliveryTimes': deliveryTimes,
    #         'address': str(address)}


def captureImage(link, imageName):
    imagePath = os.path.join(basedir + '/app/', imageName[3:])
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

    avatarName = RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())
    captureImage(link, avatarName)

    return name, avatarName


# with open('url.txt', 'w') as myfile:
#     myfile.write(openWebsite(link).read())
print(extractDetailsTripAdvisor(link))

# print(os.path.join(basedir + '/app/', RESTAURANTPATH[3:]))
