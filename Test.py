import Utils

# info = Utils.dumpInfo('https://www.readlightnovel.org/magis-grandson-1/')
#
# for i in range(6):
#     Utils.dumpChapterText(info, i)
#
# Utils.dumpCover(info)

# info = Utils.loadInfo("Magi's Grandson")
#
# chapters = []
#
# for i in range(6):
#     chapters.append(info['chapters'][i])
#
# Utils.generateEPUB('test.epub', "Magi's Grandson 1-6", info, chapters)

# print(Utils.loadSettings())
#settings = Utils.defaultSettings()

# import cfscrape
#
# scraper = cfscrape.create_scraper()
# x = scraper.post('https://www.readlightnovel.org/search/autocomplete', data='q=kenja',
#              headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#                       "X-Requested-With": "XMLHttpRequest"}).content

settings = Utils.loadSettings()
print(Utils.search('Kenja no', settings))
