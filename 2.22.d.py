import math
from itertools import permutations
from functools import reduce
from collections import defaultdict


ciphertext = \
	"BNVSNSIHQCEELSSKKYERIFJKXUMBGYKAMQLJTYAVFBKVT" \
	"DVBPVVRJYYLAOKYMPQSCGDLFSRLLPROYGESEBUUALRWXM" \
	"MASAZLGLEDFJBZAVVPXWICGJXASCBYEHOSNMULKCEAHTQ" \
	"OKMFLEBKFXLRRFDTZXCIWBJSICBGAWDVYDHAVFJXZIBKC" \
	"GJIWEAHTTOEWTUHKRQVVRGZBXYIREMMASCSPBNLHJMBLR" \
	"FFJELHWEYLWISTFVVYFJCMHYUYRUFSFMGESIGRLWALSWM" \
	"NUHSIMYYITCCQPZSICEHBCCMZFEGVJYOCDEMMPGHVAAUM" \
	"ELCMOEHVLTIPSUYILVGFLMVWDVYDBTFHRAYISYSGKVSUU" \
	"HYHGGCKTMBLRX"

def char2val(c) -> int:
	return ord(c) - ord('A')

def val2char(v) -> str:
	return chr(ord(v) + ord('A'))

def freqs_of(text) -> dict:
	freqs = defaultdict(int)
	for c in text:
		freqs[c] += 1
	return freqs

probs = {
	'E': 0.12,
	'T': 0.091,
	'A': 0.082,
	'O': 0.075,
	'I': 0.07,
	'N': 0.067,
	'S': 0.063,
	'H': 0.061,
	'R': 0.06,
	'D': 0.043,
	'L': 0.04,
	'C': 0.028,
	'U': 0.028,
	'M': 0.024,
	'W': 0.023,
	'F': 0.022,
	'G': 0.02,
	'Y': 0.02,
	'P': 0.019,
	'B': 0.015,
	'V': 0.01,
	'K': 0.008,
	'J': 0.002,
	'X': 0.001,
	'Q': 0.001,
	'Z': 0.001,
	}

def ic(text) -> int:
	freqs = freqs_of(text)
	length = len(text)
	ic = 0
	for freq in freqs.values():
		ic += freq ** 2
	return ic / (length ** 2)

def mg_of(text):
	freqs = freqs_of(text)
	length = len(text)
	mg = 0
	for c, prob in probs.items():
		mg += prob * freqs[c]
	return mg / length

def mg_diff(text):
	return abs(mg_of(text)-0.065)

freqs = freqs_of(ciphertext)
print(', '.join("{}: {}".format(c, freq) \
	for c, freq in sorted(
		freqs.items(),
		key=lambda x: x[1],
		reverse=True)))
# again letter distribution is weird

print(mg_of(ciphertext))
# also not a substitution / shift / affine cipher (only)

print("length: {}".format(len(ciphertext)))

triplets = defaultdict(int)
for idx in range(len(ciphertext)-2):
	triplets[ciphertext[idx:idx+3]] += 1
	
for triplet, count in triplets.items():
	if count > 1:
		print("{}:{}".format(triplet, count))
	
quads = defaultdict(int)
for idx in range(len(ciphertext)-3):
	quads[ciphertext[idx:idx+4]] += 1

for quad, count in quads.items():
	if count > 1:
		print("{}:{}".format(quad, count))
		
duplicates = ("MMAS", "EAHT", "WDVY", "DVYD", "MBLR", "WDVYD")

def indices(text):
	indices = []
	s_idx = 0
	while True:
		idx = ciphertext.find(text, s_idx)
		if idx == -1:
			break
		indices.append(idx)
		s_idx = idx + 1
	return indices

diffs = []
for duplicate in duplicates:
	first, second = indices(duplicate)
	print(second-first)
	diffs.append(second-first)
print(reduce(math.gcd, diffs))

# key is at most 174, number appears too much
# could be even m=3 assuming all 4-duplicates are meaningful
# m=9 has ~0.065 distribution, but does not fit most diffs
m = 6

