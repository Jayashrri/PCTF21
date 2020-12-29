from random import randrange
from sympy import isprime
import hashlib
import os

def rand_prime(digits) :
	lower = 10**(digits - 1)
	upper = 10*lower

	prime = randrange(lower, upper)
	while not isprime(prime) :
		prime = randrange(lower, upper)

	return prime

def ask_questions(sequence) :
	count = 0
	for num in sequence :
		factor = 1
		correct_response = 'y'
		
		if num == '1' :
			factor = randrange(2, 10)
			correct_response = 'n'
				
		prime = factor*rand_prime(38)
		response = input(f"\n  {prime}  :  ")
		
		if not response.lower() == correct_response :
			break

		count += 1
		
	f.close()
	return (count == len(sequence))
	
def sha256(message) :
	return hashlib.sha256(message.encode()).digest().hex()

M = 310717010502520989590157367261876774703
G = (179210853392303317793440285562762725654, 105268671499942631758568591033409611165)
P = (280810182131414898730378982766101210916, 291506490768054478159835604632710368904)

print("\n  " + "*"*50)
print(f"\n  M = {M}\n  G = {G}\n  P = {P}\n")
print("  Sorry we forgot to tell you curve parameters :(\n")
print("  Well, now is an opportunity.\n")
print("  " + "*"*50)
print("\n  Are the given numbers prime? (y/n)\n")
print("  " + "*"*50)

script_dir = os.path.dirname(os.path.realpath(__file__))

f = open(script_dir + '/flag.txt', 'r')

try :
	sequence = ''.join('{:08b}'.format(ord(ch)) for ch in f.readline().strip())
	assert ask_questions(sequence)

	answer = sha256(input("\n  SECRET KEY (hex) : "))
	assert (answer == sha256(f.readline().strip()))

	print(f"\n  Here is your flag : {f.readline().strip()}\n")
		
except AssertionError :
	print("\n  OOPS! Try again.\n")

f.close()

