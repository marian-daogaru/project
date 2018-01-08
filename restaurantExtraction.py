import urllib2
import urllib
import ssl
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
link = 'https://www.caserola.ro/restaurant/zexezahana'

mediaFolderPath = 'app/static/data/media/avatars/restaurants/'

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
    with open(imageName, 'wb') as myfile:
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
    avatarName = mediaFolderPath + '{}.png'.format("".join(name.split()).lower())

    saveImage(avatarName, avatarLink)

    return (name, avatarName)


def extractOliviera(link):
    webpage = openWebsite(link).read()
    nameIndex = webpage.index('meta property="og:title" content="') + 34
    firstBraketIndex = webpage[nameIndex:].index('>') + nameIndex - 1  # exclude the "
    name = webpage[nameIndex : firstBraketIndex]

    httpStart = firstBraketIndex + 42  # \n\t\t<meta property="og:image" content=" length
    httpStop = webpage[httpStart:].index('">') + httpStart
    avatarLink = webpage[httpStart : httpStop]
    avatarName = mediaFolderPath + '{}.png'.format("".join(name.split()).lower())


    # this is different because we are using certificate authentification
    with open(avatarName, 'wb') as myfile:
        myfile.write(openWebsiteCert(avatarLink).read())

    return name, avatarName


def extractHipMenu(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('<div class="top-bar-name"><span>') + 32
    nameIndexStop = webpage[nameIndexStart:].index("</span>") + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]

    logoIndex = webpage.index('id="logoInfo"')
    httpStart = webpage[logoIndex:].index("https://") + logoIndex
    httpStop = webpage[httpStart:].index('">') + httpStart
    avatarLink = webpage[httpStart : httpStop]
    avatarName = mediaFolderPath + '{}.png'.format("".join(name.split()).lower())

    saveImage(avatarName, avatarLink)

    return name, avatarName


def extractCaserola(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('h1 itemprop="name"') + 19
    nameIndexStop = webpage[nameIndexStart:].index('</h1>') + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]

    logoIndex = webpage.index('restaurant-logo')
    httpStart = webpage[logoIndex:].index("/images") + logoIndex
    httpStop = webpage[httpStart:].index('" alt=') + httpStart
    avatarLink = 'https://caserola.ro' + webpage[httpStart : httpStop]
    avatarName = mediaFolderPath + '{}.png'.format("".join(name.split()).lower())

    with open(avatarName, 'wb') as myfile:
        myfile.write(openWebsite(avatarLink).read())

    return name, avatarLink


def captureImage(link, imageName):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)
    driver.get(link)
    driver.save_screenshot(imageName)
    driver.close()

def extractParticular(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('<title>') + 7
    nameIndexStop = webpage[nameIndexStart:].index('</title>') + nameIndexStart - 1
    name = webpage[nameIndexStart : nameIndexStop]

    avatarName = mediaFolderPath + '{}.png'.format("".join(name.split()).lower())
    captureImage(link, avatarName)
    return name

# with open('url.txt', 'w') as myfile:
#     myfile.write(openWebsite(link).read())

print(extractCaserola(link))
