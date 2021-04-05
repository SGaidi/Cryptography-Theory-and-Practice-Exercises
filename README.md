# Cryptography Theory and Practice Exercises

Decrypting classical encryption of text using mainly alphabetical distribution in the English language.

_Note these are one-time scripts, they are intended for maintenance, and so do not comply with PEP8 standarts. It's just for fun ;)_

## 2.21.a.py - Substitution Cipher

You are given a text in which each letter is substituted by another. And it's hinted that `F` decrypts to `w`.

- Frequencies of single letters, pairs and triplets are calculated.
- We start guessing, like `C` decrypts to `e`, `Z` decrypts to `h`, etc.
- When we fail (we get impossible text in the English language, we trace back to a valid starting point.

## 2.21.b.py - Vigenere Cipher

A cryptosystem that was unbreakable for a considerable period of time. Made use of a key word which encrypted and decrypted each letter in a block - separately.

- Frequencies of triplets and quads are calculated. Two from of the most common triplets are chosen: `HJV` and `KFT`.
- We count the difference between each appearance of these triplets, and we get their GCD (greatest common divisor). After some guesses, we conclude the block size is probably 6.
- We partition the text by `m=6`, and we can make use of single letter frequencies. We fine-tune our guesses to match the frequencies of the English language.

## 2.21.c.py - Affine Cipher

Assuming we know it's an affine cipher, it's fairly easy to decrypt using single letter frequency count.

## 2.21.d.py - Unspecified Cipher

- Tested single letter distribution, it was not a substitution, shift or affine cipher.
- Frequencies of triplets and quads calculated, found duplicates: `MMAS`, `EAHT`, `WDVY`, `DVYD`, `MBLR`, and `WDVYD`.
- Their corresponding indices diff GCD is calculated. Possible block sizes are: 3, 6 and 9.
- Tried decrypting using Hill cipher, it was disqualified.
- Only option left is Vigenere cipher.
