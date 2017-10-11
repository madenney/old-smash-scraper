# test.py


import dataCleaner

with open("archive/testname.txt", "r") as file:
	for line in file:
		x = line

print x

for char in x:
	print(str(char) + " " + str(ord(char)))

arr = list(x)
print(arr)
for a in arr:
	if(ord(a) == 195 or ord(a) == 226 or ord(a) == 194):
		print("unicode letter found")

		# Check for tm sign
		if(ord(arr[arr.index(a) + 1]) == 132 and ord(arr[arr.index(a) + 2]) == 162):
			index = arr.index(a)
			arr.pop(index)
			arr.pop(index)
			arr.pop(index)
			continue
		if(ord(arr[arr.index(a) + 1]) in [128, 129, 130, 131, 132, 133]):
			arr[arr.index(a) + 1] = "A"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [134]):
			arr[arr.index(a) + 1] = "AE"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [136, 137, 138, 139]):
			arr[arr.index(a) + 1] = "E"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [140, 141, 142, 143]):
			arr[arr.index(a) + 1] = "I"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [144]):
			arr[arr.index(a) + 1] = "D"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [146, 147, 148, 149, 150]):
			arr[arr.index(a) + 1] = "O"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [153, 154, 155, 156]):
			arr[arr.index(a) + 1] = "U"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [160, 161, 162, 163, 164, 165]):
			arr[arr.index(a) + 1] = "a"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [166]):
			arr[arr.index(a) + 1] = "ae"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [168, 169, 170, 171]):
			arr[arr.index(a) + 1] = "e"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [172, 173, 174, 175]):
			arr[arr.index(a) + 1] = "i"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [176]):
			arr[arr.index(a) + 1] = " "
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [177]):
			arr[arr.index(a) + 1] = "n"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [178, 179, 180, 181, 182]):
			arr[arr.index(a) + 1] = "o"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [184]):
			arr[arr.index(a) + 1] = "o"
			arr.pop(arr.index(a))
		elif(ord(arr[arr.index(a) + 1]) in [185, 186, 187, 188]):
			arr[arr.index(a) + 1] = "u"
			arr.pop(arr.index(a))

		# Figure this out later
		# elif(ord(arr[arr.index(a) + 1]) in [132]):
		# 	# This is for the tm sign. Just get rid of it. Don't replace
		# 	index = arr.index(a)
		# 	arr.pop(index)
		# 	arr.pop(index)
		# 	arr.pop(index)


x = ""
for a in arr:
	x += a
print x