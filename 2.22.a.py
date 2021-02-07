from collections import defaultdict


ciphertext = \
	"EMGLOSUDCGDNCUSWYSFHNSFCYKDPUMLWGYICOXYSIPJCK" \
	"QPKUGKMGOLICGINCGACKSNISACYKZSCKXECJCKSHYSXCG" \
	"OIDPKZCNKSHICGIWYGKKGKGOLDSILKGOIUSIGLEDSPWZU" \
	"GFZCCNDGYYSFUSZCNXEOJCNGYEOWEUPXEZGACGNFGLKNS" \
	"ACIGOIYCKXCJUCIUZCFZCCNDGYYSFEUEKUZCSOCFZCCNC" \
	"IACZEJNCSHFZEJZEGMXCYHCJUMGKUCY"


singles_freq = defaultdict(int)
pairs_freq = defaultdict(int)
triples_freq = defaultdict(int)


for c in ciphertext:
	singles_freq[c] += 1
for idx in range(len(ciphertext)-1):
	pairs_freq[ciphertext[idx]+ciphertext[idx+1]] += 1
for idx in range(len(ciphertext)-2):
	triples_freq[ciphertext[idx]+ciphertext[idx+1]+ciphertext[idx+2]] += 1


def max_ten(d: dict) -> dict:
	return [(key, value) for key, value in sorted(d.items(), key=lambda item: item[1])]


print(max_ten(singles_freq)[:][::-1])
print()
print(max_ten(pairs_freq)[-50:][::-1])
print()
print(max_ten(triples_freq)[-26:][::-1])
print()
print(pairs_freq['NC'])
print(pairs_freq['CN'])
print(pairs_freq['CZ'])
print(pairs_freq['CA'])
print(pairs_freq['CN'])
print(pairs_freq['KC'])
print(pairs_freq['YC'])
for key, val in pairs_freq.items():
	if key[0] == 'Z':
		print("{}:{}".format(key, val))

guess_key = {
	# highly confident
	'F': 'w',  # given
	'C': 'e',  # most common by far
	'Z': 'h',  # ZC has biggest freq, by far from other (-e) pairs,
	           #  and opposite CZ freq is low as expected by he/eh (7, 1)
			   #  additional option is 'A': 'h' (6, 0), but ZCC (aee) and FZC (wae) does not make sense
	'N': 'l',  # FZCCNC (whee-e): wheel is most common word, other options are r,s,t
	'Y': 'r',  # multiple YY appear, options are: ss, tt, oo, pp, rr
	'G': 'a',  # CGNFG (e-lw-) must have a vowel for G (out of es, ed, et, en, ea options)
	# G,FZCCN,DGYYSF (a,wheel,barrow)
	# a,wheel,barrow
	'S': 'o', # CY,KZSCK,XEC (ep,sh-es,-ie)
	'D': 'b',
	'E': 'i',  # FZE (wh-) is usually completed with: a,i,o
	           #  also, he is next common diagram, and ZE is next common freq
	'K': 's',  # multiple KK appear, options are: ss, tt, pp
	'W': 'g',  # WYGKKGKGO (-rass,asa-) grass
	'M': 'm', 'U': 't',  # MGKUCY (-as-er) master
	'I': 'd', 'O': 'n',  # WGYICO (gar-e-)
	'A': 'v',  # NCGACK (lea-es)
	'J': 'c',  # ACZEJNC (vehi-le)
	'L': 'y',  # E,MGL,OSU (i,may,not)
	'P': 'u',  # DPU (but)
	'X': 'p',  # produces
	'Q': 'j',  # just
	'H': 'f',  # of
	#qhkzx
	}


print(guess_key)
plaintext = ''.join(guess_key[c] if c in guess_key else '-' for c in ciphertext)
diff = 45
print('\n'.join(plaintext[idx:idx+diff] for idx in range(0, len(plaintext), diff)))