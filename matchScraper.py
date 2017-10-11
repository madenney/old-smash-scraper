
import time
import tournamentObject
from scrapers import smashggScraper
from scrapers import challongeScraper

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Matches(object):

	def __init__(self, cleaner):
		print("Initialize Matches Object")

		self.cleaner = cleaner

		# Define unscraped file (mostly here for easy testing)
		self.unscrapedFile = "archive/unscraped_tournaments.txt"

		# Get unscraped tournaments
		self.matches = []
		self.unscraped = []

		#with open("archive/unscraped_tournaments.txt", "r") as file:
		with open(self.unscrapedFile, "r") as file:
			for line in file:
				self.unscraped.append(tournamentObject.Tournament(line))


	def scrape(self):

		tournamentCount = 0
		matchesCount = 0
		firstTournament = None
		lastTournament = None


		# Open log and find last line
		log = []
		with open("archive/log.txt", "r") as file:
			for line in file:
				log.append(line)
		logLength = len(log)

		#Loop through tournaments and scrape each one
		for tournament in self.unscraped:
			
			newMatches = False
			print("Match Scraper: " + tournament.name)

			if not(hasattr(tournament, "link")):
				#Get the link somehow <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Do this later
				print(tournament.name + " does not have a link")

	
			if("smash.gg" in tournament.link):
				newMatches = smashggScraper.scrape(tournament, self.cleaner)

			if("challonge.com" in tournament.link):
				newMatches = challongeScraper.scrape(tournament, self.cleaner)

				
			# If matches we successfully scraped
			if(newMatches != False):

				# Run through the data cleaner
				newMatches = self.cleaner.cleanTournament(newMatches, tournament)

				# Add onto tournament count and match count
				tournamentCount +=1
				matchesCount += len(newMatches)

				# Write new line into tournaments file
				with open("archive/tournaments.txt", "a") as file:
					file.write(tournament.getString())

				# Write new lines into matches file
				with open("archive/matches.txt", "a") as file:
					for match in newMatches:
							file.write((match + "\n"))

				# Assign first and last tournaments for the log
				if(firstTournament == None):
					firstTournament = tournament
				lastTournament = tournament

				# Create the log string with today's date
				today = time.strftime("%d/%m/%Y")
				logOutput = today + ", " + firstTournament.name + ", " + str(tournamentCount) + ", " + lastTournament.name + ", " + str(matchesCount) + "\n"

				# If there is no new line in the log, then add one. If there is already a new line, then change that one
				if(len(log) == logLength):
					log.append(logOutput)
				else:
					log[len(log)-1] = logOutput

				# Write log to log file
				with open("archive/log.txt", "w") as file:
					for line in log:
						file.write(line)

				# Remove tournament from unscraped and update the file
				self.unscraped[self.unscraped.index(tournament)] = "X"

				#Clear file
				open(self.unscrapedFile, "w").close()

				# Write to file
				with open(self.unscrapedFile, "w") as file:
					for t in self.unscraped:
						if( t != "X"):
							file.write(t.getString())