import urllib2, urllib
link = 'https://www.hipmenu.ro/kfc-iulius-cluj?c=00DMAOKMG1TB4M&src=hipMenu&l=ro'

mediaFolderPath = 'app/data/media/avatars/restaurants/'

def openWebsite(link):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener.open(link)


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
    avatarName = mediaFolderPath + '{}.jpg'.format("".join(name.split()).lower())

    saveImage(avatarName, avatarLink)

    return (name, avatarName)

def extractHipMenu(link):
    webpage = openWebsite(link).read()
    nameIndexStart = webpage.index('<div class="top-bar-name"><span>') + 32
    nameIndexStop = webpage[nameIndexStart:].index("</span>") + nameIndexStart
    name = webpage[nameIndexStart : nameIndexStop]

    bannerIndex = webpage.index('id="logoInfo"')
    httpStart = webpage[bannerIndex:].index("https://") + bannerIndex
    httpStop = webpage[httpStart:].index('">') + httpStart
    avatarLink = webpage[httpStart : httpStop]
    avatarName = mediaFolderPath + '{}.jpg'.format("".join(name.split()).lower())

    saveImage(avatarName, avatarLink)
    
    return name, avatarLink, avatarName
#
# with open('url.txt', 'w') as myfile:
#     myfile.write(openWebsite(link).read())
