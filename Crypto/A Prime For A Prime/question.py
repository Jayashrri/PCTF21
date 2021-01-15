import random
primes = "list of eight primes"
primes.sort()
seed_value = f"{primes[0]^primes[1]}~{primes[2]^primes[3]}~{primes[4]^primes[5]}~{primes[6]^primes[7]}"

random.seed(seed_value)
random_values = [] 


for i in range(36):
	random_int = random.randint(1,2)
	random_values.append(random_int)

flag = "You won't get it here ^_^ "
flag_cipher = ""
for i in range(36):
	if (i & 1):
		flag_cipher += chr((ord(flag[i]) ^ random_values[i]) - 2)
	else:
		flag_cipher += chr((ord(flag[i]) ^ random_values[i]) + 1)
		