def hill():
	for block in range(len(ciphertext)//3):
		s_idx = block * 3
		indices = list(range(s_idx, s_idx+3))
		print("a*x{} + b*x{} + c*x{} (mod 26) = {}".format(
			indices[0],
			indices[1],
			indices[2],
			char2val(ciphertext[indices[0]])))
		print("d*x{} + e*x{} + f*x{} (mod 26) = {}".format(
			indices[0],
			indices[1],
			indices[2],
			char2val(ciphertext[indices[1]])))
		print("g*x{} + h*x{} + i*x{} (mod 26) = {}".format(
			indices[0],
			indices[1],
			indices[2],
			char2val(ciphertext[indices[2]])))

partitions = [[] for i in range(m)]
for idx in range(len(ciphertext)):
	partitions[idx % m].append(ciphertext[idx])

for idx, part in enumerate(partitions):
	print("idx={}".format(idx))
	print("IC={}".format(ic(part)))
	print("Mg={}".format(mg_of(part)))
	freqs = freqs_of(part)
	print(', '.join("{}: {}".format(c, freq) \
		for c, freq in sorted(
			freqs.items(),
			key=lambda x: x[1],
			reverse=True)))
	# m=3 distribution was (~0.055)
	# m=9 distribution was (~0.065), with min 0.61 and max 0.83
	# each partition did not change distribution

def decrypt(text, key):
	return ''.join(chr(ord('A')+(ord(c)-ord(key))%26) for c in text)

letters = [chr(ord('A')+diff) for diff in range(26)]
part2letter = {}
decryptions = []

for idx, partition in enumerate(partitions):
	part2letter[idx] = ('A', 10)
	for c in letters:
		plaintext = decrypt(partitions[idx], c)
		curr_mg = mg_diff(plaintext)
		if curr_mg < part2letter[idx][1]:
			part2letter[idx] = (c, curr_mg)
			#print("[{}]={}".format(idx, part2letter[idx]))
			print("[{}]={}".format(idx, mg_of(plaintext)))
	decryptions.append(decrypt(partitions[idx], part2letter[idx][0]))
print(part2letter)
# shift did not make the distribution any closer to 0.065

mid_plaintext = []
for idx in range(len(ciphertext)):
	part_idx = idx % m
	inner_idx = idx // m
	mid_plaintext += decryptions[part_idx][inner_idx]
print(''.join(mid_plaintext))
# m=3,9: the diff is bigger than 0.01 and the mid_plaintext does not make sense
# this could be an affine cipher for each part???
# m=6 makes sense

import sys
sys.exit()

def affine_decrypt(letter, a, b):
	c_val = ord(letter) - ord('A')
	decrypt_val = (c_val * a + b) % 26
	return chr(decrypt_val + ord('A'))

for partition in partitions:
	freqs = freqs_of(partition)
	e_guess, *rest_guess = sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:6]
	guess2mg = {}
	for t_guess in rest_guess:
		print("d(e)={}; d(t)={}".format(e_guess[0], t_guess[0]))
		e_val = ord(e_guess[0]) - ord('A')
		t_val = ord(t_guess[0]) - ord('A')
		print("4a+b={}; 19a+b={}".format(e_val, t_val))
		diff_val = t_val - e_val
		if diff_val < 0:
			diff_val += 26
		print("15a={}".format(diff_val))
		a_guess = None
		for a in range(26):
			if (15 * a) % 26 == diff_val:
				a_guess = a
				break
		if a_guess is None:
			continue
		if math.gcd(26, a_guess) != 1:
			continue
		print("a={}".format(a_guess))
		a4 = (4 * a) % 26
		b_guess = e_val - a4
		if b_guess < 0:
			b_guess += 26
		print("b={}-{}={}".format(e_val, a4, b_guess))
		print("(a={}, b={})".format(a_guess, b_guess))
		decrypt_partition = ''.join(affine_decrypt(c, a_guess, b_guess) for c in partition)
		guess2mg[(a_guess, b_guess)] = mg_diff(decrypt_partition)
	print(guess2mg)
	
# m=3,9: the diffs are 0.02 or more, not affine

import sys
sys.exit()

# could be a sub for each partition?

diagrams = ['TH', 'HE', 'IN', 'ER', 'AN']
triagrams = ['THE', 'ING', 'AND']
# duplicates = ("MMAS", "EAHT", "WDVY", "DVYD", "MBLR", "WDVYD")

def gram_count(text):
	count = 0
	for idx in range(len(text)-1):
		if text[idx:idx+2] in diagrams \
			or text[idx:idx+3] in triagrams:
			count += 1
	return count

def sub():
	def sub_guess(g1, g2, g3, h1, h2, h3, i1, i2, i3):
		for dup1 in duplicates:
			for dup_s1_idx in range(len(dup1)):
				print(dup_s1_idx)
				part2sub = [{} for _ in range(m)]
				c_idx = ciphertext.find(dup1) + dup_s1_idx
				part_idx1 = c_idx % m
				part2sub[part_idx1][dup1[dup_s1_idx]] = g1
				part2sub[(part_idx1+1)%m][dup1[(dup_s1_idx+1)%len(dup1)]] = g2
				part2sub[(part_idx1+2)%m][dup1[(dup_s1_idx+2)%len(dup1)]] = g3
				
				for dup2 in list(set(duplicates)-set(dup1)):
					for dup_s2_idx in range(len(dup2)):
						c_idx = ciphertext.find(dup2) + dup_s2_idx
						part_idx2 = c_idx % m
						part2sub[part_idx2][dup2[dup_s2_idx]] = h1
						part2sub[(part_idx2+1)%m][dup2[(dup_s2_idx+1)%len(dup2)]] = h2
						part2sub[(part_idx2+2)%m][dup2[(dup_s2_idx+2)%len(dup2)]] = h3
				
						for dup3 in list(set(duplicates)-(set([dup1, dup2]))):
							for dup_s3_idx in range(len(dup3)):
								c_idx = ciphertext.find(dup3) + dup_s3_idx
								part_idx3 = c_idx % m
								part2sub[part_idx3][dup3[dup_s3_idx]] = i1
								part2sub[(part_idx3+1)%m][dup3[(dup_s3_idx+1)%len(dup3)]] = i2
								part2sub[(part_idx3+2)%m][dup3[(dup_s3_idx+2)%len(dup3)]] = i3
				
								plaintext = []
								for idx, c in enumerate(ciphertext):
									part_idx = idx % m
									if c in part2sub[part_idx]:
										plaintext.append(part2sub[part_idx][c])
									else:
										plaintext.append('-')
								plaintext = ''.join(plaintext)
								valid = True
								for black in ["ttt", "htt", "hht", "tth", "iii", "iing", "iin", "iig",
									"gtn", "ghn", "aaa", "niid", "ainaan", "ainaa"]:
									if black in plaintext:
										valid = False
										break
								if valid:
									print(plaintext)
									print(part2sub)
					
	sub_guess('t', 'h', 'e', 'i', 'n', 'g', 'a', 'n', 'd')
	# {'M': 'h'}, {'A': 'e'}, {'M': 't'}


# maybe permutation?

for length in [10, 50, 100]:
	for partition in partitions:
		print("{}:{}".format(length, mg_diff(partition[:length])))
		# distribution was convincing enough (~0.06) to state:
		# each partition did not change distribution
