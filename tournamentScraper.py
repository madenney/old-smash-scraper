# Tournaments Scraper

# This is used for getting the list of tournaments and tournament info
import tournamentObject
from scrapers import smashboards


class Tournaments(object):

	def __init__(self, date, cleaner):
		print("Initialize Tournaments Object")

		self.date = date
		self.cleaner = cleaner

		# Get array of unscraped tournaemnts 
		self.unscraped = []
		with open("archive/unscraped_tournaments.txt", "r") as file:
			for line in file:
				self.unscraped.append(tournamentObject.Tournament(line))


		print("Current Number of Unscraped Tournaments: ", len(self.unscraped))
		# Get array of already scraped tournaemnts 
		self.scraped = []
		with open("archive/tournaments.txt", "r") as file:
			for line in file:
				self.scraped.append(tournamentObject.Tournament(line))


	def clean(self):
		for t in self.unscraped:
			self.cleaner.removeCityStateQuotations(t)
			

	def scrape(self):
		print("Tournaments scrape()")
		# Start with smashboards
		smashboards.Smashboards()
		# Then smash.gg
		# Put names into archive
		print("Current Number of Unscraped Tournaments: ", len(self.unscraped))
		with open("archive/unscraped_tournaments.txt", "w") as file:
			for t in self.unscraped:
				file.write(t.getString())