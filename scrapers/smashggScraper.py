# smashggScraper.py

from lib import pysmash
# init the wrapper class
smash = pysmash.SmashGG()


def scrape(tournament, cleaner):
	print("Smashgg Scrape: " + tournament.name)

	# Declare variable that will be returned
	newMatches = []

	# Get link from tournament object
	link = tournament.link

	# Get smashgg tournament name out of link
	gglink = link[link.index('smash.gg/tournament')+20:]
	if '/' in gglink:
		gglink = gglink[:gglink.index('/')]
	print(gglink)

	print("Getting Sets")
	try:
		keyword = 'melee-singles'
		try:
			sets = smash.tournament_show_sets(gglink, keyword)
		except pysmash.exceptions.ValidationError:
			keyword = 'super-smash-bros-melee-singles'
			try:
				sets = smash.tournament_show_sets(gglink, keyword)
			except pysmash.exceptions.ValidationError:
				keyword = 'melee-singles-1'
				try:
					sets = smash.tournament_show_sets(gglink, keyword)
				except pysmash.exceptions.ValidationError:
					keyword = 'melee-singles-2'
					try:
						sets = smash.tournament_show_sets(gglink, keyword)
					except pysmash.exceptions.ValidationError:
						keyword = 'super-smash-bros-melee'
						sets = smash.tournament_show_sets(gglink, keyword)

		print("Number of sets: ", len(sets))

		print("Getting players") 
		players = smash.tournament_show_players(gglink, keyword)
		print("Number of players: ", len(players))

	except (KeyError, pysmash.exceptions.ResponseError) as err:
		with open('archive/error_log.txt', "a") as file:
			string = "smashggScraper Error. Tournament - " + tournament.name
			file.write(string + '\n')
			return False


	for set in sets:

		winner = loser = score = winner_score = loser_score = None

		winner_id = int(set['winner_id'])
		loser_id = int(set['loser_id'])

		if(winner_id == int(set['entrant_1_id'])):
			winner_score = str(set['entrant_1_score'])
			loser_score = str(set['entrant_2_score'])
			score = winner_score + "-" + loser_score
		else:
			winner_score = str(set['entrant_2_score'])
			loser_score = str(set['entrant_1_score'])
			score = winner_score + "-" + loser_score

		# If no score was kept
		if(winner_score == 'None' and loser_score == 'None'):
			score = 'x-x'

		# Check for DQ
		if len(score) != 3:
			print("DQ")
			continue

		# Get winner tag
		for player in players:
			#print(winner_id, ' --- ', player['entrant_id'])
			if winner_id == player['entrant_id']:
				winner = player['tag']
				winner = cleaner.cleanName(winner)
				break

		# Get loser tag
		for player in players:
			if loser_id == player['entrant_id']:
				loser = player['tag']
				loser = cleaner.cleanName(loser)
				break

		try:
			output = winner + ',' +loser + ',' + score + ',' + tournament.name
		except TypeError:
			print("An error occured. Skipping this match.")
			with open('archive/error_log.txt', "a") as file:
				string = "smashggScraper typeError. Tournament - " + tournament.name
				if(winner != None):
					string += " player -" + winner
				if(loser != None):
					string += " player -" + loser
				file.write(string + '\n')
			continue

		print(output)
		newMatches.append(output)

	if len(newMatches) > 0:
		return newMatches
	else:
		return False






def getTournaments():


	import requests
	import re
	from BeautifulSoup import BeautifulSoup

	# https://smash.gg/tournaments?per_page=30&filter=%7B%22name%22%3A%22%22%2C%22past%22%3Atrue%2C%22upcoming%22%3Afalse%7D&page=1

	maxPage = 2 # find a way to get this number


	urlBase = "https://smash.gg/tournaments?per_page=30&fipoopC%22past%22%3Atrue%7D&page="

	for i in range(1,maxPage):

		url = urlBase + str(i)

		# Do request
		# try:
		# 	data = requests.get(url).text
		# except ChunkedEncodingError:
		# 	print("Error with tournament: " + tournament.name)
		# 	return False

		print url
		data = requests.get(url).text
		print data
		with open('requesttest.txt','w') as file:
			file.write(data)
		soup = BeautifulSoup(data)

		divs = soup.findall("div", {"class" : "TournamentCardContainer"})
		print len(divs)
		# m = re.findall('aria-label="(.*?)\"', input)
