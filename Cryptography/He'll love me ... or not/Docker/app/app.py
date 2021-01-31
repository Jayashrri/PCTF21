#!/usr/local/bin/python3
from random import randrange
from sympy import isprime
from os.path import dirname, realpath, join
from json import load
from signal import SIGINT, signal
import sys

class EllipticCurve:

	def __init__(self, field_order, params):
		self.a, self.b = params
		self.M = field_order

	def set_point(self, xy):
		if not (xy[1]**2) % self.M == (xy[0]**3 + self.a*xy[0] + self.b) % self.M:
			raise Exception(f'No such point {xy} lies on the curve.')
		return Point(xy, self)

class Point:

	def __init__(self, xy, curve):
		self.x, self.y = xy
		self.curve = curve

	def extended_euclid(self, a, b):
		if not a:
			return (0, 1, b)
		p, q, r = self.extended_euclid(b % a, a)
		q = q - (b//a)*p
		return (q, p, r)

	def inverse_mod(self, a, m):
		p, q, r = self.extended_euclid(a, m)
		if not r == 1:
			raise Exception(f'Modular inverse of {a} mod {m} doesn\'t exist.')
		return p % m

	def double(self):
		slope = (3*(self.x**2) + self.curve.a) % self.curve.M
		slope *= self.inverse_mod(2*self.y, self.curve.M)
		slope %= self.curve.M
		_x = (slope**2 - 2*self.x) % self.curve.M
		_y = (-self.y - slope*(_x - self.x)) % self.curve.M
		return Point((_x, _y), self.curve)

	def __add__(self, P):
		try:
			assert self.curve.M == P.curve.M
			assert self.curve.a == P.curve.a
			assert self.curve.b == P.curve.b
			if (self.x, self.y) == (P.x, P.y):
				return P.double()
			sign = 1 if P.x < self.x else -1
			slope = (sign*(self.y - P.y)) % self.curve.M
			slope *= self.inverse_mod(sign*(self.x - P.x), self.curve.M)
			slope %= self.curve.M
			_x = (slope**2 - self.x - P.x) % self.curve.M
			_y = (-self.y - slope*(_x - self.x)) % self.curve.M
			return Point((_x, _y), self.curve)
		except AssertionError:
			raise Exception('Addition is defined only for points lying on the same curve.')

	def multiply(self, n):
		result = None
		addend = self
		while n:
			if n & 1:
				if not result:
					result = addend
				else:
					result += addend
			n = n >> 1
			addend = addend.double()
		return result

	def xy(self):
		return (self.x, self.y)


class Challenge:

	def __init__(self, field_order, params, generator, public_key, url):
		self.curve = EllipticCurve(field_order, params)
		self.G = self.curve.set_point(generator)
		self.P = self.curve.set_point(public_key)
		self.url = url

	def random_prime(self, digits):
		lower = 10**(digits - 1)
		upper = 10*lower
		prime = randrange(lower, upper)
		while not isprime(prime):
			prime = randrange(lower, upper)
		return prime

	def ask_questions(self, sequence):
		count = 0
		for bit in sequence:
			factor, correct = (randrange(2, 10), 'n') if bit == '1' else (1, 'y')
			prime = factor*self.random_prime(38)
			response = input(f"\n{prime} :  ")
			if not response.lower() == correct:
				break
			count += 1
		return count == len(sequence)

	def welcome(self):
		print("*"*50)
		print("Sorry we forgot to tell you curve parameters:(")
		print("Well, now is an opportunity.")
		print("Just answer the following questions and you shall get what you seek.")
		print("Are the given numbers prime? (y/n)")
		print("*"*50)

	def endgame(self):
		print("\nLOL did you seriously think we would give up the flag that easy?")
		print(f"Hurry up {self.url}")

	def run(self):
		self.welcome()
		sequence = ''.join('{:08b}'.format(ord(ch)) for ch in f'Here you go, a = {self.curve.a}')
		try:
			assert self.ask_questions(sequence)
			answer = int(input(f'\nSECRET KEY (hex): '), 16)
			assert self.P.xy() == self.G.multiply(answer).xy()
			self.endgame()
		except AssertionError:
			print("\nOOPS! Keep trying ...\n")

def handler(sig, frame):
	sys.exit(0)

def main():
	cwd = dirname(realpath(__file__))
	config_file = join(cwd, 'config.json')
	data = load(open(config_file, 'r'))
	data = [data[i] for i in data.keys()]

	signal(SIGINT, handler)
	Challenge(*data).run()


if __name__ == '__main__':
	main()
