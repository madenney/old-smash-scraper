# tournemnt.py


class Tournament(object):

	def __init__(self, string):

		arr = string.split(",");
		self.date = arr[0]
		self.name = arr[1]
		self.entrants = arr[2]
		self.city = arr[3]
		self.state = arr[4]
		self.region = arr[5]
		self.winner = arr[6]
		self.link = arr[7]


	def getString(self):
		string = self.date + "," + self.name + "," + self.entrants + "," + self.city + "," + self.state + "," + self.region + "," + self.winner + "," + self.link
		return string
