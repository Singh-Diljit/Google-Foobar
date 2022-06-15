import base64

encrypted = 'H1QUGg8HHEBDQ1NdT0sDC1ZREFRLT0sHFl9cARIAGglDWQkQQxYUGwkBFFZUQ19HSAkCH1xCEABA T1ZEXlpeBwECCwUGFVYXSFNADg8MEFZGAR4CARhDWQkQQwYJAwMHElZUQ19HSB4FG1FZEABAT1ZE XkBRAhZAQ0xDH1xfQ1NdT0sTEF0RQw4= ' 

my_eyes = str.encode('######') #I've redacted my private email
decoded = base64.b64decode(encrypted)

decrypted = ''

for i in range(0, len(decoded)):
    decrypted += chr((my_eyes[i%len(my_eyes)] ^ decoded[i]))


print(decrypted)

Ans: {'success' : 'great', 'colleague' : 'esteemed',
      'efforts' : 'incredible', 'achievement' : 'unlocked',
      'rabbits' : 'safe', 'foo' : 'win!'}

#<encrypted>
#H1QUGg8HHEBDQ1NdT0sDC1ZREFRLT0sHFl9cARIAGglDWQkQQxYUGwkBFFZUQ19HSAkCH1xCEABA

#T1ZEXlpeBwECCwUGFVYXSFNADg8MEFZGAR4CARhDWQkQQwYJAwMHElZUQ19HSB4FG1FZEABAT1ZE

#XkBRAhZAQ0xDH1xfQ1NdT0sTEF0RQw4= </encrypted>
