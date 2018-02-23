
mod = 1e7

def factorial(num):
	if num == 0:
		return 1
	else:
		return num * factorial(num-1)


def choose(num, pick):
	num = float(num)
	difference = num - pick
	numerator = 1
	if difference > pick:
		while num > difference:
			numerator *= num
			numerator %= mod
			num -= 1
		return numerator/factorial(pick)

	else:
		while num > pick:
			numerator *= num
			num -= 1
		return (numerator/factorial(difference))%mod


def calcPascal(num):
	num = float(num)
	row = []
	index = 0
	while index < num/2:
		row.append(choose(num, index))
		index+=1

	for each in row:
		print(int(each), end=" ")
	if num % 2 == 0:
		print(int(choose(num,index)), end = " ")
	for i in reversed(row):
		print(int(i), end=" ")

	print()





numTests = input()
numbers = []

for i in range(int(numTests)):
	temp = input()
	calcPascal(temp)


