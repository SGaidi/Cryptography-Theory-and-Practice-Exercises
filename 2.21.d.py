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
# m=6 makes sense
