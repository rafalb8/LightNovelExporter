import faster_than_requests as requests
from bs4 import BeautifulSoup
from ebooklib import epub
from os import makedirs
from unidecode import unidecode
import json


# Function that generates ranges list
def ranges(numbers):
    out = []
    end = -2
    start = -1

    for item in numbers:
        if item != end + 1:
            if start != -1:
                out.append((start, end))
            start = item
        end = item

    out.append((start, end))

    return out

# Save Settings
def saveSettings(settings):
    json.dump(settings, open('settings.json', 'w'), indent=4)


# Load
def loadSettings():
    return json.load(open('settings.json'))


# Save json with default settings
def defaultSettings():
    settings = {'BooksDirectory': 'books/', 'MainURL': 'readlightnovel.org'}
    saveSettings(settings)


# Get Information about novel
def getInfo(url):
    # Make request and parse html
    body = requests.get2str(url)
    html = BeautifulSoup(body, 'lxml')

    # Get Info
    novel = html.find('div', class_= 'novel')
    title = unidecode(novel.img['alt'])
    img = novel.img['src']

    details = html.select('div.novel-detail-body')

    # Type
    novelType = details[0].a.string

    # Genres
    genres = [genre.string for genre in details[1].select('a')]

    # details[2] - Tags

    # Language
    language = details[3].li.string

    # Author
    author = details[4].li.string

    # Year
    year = details[6].li.string

    # Prepare json object
    info = {'title': title, 'img': img, 'type': novelType, 'genres': genres,
            'language': language, 'author': author, 'year': year, 'chapters': []}

    # Start parsing chapters
    volume = html.select('div.panel-default')

    for vol in volume:
        chapters = []
        for chp in vol.select('ul.chapter-chs a'):
            tmp = {'name': chp.string, 'url': chp['href'], 'volume': vol.h4.string}

            chapters.append(tmp)

        info['chapters'] += chapters

    # Return parsed info
    return info


# Save information to JSON file
def dumpInfo(url, settings):
    info = getInfo(url)
    booksDir = settings['BooksDirectory']

    try:
        makedirs(booksDir+info['title'])
    except OSError:
        pass

    json.dump(info, open(booksDir + info['title'] + '/info.json', 'w'), indent=4)
    return info


# Read JSON file
def loadInfo(title, settings):
    booksDir = settings['BooksDirectory']
    return json.load(open(booksDir + title + '/info.json', 'r'))


def getChapterText(url):
    # Make request and parse html
    body = requests.get2str(url)
    html = BeautifulSoup(body, 'lxml')

    # Get text and format it
    text = '\n'.join([str(p.string).strip() for p in html.find('div', class_='desc') if p.string is not None])
    return text


# Save Chapter text
def dumpChapterText(info, idx, settings):
    booksDir = settings['BooksDirectory']
    try:
        makedirs(booksDir + info['title'])
    except OSError:
        pass

    with open(booksDir + info['title'] + '/' + info['chapters'][idx]['name']+'.txt', 'w') as f:
        f.write(getChapterText(info['chapters'][idx]['url']))


# Save cover
def dumpCover(info, settings):
    booksDir = settings['BooksDirectory']

    try:
        makedirs(booksDir + info['title'])
    except OSError:
        pass

    requests.downloads(info['img'], booksDir + info['title']+'/cover.jpg')


# Generate ePUB
def generateEPUB(filename, title, info, chapters, settings):
    # Create empty ePUB file
    book = epub.EpubBook()
    booksDir = settings['BooksDirectory']

    # Metadata
    book.set_title(title)
    book.set_language('en')
    book.add_author(info['author'])

    # Cover
    book.set_cover('cover.jpg', open(booksDir + info['title'] + '/cover.jpg', 'rb').read())

    # Empty Table of contents
    toc = {}

    # Chapter
    for chp in chapters:
        # Create chapter
        newChapter = epub.EpubHtml(title=chp['name'], file_name=chp['name'] + '.xhtml', lang='en')
        newChapter.content = u'<h1 align="center">' + chp['name'] + '\n</h1>' + \
                             (open(booksDir + info['title']+'/'+chp['name']+'.txt', 'r').read())

        # Add to book
        book.add_item(newChapter)

        # Add to table of contents
        if toc.get(chp['volume']) is None:
            toc[chp['volume']] = []

        toc[chp['volume']].append(newChapter)

    # Create table of contents
    book.toc = [(epub.Section(key), toc[key]) for key in toc.keys()]

    # Flatten Table of contents and create spine
    book.spine = ['nav'] + [chp for vol in toc.values() for chp in vol]

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(filename, book)
