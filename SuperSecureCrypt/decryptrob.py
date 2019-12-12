#!/usr/bin/env python
import sys

#store key and check to variables
check = open('check.txt','r')
check = check.read()
encChr = open('out.txt','r')
encChr = encChr.read()

#Setup encryption in sequence
chklen = len(check)
chkPos = 0
key = ""

for x in encChr:
	#First character of key
	chkChr = check[chkPos]
	
	#convert character of encChr to byte
	newChr = ord(x)
	
	#Adding newChr which is x to keyChr which is key then gets modulated by 255.
	newChr = chr((newChr + ord(chkChr)) % 255)
	
	#value for newChr will be stored into variable encrypted	
	key += newChr
	
	#current position in key will shift to the next character
	chkPos += 1
	
	#current position of key will be divided by key length
	chkPos = chkPos % chklen

print(key)
