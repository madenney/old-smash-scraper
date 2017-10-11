# facebookScraper.py

import re



def scrape():

	groups = []
	with open('archive/fb_groups.txt','r') as file:
		for line in file:
			l = line.split(",")
			l[1] = l[1].replace("\n","")
			groups.append(l)

	
	# ok so this failed












# This is a one time use function
# Not really real scraping

# Explanation:
# Went onto Jim Gray fb page, manually copied HTML of the list of groups
# Save that html into a file and have this function run on it to extract the group names and id's
# It saves that to an output file specified

def groupScraper(inputFile, outputFile):

	print("Facebook Group Scraper")

	finalData = []

	with open(inputFile, 'r') as file:
		input = file.read()
	
	
	m = re.findall('aria-label="(.*?)\"', input)

	nameCount = 0
	for item in m:
		nameCount += 1
		finalData.append([item])

	m = re.findall('data-hovercard=\"/ajax/hovercard/hovercard.php\?id=(.*?)\"', input)

	idCount = 0
	for i in range(0, len(finalData)):
		finalData[i].append(m[i])
		idCount += 1


	with open(outputFile, 'w') as file:
		for f in finalData:
			while "," in f[0]:
				f[0] = f[0].replace(","," ")


			line = f[0] + "," + f[1]
			print line
			line += "\n"
			file.write(line)



