from lib import pysmash
# init the wrapper class
smash = pysmash.SmashGG()

# All results are represented as normal Python dicts
# Convenience Method usage

# Shows a complete list of sets given tournament and event names
# This method ignores sets without a recorded score (Smash.gg "oddity". Either the set was not played or the set
# potentially fed into another bracket.)
print("Getting Sets")
sets = smash.tournament_show_sets('i-m-not-yelling-feat-armada', 'melee-singles')
print("Number of sets: ", len(sets))

print("Getting players") 
players = smash.tournament_show_players('i-m-not-yelling-feat-armada', 'melee-singles')
print("Number of players: ", len(players))

for set in sets:

	winner = loser = score = None

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

	# Check for DQ
	if len(score) != 3:
		print("DQ")
		continue

	# Get winner tag
	for player in players:
		#print(winner_id, ' --- ', player['entrant_id'])
		if winner_id == player['entrant_id']:
			winner = player['tag']

	# Get loser tag
	for player in players:
		if loser_id == player['entrant_id']:
			loser = player['tag']
			break



	print(winner + ","+score+"," + loser)