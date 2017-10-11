# smashgg.py
from BeautifulSoup import BeautifulSoup
import requests
import dataCleaner

# Copied from stackoverflow. Find nth occurrence of substring in string
def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

# Extract name from this annoying html element
def extractName(string):
	# The next line is what the string looks like when it comes in
	#<span class="match-player-name-container" data-reactid="358"><span class="prefix text-muted" data-reactid="359">RNG</span><!-- react-text: 360 --> <!-- /react-text --><!-- react-text: 361 -->Swedish Delight<!-- /react-text --></span>
	name = string[findnth(string, "<!-- react-text", 1) :]
	name = name[ str.index(name, ">") + 1 : findnth(name, "<!--", 1)]
	name = dataCleaner.cleanName(name)
	return name

def scrape(tournament):
	print("Smashgg Scrape: " + tournament.name)

	# Declare variable that will be returned
	newMatches = []

	# Get link from tournament object
	link = tournament.link

	# Create api call from tournament link
	apiCall = link[:findnth(link, "/", 4)] + "?expand[]=groups"
	apiCall = apiCall.replace("smash.gg", "api.smash.gg")
	
	# Do api call
	response = requests.get(apiCall)
	obj = response.json()


	# Make sure the loop will work
	try:
		x = obj['entities']['groups']
	except KeyError:
		print("Error with " + tournament.name)
		return False


	# Loop through all phase groups
	for group in obj['entities']['groups']:

		matchDivs = []
		isRoundRobin = False
		stop = False
		urlVersions = ["melee-singles", "super-smash-bros-melee", "melee-singles-1", "melee-singles-2", "stopper"]
		for urlVersion in urlVersions:

			# Check for stopper
			if( urlVersion == "stopper"):
				stop = True
				break

			# Create url for next api call
			url = link[:findnth(link, "/", 4)] + "/events/" + urlVersion + "/brackets/" + str(group['phaseId']) + "/" + str(group['id'])
		
			# Do api call and create soup from it
			try:
				data = requests.get(url).text
			except ChunkedEncodingError:
				print("Error with tournament: " + tournament.name)
				return False
			soup2 = BeautifulSoup(data)

			# Get all matches from soup
			matchDivs = soup2.findAll("div", {"class" : "match-affix-wrapper"})

			# If there are no matches-affix-wrappers on this page
			if(len(matchDivs) == 0):
				# If its a round robin table 
				roundRobin = soup2.findAll("div", {"class" : "round-robin-table"})
				if(len(roundRobin) > 0):
					isRoundRobin = True
					break
			else:
				break


		# If this url ended up being worthless
		if(stop == True):
			print("Worthless URL = " + url)
			continue

		# Extract info from Round Robin Table
		if(isRoundRobin == True):
			print("Round Robin: ")

			# Get rows from table
			rows = roundRobin[0].findAll("div", {"class" : "rr-row"})

			# Get names from each row
			nameContainers = rows[0].findAll("span", {"class" : "match-player-name-container"})
			names = []
			for container in nameContainers:
				names.append(extractName(str(container)))
			
			# Iterate through table
			for i in range(1, len(names)):

				# Start with first child of row, then step through siblings
				col = rows[i].div
				for step in range(i):
					col = col.nextSibling
				for j in range(i + 1, len(names) + 1):
					col = col.nextSibling

					# Get score from score div
					score = col.find("div", {"class" : "score"}).text

					# Check for DQ
					if("DQ" in score):
						print("DQ")
						continue

					# Extract score values from text
				  	score1 = score[0]
				  	score2 = score[len(score)-1]

				  	# Check for winner and loser
					if("winner" in col["class"]):
						winner = names[i-1]
						loser = names[j-1]
					elif ("loser" in col["class"]):
						winner = names[j-1]
						loser = names[i-1]
						temp = score1
						score1 = score2
						score2 = temp
					else:
						continue

					# Clean names, create output string, and append it to the matches
					winner = dataCleaner.cleanName(winner)
					loser = dataCleaner.cleanName(loser)
					# Skip this match if the name is too shitty
					if(winner == False or loser == False):
						continue
					score = score1 + "-" + score2
					output = winner + "," + loser + "," + score + "," + tournament.name
					print(output)
					newMatches.append(output)

			continue

		# Loop through all matches on this page
		print("Matches on this page: " + str(len(matchDivs)))
		for matchdiv in matchDivs:

			# Check for DQ
			dqs = matchdiv.findAll("div", {"class" : ["match-player entrant loser dq", "match-player entrant loser missing dq"]})
			if(len(dqs) > 0):
				print("DQ")
				continue
			# if('class="text-dq"' in str(matchdiv)):
			# 	print("DQ")
			# 	continue

			# Check for byes
			byes = matchdiv.findAll("div", {"class" : ["match-player bye"]})
			if(len(byes) > 0):
				print("Bye")
				continue

			# Get the winner from the match div, extract name and score value
			winner = matchdiv.find("div", {"class" : ["match-player entrant winner", "match-player entrant winner missing"]})
			try:
				winnerName = extractName(str(winner.find("span", {"class" : "match-player-name-container"})))
			except AttributeError:
				print("Attribute Error")
				continue
			winnerScoreContainer = winner.findAll("div", {"class" : "match-player-info"})
			# If there was an empty score, then look for the empty score class (when it includes status-bar)
			if(len(winnerScoreContainer) == 0):
				winnerScoreContainer = winner.findAll("div", {"class" : "match-player-info status-bar"})
				if(len(winnerScoreContainer) == 0):
					# This is here in case of weird things happening
					print("Whats going on here: ", winner.text)
					winnerScore = "x"
				else:
					winnerScore = "x" 
			else:
				winnerScore = str(winnerScoreContainer[0].text)

			
			# Get the loser from the match div, extract name and score value
			loser = matchdiv.find("div", {"class" : ["match-player entrant loser", "match-player entrant loser missing"]})
			loserName = extractName(str(loser.find("span", {"class" : "match-player-name-container"})))
			loserScoreContainer = loser.findAll("div", {"class" : "match-player-info"})
			# If there was an empty score, then look for the empty score class (when it includes status-bar)
			if(len(loserScoreContainer) == 0):
				loserScoreContainer = loser.findAll("div", {"class" : "match-player-info status-bar"})
				if(len(loserScoreContainer) == 0):
					# This is here in case of weird things happening
					print("Whats going on here: ", loser.text)
					loserScore = "x"
				else:
					loserScore = "x" 
			else:
				loserScore = str(loserScoreContainer[0].text)
			
			score = winnerScore + "-" + loserScore

			# Skip this match if the name is too shitty
			if(winnerName == False or loserName == False):
				continue

			output = winnerName + "," + loserName + "," + score + "," + tournament.name

			print(output)
			newMatches.append(output)




	if(len(newMatches) > 0):
		return newMatches
	else:
		return False 
