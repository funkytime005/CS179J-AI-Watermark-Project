import os
from PIL import Image
import time
import requests

WATERMARK_BINARY = [['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'],
                    ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0']]

# returns an int 0-255, corresponding to either the passed in color channel or a 1-digit offset
# if the current binary digit of the watermark is 0, red channel's value should be even. else, red channel's value should be odd
def set_last_digit(r, i, str, complement): 
    test = True # SET THIS TO FALSE WHEN YOU'RE ACTUALLY USING IT, IT MAKES IT REALLY EASY TO SEE WHEN IT'S TRUE FOR DEBUGGING
    if not complement:
        if str[i] == '0': # current digit is 0, make red channel even
            if test:
                return 0 # temp test statement to make changes visibly obvious (when the whole point is to be invisible, it's difficult to ensure correctness visually)
        
            if r % 2 == 0: # red channel is already even -> do not alter
                return r
            else: # red channel is odd -> make even (note: if red channel is 255, adding 1 does not generate a valid rgb value so set to 254 instead)
                return min(r + 1, 254)
        else: # current digit is 1, make red channel odd
            if test:
                return 255 # temp test statement to make changes visibly obvious (when the whole point is to be invisible, it's difficult to ensure correctness visually)
        
            if r % 2 == 0: # red channel is even -> make odd (note: highest even red is 254, so adding 1 will not overflow)
                return r + 1
            else: # red channel is already odd -> do not alter
                return r
    else: # COMPLEMENT CASE: same procedure, but exactly the opposite. this applies the complement of the binary watermark, protecting it against tampering by inversion
        if str[i] == '1': # check opposite digit to exactly invert above branch
            if test:
                return 0 # temp test statement to make changes visibly obvious (when the whole point is to be invisible, it's difficult to ensure correctness visually)
        
            if r % 2 == 0: 
                return r
            else: 
                return min(r + 1, 254)
        else:
            if test: 
                return 255 # temp test statement to make changes visibly obvious (when the whole point is to be invisible, it's difficult to ensure correctness visually)
        
            if r % 2 == 0: 
                return r + 1
            else: 
                return r

# returns the current unix timestamp (time since 1/1/1970) in seconds, converted to binary, as a string
def get_time():
    return str(bin(int(time.time()))[2:]) # get unix timestamp to second, format as binary string

# returns a quadruple of 8-bit binary strings, each corresponding to one of each group separated by dots in user public ip address
def get_ip():
    ip = requests.get('https://api.ipify.org').text # get public ip address
    
    ip_str = ip.split('.') # separate out each dotted group
    
    for i in range(len(ip_str)): # convert each index to 8-bit binary
        ip_str[i] = format(int(ip_str[i]), '08b')

    return ''.join(ip_str) # return ip string list concatenated to single string

# applies watermark pattern, timestamp, and public IP address over entire image in binary + complement
def apply_watermark(fileName): 
    t = get_time() # get current time
    ip = get_ip() # get user's public ip address

    img = Image.open(fileName) # open passed filename
    img = img.convert('RGB')
    _img = img.load()
    [width, height] = img.size

    for x in range(width):
        for y in range(height):
            if (x % 60 == 0) and (y % 60 == 0) and (x + 60 < width) and (y + 60 < height):
                # print(x, y)

                for i in range(len(WATERMARK_BINARY)): # apply invisible watermark
                    xtemp = x + i
                    for j in range(len(WATERMARK_BINARY[0])):
                        ytemp = y + j
                        # print(xtemp, ytemp)
                        [r, g, b] = _img[xtemp, ytemp] # get rgb of current pixel
                        r = set_last_digit(r, i, WATERMARK_BINARY[j], False) # accordingly set red channel (watermark)
                        img.putpixel((xtemp, ytemp), (r, g, b)) # draw marked pixel
                
                ytemp += 1
                for i in range(len(t)): # apply timestamp (same method as above)
                    xtemp = x + i
                    [r, g, b] = _img[xtemp, ytemp]
                    r = set_last_digit(r, i, t, False)
                    img.putpixel((xtemp, ytemp), (r, g, b))
                
                ytemp += 1    
                for i in range(len(ip)): # apply ip address
                    xtemp = x + i
                    [r, g, b] = _img[xtemp, ytemp]
                    r = set_last_digit(r, i, ip, False)
                    img.putpixel((xtemp, ytemp), (r, g, b))

                # APPLY COMPLEMENTS    
        
                for i in range(len(WATERMARK_BINARY)): # apply invisible watermark
                    xtemp = x + 30 + i
                    for j in range(len(WATERMARK_BINARY[0])):
                        ytemp = y + 30 + j
                        [r, g, b] = _img[xtemp, ytemp] # get rgb of current pixel
                        r = set_last_digit(r, i, WATERMARK_BINARY[j], True) # accordingly set red channel (watermark)
                        img.putpixel((xtemp, ytemp), (r, g, b)) # draw marked pixel

                ytemp += 1
                for i in range(len(t)): # apply timestamp (same method as above)
                    xtemp = x + 30 + i
                    [r, g, b] = _img[xtemp, ytemp]
                    r = set_last_digit(r, i, t, True)
                    img.putpixel((xtemp, ytemp), (r, g, b))
                
                ytemp += 1    
                for i in range(len(ip)): # apply ip address
                    xtemp = x + 30 + i
                    [r, g, b] = _img[xtemp, ytemp]
                    r = set_last_digit(r, i, ip, True)
                    img.putpixel((xtemp, ytemp), (r, g, b))
    
    img = img.save(fileName.removesuffix('.png') + '_watermarked.png', quality = 'keep', subsampling = 0) # save watermarked image to same file path

# driver code, takes in and verifies file, then sends it to apply_watermark()
def main():
    fileExists = False
    while not fileExists: # continuously ask for file name until valid file entered
        name = input('Enter name of file in current folder: ') # get filename
        for file in os.listdir(): # read through current directory
            if file == name:
                fileExists = True # found file, stop looping 
        if not fileExists:
            print(name + " not found.") # error then try again

    apply_watermark(name)

if __name__ == "__main__":
    main()
