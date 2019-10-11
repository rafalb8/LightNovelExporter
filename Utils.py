import faster_than_requests as requests
from bs4 import BeautifulSoup
from ebooklib import epub
from os import makedirs, path
from unidecode import unidecode
from cfscrape import create_scraper
import json


# Function that generates ranges list
# https://stackoverflow.com/a/43884649
def ranges(ints):
    ints = sorted(set(ints))
    start = prev = ints[0]

    for number in ints[1:]:
        if number == prev + 1:
            prev = number
        else:
            yield start, prev
            start = prev = number

    yield start, prev


# Save Settings
def saveSettings(settings):
    json.dump(settings, open('settings.json', 'w'), indent=4)


# Load
def loadSettings():
    return json.load(open('settings.json'))


# Save json with default settings
def defaultSettings():
    settings = {'BooksDirectory': 'books',
                'MainURL': 'readlightnovel.org',
                'Search': '/search/autocomplete',
                'SearchHeaders': {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Requested-With": "XMLHttpRequest"
                    }
                }
    saveSettings(settings)


# Get Information about novel
def getInfo(url):
    # Make request and parse html
    body = requests.get2str(url)
    html = BeautifulSoup(body, 'lxml')

    # Get Info
    novel = html.find('div', class_='novel')
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
    bookDir = path.join(settings['BooksDirectory'], info['title'])

    try:
        makedirs(bookDir)
    except OSError:
        pass

    json.dump(info, open(path.join(bookDir, 'info.json'), 'w'), indent=4)
    return info


# Read JSON file
def loadInfo(title, settings):
    info = path.join(settings['BooksDirectory'], title, 'info.json')
    return json.load(open(info, 'r'))


def getChapterText(url):
    # Make request and parse html
    body = requests.get2str(url)
    html = BeautifulSoup(body, 'lxml')

    # Get text
    text = html.find('div', class_='desc')

    # Remove unwanted tags
    for script in text('script'):
        script.decompose()

    [x.decompose() for x in text('div', class_='hidden')]
    [x.decompose() for x in text('div', class_='col-lg-12 text-center')]

    # Remove formatting
    for attr in ['class', 'style', 'data-size']:
        del text[attr]

    return str(text)


# Save Chapter text
def dumpChapterText(info, idx, settings):
    bookDir = path.join(settings['BooksDirectory'], info['title'])
    try:
        makedirs(bookDir)
    except OSError:
        pass

    chapter = info['chapters'][idx]

    with open(path.join(bookDir, '{0}.{1}.html'.format(chapter['volume'], chapter['name'])), 'w') as f:
        f.write(getChapterText(info['chapters'][idx]['url']))


# Save cover
def dumpCover(info, settings):
    bookDir = path.join(settings['BooksDirectory'], info['title'])

    try:
        makedirs(bookDir)
    except OSError:
        pass

    requests.downloads(info['img'], path.join(bookDir, 'cover.jpg'))


def search(title, settings):
    # Prepare data for request
    data = 'q={0}'.format(title.replace(' ', '+'))
    headers = settings['SearchHeaders']
    url = 'https://www.{0}{1}'.format(settings['MainURL'], settings['Search'])
    scraper = create_scraper()

    # Send POST Request
    body = scraper.post(url, data=data, headers=headers).content
    html = BeautifulSoup(body, 'lxml')

    # Parse html
    results = []
    for b in html('li'):
        book = {'title': unidecode(b.text), 'img': b.img['src'], 'url': b.a['href']}
        results.append(book)

    return results

# Generate ePUB
def generateEPUB(filename, title, info, chapters, settings):
    # Create empty ePUB file
    book = epub.EpubBook()
    bookDir = path.join(settings['BooksDirectory'], info['title'])

    # Metadata
    book.set_title(title)
    book.set_language('en')
    book.add_author(info['author'])

    # Cover
    book.set_cover('cover.jpg', open(path.join(bookDir, 'cover.jpg'), 'rb').read())

    # Empty Table of contents
    toc = {}

    # Chapter
    for chp in chapters:
        # Create chapter
        newChapter = epub.EpubHtml(title=chp['name'], file_name=chp['name'] + '.xhtml', lang='en')
        newChapter.content = open(path.join(bookDir, '{0}.{1}.html'.format(chp['volume'], chp['name'])), 'r').read()

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
