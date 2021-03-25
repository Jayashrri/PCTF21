# The Epsilon Program

We begin by analysing the given image:

## Image Analysis

![Image](https://imgur.com/seaKmiM.png)

```bash
$ exiftool thesacredones.png
ExifTool Version Number         : 11.88
File Name                       : thesacredones.png
[-truncated-output-]
User Comment                    : Look out for the sacred ones and shed light upon those who are not. Then you should be able to Quite Read the message.
Flashpix Version                : 0100
Image Size                      : 480x480
Megapixels                      : 0.230
```

From the capitalisation of *Quite Read* and the square nature of the image we can infer that it has something to do with QR. Let us take a look at the image data:

```python
from PIL import Image
im = Image.open('thesacredones.png')
for pixel in iter(im.getdata()):
    print(pixel)
```

This gives us a long list of pixels. On observing closely we can notice that the RGB values of a pixel are either all prime or all composite. Now we can make sense of the clue: Sacred ones must be prime number valued pixel and *shedding light* could mean making the rest as white and keeping the prime ones as black so as to obtain a QR code. We can do this like so:

```python
from PIL import Image
import numpy, sympy

stegImage = Image.open('thesacredones.png')
pixels = numpy.array(stegImage)
qrimg = Image.new('RGB',(480,480))
qr = numpy.array(qrimg)

for i in range(len(pixels)):
    for j in range(len(pixels)):
        if sympy.isprime(pixels[i][j][0]):
            qr[i][j] = [0,0,0]
        else:
            qr[i][j] = [255,255,255]

qrimg = Image.fromarray(qr)
qrimg.save('decoded.png')
```

We find this in the QR:

```bash
$ zbarimg decoded.png
QR-Code:https://drive.google.com/file/d/1JKNEKehoZEjBQ6ki6s_DJTNZtV-6U633/view?usp=sharing
scanned 1 barcode symbols from 1 images in 0.01 seconds
```

The [link](https://drive.google.com/file/d/1JKNEKehoZEjBQ6ki6s_DJTNZtV-6U633/view?usp=sharing) takes us to an audio file (.wav). Let us analyse this:

## Audio File

```tex
$ exiftool therightones.wav
ExifTool Version Number         : 11.88
File Name                       : therightones.wav
[-truncated-output-]
Num Channels                    : 2
[-truncated-output-]
Comment                         : You have found out the sacred ones, now seek out the ones of their type who look the same either way you see them. They are Lucid, Simple and Beautiful. They are the Right ones.
Duration                        : 0:00:30
```

Again we can infer from the capitalisation that it has something to do with LSB. We have established that the sacred ones are prime numbers, so the first line should be talking about palindromes of such nature. One more thing we need to take note from the exif data is that this is a stereo audio, as indicated by the `Num Channels` value. Hence the mention of *right* in the question should pertain to audio from the right channel.

The [Wave file format](https://wavefilegem.com/how_wave_files_work.html) consists of data chunks with bytes known as frame bytes. In a stereo audio, the bytes in the odd positions (even index, if starting from 0) correspond to the left channel and the ones in the even positions correspond to the right channel. Two such frame bytes make up one frame.
Hence, our final script for extracting the LSBs of frames at prime palindrome positions from the right channel should be something like this:

```python
import wave
import sympy

stegFile = wave.open('therightones.wav','rb')
frameBytes = bytearray(list(stegFile.readframes(stegFile.getnframes())))
binaryMessage = ''
print(stegFile.getparams())

# 1460291 is the number of frames in this audio
primeList = list(sympy.primerange(2,1460291))
palPrimeList = []

for prime in primeList:
    if str(prime) == str(prime)[::-1]:
        palPrimeList.append(prime)

#Odd indices contain right channel audio, also not 2*i + 1 because 
# counting starts from 1  
for i in palPrimeList:
    binaryMessage += str(frameBytes[2*i-1] & 1)
   
blocks = (binaryMessage[i:i+8] for i in range(0,len(binaryMessage),8))
print(''.join(chr(int(block, 2)) for block in blocks))
```

Running this gives us the flag.
