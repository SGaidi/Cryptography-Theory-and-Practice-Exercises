import math
from functools import reduce
from collections import defaultdict

ciphertext = \
	"KCCPKBGUFDPHQTYAVINRRTMVGRKDNBVFDETDGILTXRGUD" \
	"DKOTFMBPVGEGLTGCKQRACQCWDNAWCRXIZAKFTLEQRPTYC" \
	"QKYVXCHKFTPONCQQRHJVAJUWETMCMSPKQDYHJVDAHCTRL" \
	"SVSKCGCZQQDZXGSFRLSWCWSJTBHAFSIASPRJAHKJRJUMV" \
	"GKMITZHFPDISPZLVLGWTFPLKKEBDPGCEBSHCTJRWXBAFS" \
	"PEZQNRWXCVYCGAONWDDKACKAWBBIKFTIOVKCGGHJVLNHI" \
	"FFSQESVYCLACNVRWBBIREPBBVFEXOSCDYGZWPFDTKFQIY" \
	"CWHJVLNHIQIBTKHJVNPIST"

print(len(ciphertext))

triplets = defaultdict(int)
quads = defaultdict(int)

for idx in range(0,  len(ciphertext)-2):
	triplets[ciphertext[idx]+ciphertext[idx+1]+ciphertext[idx+2]] += 1
for idx in range(0,  len(ciphertext)-3):
	quads[ciphertext[idx]+ciphertext[idx+1]+ciphertext[idx+2]+ciphertext[idx+3]] += 1

def max_10(d):
	return sorted([(key, value) for key, value in d.items()], key=lambda x: x[1])[:-10:-1]

print(max_10(triplets))
print(max_10(quads))

def diffs(main_text, search_text) -> list:
	indices = []
	s_idx = 0
	while True:
		idx = main_text.find(search_text, s_idx)
		if idx == -1:
			break
		indices.append(idx)
		s_idx = idx + 1
	diffs = []
	for idx in range(len(indices)-1):
		diffs.append(indices[idx+1]-indices[idx])
	return diffs

print(reduce(math.gcd, diffs(ciphertext, 'HJV')))
print(reduce(math.gcd, diffs(ciphertext, 'KFT')))

m = 6
partitions = [[] for part in range(m)]

for idx in range(len(ciphertext)):
	partitions[idx%m].append(ciphertext[idx])
print('\n'.join(''.join(part) for part in partitions))

def ic(text) -> int:
	freqs = defaultdict(int)
	for c in text:
		freqs[c] += 1
	length = len(text)
	ic = 0
	for freq in freqs.values():
		ic += freq ** 2
	return ic / (length ** 2)

for part in partitions:
	print(ic(part))

def decrypt(text, key):
	return ''.join(chr(ord('A')+(ord(c)-ord(key))%26) for c in text)

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

def mg(text):
	freqs = defaultdict(int)
	for c in text:
		freqs[c] += 1
	mg = 0
	for c, prob in probs.items():
		mg += prob * freqs[c]
	mg /= len(text)
	return abs(mg-0.065)
	
letters = [chr(ord('A')+diff) for diff in range(26)]
part2letter = {}
decryptions = []

for idx, partition in enumerate(partitions):
	part2letter[idx] = ('A', 10000)
	for c in letters:
		plaintext = decrypt(partitions[idx], c)
		curr_mg = mg(plaintext)
		if curr_mg < part2letter[idx][1]:
			part2letter[idx] = (c, curr_mg)
	decryptions.append(decrypt(partitions[idx], part2letter[idx][0]))
print(part2letter)

plaintext = []
for idx in range(len(ciphertext)):
	part_idx = idx % m
	inner_idx = idx // m
	plaintext += decryptions[part_idx][inner_idx]
print(''.join(plaintext))
