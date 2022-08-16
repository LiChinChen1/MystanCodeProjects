"""
File: boggle_extension.py
Name: Chin
----------------------------------------
1. Ask user to input 4 words split by space in a line 4 times, to create a boggle game.
	1-1. If user input over 4 words or doesn't split by space between words
		, program will print "Illegal input." and quit the program.
2. The program will sequentially select the initial position and perform the recursion to find the string in dictionary.
3. Print the result found in dictionary.
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
EXIT = -1
BOGGLE_SIZE = 4


def main():
	"""
	1. Ask user to input 4 words split by space in a line 4 times, to create a boggle game.
		1-1. If user input over 4 words or doesn't split by space between words
			, program will print "Illegal input." and quit the program.
	2. The program will sequentially select the initial position and perform the recursion to find the string in dictionary.
	3. Print the result found in dictionary.
	"""
	dic = read_dictionary()
	times = 1
	boggle_dic = {}

	print('Welcome to stanCode \"Boggle Generator\" (or -1 to quit)')

	# Create Boggle list from input string.
	while True:
		if times < BOGGLE_SIZE + 1:											# Check input times
			boggle = input(f'{times} row of letters: ').lower().strip()		# Change lower-case and strip space in the end

			if len(boggle.split(" ")) != BOGGLE_SIZE:			# Check boggle game size, and space
				print('Illegal input.')
				quit()

			for word in boggle.split(" "):						# Check input word is alpha
				if len(word) != 1 or not word.isalpha():
					print('Illegal input.')
					quit()

				boggle_dic[times] = boggle.split(" ")			# Create boggle dictionary
			times += 1
		else:
			break
	start = time.time()
	# Find the word in dictionary by recursion.

	# Total num = 4 x 4 = 16 個初始位置
	start_position_lst = []
	boggle_answer = []
	for x in range(1, BOGGLE_SIZE + 1):
		for y in range(1, BOGGLE_SIZE + 1):
			if (x, y) not in start_position_lst:   # 確認是否是已經執行過的初始位置
				start_position_lst.append((x, y))  # 紀錄選擇的初始位置
				boggle = find_boggle(s=boggle_dic, current_s=boggle_dic[x][y-1], current_lst=[(x, y)], answer_lst=[],
										dic=dic, current_position=(x, y))
				boggle_answer.extend(boggle)

	print(f'{len(boggle_answer)} anagrams : {boggle_answer}')

	end = time.time()
	print('----------------------------------')
	print(f'The speed of your boggle algorithm: {end - start} seconds.')


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""

	dic = []
	start_with_dic = []
	with open(FILE, 'r') as f:
		for line in f:
			if len(line.strip()) >= 4:
				dic.append(line.strip())
				for i in range(len(line)-1):
					start_with_dic.append(line[:i+1])      # start with in dictionary

	return set(dic), set(start_with_dic)


def find_boggle(s, current_s, current_lst, answer_lst, dic, current_position):
	prefix = has_prefix(current_s, dic)		# Check current string start with alpha in history dictionary
	if not prefix:
		return
	else:
		# Current num
		explore_dir = find_explore_dir(position=(current_position[0], current_position[1]), history_path=current_lst)
		print('explore_dir : ', explore_dir)
		for position in explore_dir:
			print('position: ', current_position)
			x1 = position[0]  # x-coordinate of explore dir.
			y1 = position[1]  # y-coordinate of explore dir.

			# choose
			current_lst.append((x1, y1))
			current_s += s[x1][y1-1]
			print('current lst :', current_lst)
			print('current str :', current_s)
			print('----------------------------------')

			# explore
			find_boggle(s, current_s, current_lst, answer_lst, dic, (x1, y1))

			# Un-choose
			current_lst.pop()
			current_s = current_s[:-1]

			# 回程再把答案記進去
			if current_s in dic[0] and current_s not in answer_lst:  # Unique
				print('--------------------------------------------')
				print(f'Searching...')
				print(f'Found: {current_s}')
				print('--------------------------------------------')
				answer_lst.append(current_s)

	return answer_lst


def has_prefix(sub_s, dic):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:param dic: (tuple) A tuple that contains two word dictionary: Answer dictionary and History dictionary.
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	if sub_s in dic[1]:
		return True
	return False


def find_explore_dir(position, history_path):
	x = position[0]
	y = position[1]
	lst = []
	for i in range(x-1, x+2, 1):
		for j in range(y-1, y+2, 1):
			if BOGGLE_SIZE >= i > 0 and BOGGLE_SIZE >= j > 0 \
					and (i, j) not in history_path and (i, j) != position:		# 處理邊界 & 現在位置
				lst.append((i, j))
	return lst


if __name__ == '__main__':
	main()
