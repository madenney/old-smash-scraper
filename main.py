# Main.py 

print("hello World")

import tournamentScraper
import matchScraper
import dataCleaner
from scrapers import smashggScraper

smashggScraper.getTournaments()
exit()

cleaner = dataCleaner.DataCleaner()
x = tournamentScraper.Tournaments(5, cleaner) # have to put a number there as the date. Will get back to this soon.
x.clean()
x.scrape()


y = matchScraper.Matches(cleaner)
y.scrape()