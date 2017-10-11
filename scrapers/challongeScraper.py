# challonge.py

# Using the challonge API python wrapper, created by -russ
# Get the list of participants and the list of matches
# Loop through matches, get participants IDs, and use participants list to match to their display names
# Get the score, check for errors in scorekeeping
# Create final string

from BeautifulSoup import BeautifulSoup
import requests
from lib import challonge

def scrape(tournament, cleaner):
	print("Challonge Scrape:  " + tournament.name)

	newMatches = []

	# Start the challonge api wrapper
	challonge.set_credentials("madmattstats", "rK5Qd346EsIekQHQtkWFpfUg7r5RCHQbyAH3JO6K")

	# Get link from tournament object
	link = tournament.link

	# Try to get subdomain, if none exists, then make it an empty string
	try:
		subdomain = link[ link.index("//") + 2 : link.index(".challonge")] + "-"
	except ValueError:
		subdomain = ""
	# Get tourney url
	tourneyURL = link[ link.index(".com/") + 5 :-2]
	url = subdomain + tourneyURL


	# Get participants
	participantsApiCall = "https://madmattstats:rK5Qd346EsIekQHQtkWFpfUg7r5RCHQbyAH3JO6K@api.challonge.com/v1/tournaments/" + url + "/participants.json"
	try:
		players = requests.get(participantsApiCall).json()
	except ValueError:
		return False
	# Get matches
	matchesApiCall = "https://madmattstats:rK5Qd346EsIekQHQtkWFpfUg7r5RCHQbyAH3JO6K@api.challonge.com/v1/tournaments/" + url + "/matches.json"
	matches = requests.get(matchesApiCall).json()

	# Loop through matches
	for match in matches:

		try:
			# If match is not complete, then skip
			if(match['match']['state'] != "complete"):
				print("Incomplete Match")
				break
		except TypeError:
			print("Error: TypeError at " + tournament.name)
			break

		# Get info from match object
		player1ID = match['match']['player1_id']
		player2ID = match['match']['player2_id']
		score = match['match']['scores_csv']

		# Find matching playerID in participants list and then get display name from that
		player1 = None
		player2 = None
		for player in players:
			if(player['participant']['id'] == player1ID):
				player1 = player['participant']['display_name']
			if(player['participant']['id'] == player2ID):
				player2 = player['participant']['display_name']
			if(player1 != None and player2 != None):
				break

		# Skip if there was no matching ID
		if(player1 == None or player2 == None):
			continue

		# Clean names
		player1 = cleaner.cleanName(player1)
		player2 = cleaner.cleanName(player2)

		# Skip this match if the name is too shitty
		if(player1 == False or player2 == False):
			continue

		# If the first score is negative then its a DQ
		if(score[0] == "-"):
			print("DQ")
			continue

		# Extract scores from score
		score1 = score[:score.index("-")]
		score2 = score[score.index("-")+1:]
		
		# If the second score is negative, then its a DQ
		if(int(score2) < 0):
			print("DQ")
			continue

		# Assign winner and create final score
		if(int(score1) > int(score2)):
			winner = player1
			loser = player2
			score = score1 + "-" + score2
		else:
			winner = player2
			loser = player1
			score = score2 + "-" + score1

		# Put this here to account for idiots who put stuff like 9000-0 for score
		if len(score) > 3:
			score = "x-x"

		output = winner + "," + loser + "," + score + "," + tournament.name
		print(output)
		newMatches.append(output)



	if(len(newMatches) > 0):
		return newMatches
	else:
		return False
	
