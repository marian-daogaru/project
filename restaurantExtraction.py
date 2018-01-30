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
link = 'https://www.caserola.ro/restaurant/lacrimisisfinti'


def extractRestaurant(url):
    extractPlacesFuncDict = {
            'foodpanda': extractFoodPanda,
            'oliviera': extractOliviera,
            'caserola': extractCaserola,
            'hipmenu': extractHipMenu
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

    # coords search
    searchStartParam = 'staticmap?center='
    searchEndParam = '&amp'
    coordsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    coordsEndIndex = webpage[coordsStartIndex:].index(searchEndParam) + coordsStartIndex
    coords = webpage[coordsStartIndex:coordsEndIndex]
    lat, lon = [float(coord) for coord in coords.split(',')]

    # tags search
    searchStartParam = '<ul class="vendor-info-main-details-cuisines">'
    searchEndParam = '</ul>'
    tagsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    tagsEndIndex = webpage[tagsStartIndex:].index(searchEndParam) + tagsStartIndex
    tags = [tag.split('>')[1] for tag in webpage[tagsStartIndex:tagsEndIndex].split("<")[1::2]]

    # delivery times
    searchStartParam = '<ul class="vendor-delivery-times">'
    searchEndParam = '</ul>'
    dtStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    dtEndIndex = webpage[dtStartIndex:].index(searchEndParam) + dtStartIndex
    deliveryTimes = webpage[dtStartIndex:dtEndIndex].split()
    deliveryTimes = [int(time.split(':')[0]) + int(time.split(':')[1]) / 100 for time in [deliveryTimes[7], deliveryTimes[9]]]

    # address
    searchStartParam = '<p class="vendor-location">'
    searchEndParam = '</p>'
    addrStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    addrEndIndex = webpage[addrStartIndex:].index(searchEndParam) + addrStartIndex
    address = webpage[addrStartIndex:addrEndIndex]

    return {'lat': lat,
            'lon': lon,
            'tags': tags,
            'deliveryTimes': deliveryTimes,
            'address': str(address)}


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

    """LOCATION IS NOT VERY NICE TO GET, ALMOST IMPOSSIBLE"""
    """UPDATE: NEVER SAY NEVER BOY!"""
    # coords search
    searchStartParam = '&quot;lat&quot;:'
    searchEndParam = ',&quot;average_food'
    coordsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    coordsEndIndex = webpage[coordsStartIndex:].index(searchEndParam) + coordsStartIndex
    coords = webpage[coordsStartIndex:coordsEndIndex]
    lat, lon = [float(coord) for coord in coords.split(',&quot;lng&quot;:')]

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

    """not quite :( """
    # coords search
    searchStartParam = 'staticmap?center='
    searchEndParam = '&amp'
    coordsStartIndex = webpage.index(searchStartParam) + len(searchStartParam)
    coordsEndIndex = webpage[coordsStartIndex:].index(searchEndParam) + coordsStartIndex
    coords = webpage[coordsStartIndex:coordsEndIndex]
    lat, lon = [float(coord) for coord in coords.split(',')]

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
    name = webpage[nameIndexStart : nameIndexStop]

    avatarName = RESTAURANTPATH + '{}.png'.format("".join(name.split()).lower())
    captureImage(link, avatarName)
    return name, avatarName


with open('url.txt', 'w') as myfile:
    myfile.write(openWebsite(link).read())
# print(extractDetailsOliviera(link))

# print(os.path.join(basedir + '/app/', RESTAURANTPATH[3:]))
