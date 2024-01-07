import os
import time
import random
import string

def tumbler(text):
	buffer = [''] * len(text)
	while True:
		done = True
		for i in range(len(buffer)):
			if text[i] == '\t':
				buffer[i] = '\t'
			elif text[i] == '\n':
			    buffer[i] = '\n'
			elif text[i] != buffer[i]:
				code = ord(text[i])
				rand = random.randint(max(0, code - 2), code + 2)
				buffer[i] = chr(rand)
				done = False
		if done:
			print(text, end='\r')
			break
		print(''.join(buffer), end='\r')
		time.sleep(0.06)

# text = "ASCII Text is fascinating isnt it!
tumbler("text here written")

time.sleep(3)
tumbler("other text here  ")

time.sleep(3)
