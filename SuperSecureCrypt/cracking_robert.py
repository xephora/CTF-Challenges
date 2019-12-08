#!/usr/bin/env python
import os

print('Cracking Roberts Hashed Password')
print('============================================')

letters = raw_input('Insert letter/letters: ')

os.system("python3 /tmp/xfer/SuperSecureCrypt.py -k " + letters + " -i check.txt -o test.txt")


print ('===========================================')
print ('Compare test.txt with out.txt to see if any letters matched')
print (" ")
print (" ")
print ('out.txt Output')
print (" ")
print (" ")
os.system("cat out.txt")
print ("===========================================")
print (" ")
print (" ")
print ('test.txt Output')
print (" ")
print (" ")
os.system("cat test.txt")
