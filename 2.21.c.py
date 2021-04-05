from collections import defaultdict


ciphertext = \
	"KQEREJEBCPPCJCRKIEACUZBKRVPKRBCIBQCARBJCVFCUP" \
	"KRIOFKPACUZQEPBKRXPEIIEABDKPBCPFCDCCAFIEABDKB" \
	"BCPFEQPKAZBKRHAIBKAPCCIBURCCDKDCCJCIDFUIXPAFF" \
	"ERBICZDFKABICBBENEFCUPJCVKABPCYDCCDPKBCOCPERK" \
	"IVKSCPICBRKIJPKABI"

freqs = defaultdict(int)
for c in ciphertext:
	freqs[c] += 1
print(freqs)


def decrypt(c):
	res = (ord(c)-ord('A') - 4) * 11
	if res >= 0:
		return chr((res % 26) + ord('A')) 
	else:
		return chr(ord('A') + 26 -((-res) % 26))


print(''.join(decrypt(c) for c in ciphertext))
