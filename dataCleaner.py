# dataCleaner.py


import re

class DataCleaner(object):


	def __init__(self):
		print("Initializing Data Cleaner")

		aliases = []
		with open("archive/aliases.txt","r") as file:
			for line in file:
				line = line[:-2].split(",")
				aliases.append(line)
		self.aliases = aliases

		sponsors = []
		with open("archive/sponsors.txt","r") as file:
			for line in file:
				sponsors.append(line[:-2])
		self.sponsors = sponsors

	# Take a line and an expected number of commas, returns true if number of commas in line matches expected number
	def checkCommas(self, line, numExpectedCommas):
		if line.count(",") == numExpectedCommas:
			return True
		else:
			return False


	# Remove quotation marks from city and state
	def removeCityStateQuotations(self, tourneyObj):
		tourneyObj.city = tourneyObj.city.replace('"',"")
		tourneyObj.state = tourneyObj.state.replace('"',"")


	# For cleaning individual player names
	def cleanName(self, string):

		# Check for apostrophes and commas
		string = string.replace("&#x27;", "'")
		string = string.replace(",", " ")


		# Remove sponsors tag
		# start by removing things before |
		while "|" in string:
			string = string[string.index("|")+1:]

		# Get rid of the space in the first index
		while string[0] == " " or string[0] == "\t":
			string = string[1:]


		# Check for things like (p1) or [#5] or (pool1)
		p = re.compile(".*([\(\[][Ppol#0-9. \-]{1,6}[\)\]]).*")
		m = p.match(string)
		while m:
			string = string[:string.index(m.group(1))] + string[string.index(m.group(1))+ len(m.group(1)):]
			m = p.match(string)


		# Get rid of sponsors inside of brackets like [CLG]
		p = re.compile(".*(\[.{2,10}\]).*")
		m = p.match(string)
		if m:
			string = string[:string.index(m.group(1))] + string[string.index(m.group(1))+ len(m.group(1)):]


		# look for sponsors in front
		for sponsor in self.sponsors:
			# Do regex to look for sponsor in the beginning of the string
			p = re.compile("^("+sponsor.lower()+"[. _])(.{2,})")
			m = p.match(string.lower())
			if m:
			    string = string[string.lower().index(m.group(2).lower()):]
			
			# Check for sponsor post-regex and add to warnings if its still there
			p = re.compile("^ *"+sponsor.lower())
			m = p.match(string.lower())
			if m:
			    with open('archive/warning_log.txt','a') as file:
			    	file.write("Name Clean Warning: " + string + "\n")


		# Check for aliases
		for aliasList in self.aliases:
			for i in range(1,len(aliasList)):
				if aliasList[i].lower() == string.lower():
					string = aliasList[0]

		# Get rid of extra spaces
		while "  " in string:
			string = string.replace("  ", " ")

		while string[0] == " ":
			string = string[1:]

		while string[len(string)-1] == " ":
			string = string[:-1]


		return string


	def cleanTournament(self, matches, tournament):
		

		# Check if all names in each match start with the same symbol or all start with a number
		# for tournaments where players are like this: 1-2 Axe or #1 Hugs 
		p = re.compile("^[#0-9.\- \t]")
		allFirstIndicesMatch = True
		nonMatchCount = 0
		for match in matches:
			m = p.match(match)
			if not m:
				nonMatchCount += 1
				# If more than half of the matches don't follow the pattern, then break
				if nonMatchCount > len(matches)/2:
					allFirstIndicesMatch = False
					break


		if allFirstIndicesMatch == True:

			# Add to warning file
			with open('archive/warning_log.txt','a') as file:
				file.write("Tournament Warning: " + tournament.name + "\n")


			newMatches = []
			for match in matches:
				newMatches.append(match.split(","))

			# Have to look out for the top bros with annoying names
			exceptions = ["%4","42nd",".jpg","999","1der","47","007","23"]

			# While there are still extra characters on the front of the string
			while self.checkFirstIndexOfPlayers(newMatches) == True:
				for match in newMatches:
					m = p.match(match[0])
					if m and match[0] not in exceptions:
						match[0] = match[0][1:]
					m = p.match(match[1])
					if m and match[1] not in exceptions:
						match[1] = match[1][1:]

			matches = []
			for match in newMatches:
				match[0] = self.cleanName(match[0])
				match[1] = self.cleanName(match[1])

				matches.append(",".join(match))



		return matches



	def checkFirstIndexOfPlayers(self, matches):
		p = re.compile("^[#0-9.\- \t]")
		allMatch = True
		nonMatchCount = 0
		for match in matches:
			m = p.match(match[0])
			if not m:
				nonMatchCount += 1
				if nonMatchCount > len(matches)/2:
					allMatch = False
					break
			m = p.match(match[1])
			if not m:
				nonMatchCount += 1
				if nonMatchCount > len(matches)/2:
					allMatch = False
					break

		return allMatch