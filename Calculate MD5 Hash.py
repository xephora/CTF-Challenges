import hashlib
 
b = input('Enter File and extension here:')

hasher = hashlib.md5()

with open(b, 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)

print(hasher.hexdigest())

