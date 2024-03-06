import os
from PIL import Image
import time

WATERMARK_BINARY = ['1', '0', '0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0'] # 15-digit watermark creates 0.0031% FP rate, can be changed arbitrarily

# returns an int 0-255, corresponding to either the passed in color channel or a 1-digit offset
def set_last_digit(r, i, str, complement): # if the current binary digit of the watermark is 0, red channel's value should be even. else, red channel's value should be odd
    if not complement:
        if str[i] == '0': # current digit is 0, make red channel even
            # return 0 # temp test statement to make changes visibly obvious (when the whole point is to be invisible, it's difficult to ensure correctness visually)
        
            if r % 2 == 0: # red channel is already even -> do not alter
                return r
            else: # red channel is odd -> make even (note: if red channel is 255, adding 1 does not generate a valid rgb value so set to 254 instead)
                return min(r + 1, 254)
        else: # current digit is 1, make red channel odd
            # return 255 # temp test statement to make changes visibly obvious (when the whole point is to be invisible, it's difficult to ensure correctness visually)
        
            if r % 2 == 0: # red channel is even -> make odd (note: highest even red is 254, so adding 1 will not overflow)
                return r + 1
            else: # red channel is already odd -> do not alter
                return r
    else: # COMPLEMENT CASE: same procedure, but exactly the opposite. this applies the complement of the binary watermark, protecting it against tampering by inversion
        if str[i] == '1': # check opposite digit to exactly invert above branch
            # return 0 # temp test statement to make changes visibly obvious (when the whole point is to be invisible, it's difficult to ensure correctness visually)
        
            if r % 2 == 0: 
                return r
            else: 
                return min(r + 1, 254)
        else: 
            # return 255 # temp test statement to make changes visibly obvious (when the whole point is to be invisible, it's difficult to ensure correctness visually)
        
            if r % 2 == 0: 
                return r + 1
            else: 
                return r

# applies the current unix timestamp in binary at the end of watermark (or its complement)
def get_time(): # TODO: stub
    return str(bin(int(time.time()))[2:]) # get unix timestamp to second, format as binary string

def apply_watermark(fileName): # applies watermark pattern to entire image
    t = get_time()
    img = Image.open(fileName) # open passed filename
    _img = img.load()
    [width, height] = img.size

    for x in range(width):
        for y in range(height):
            if (x % 50 == 0) and (y % 10 == 0) and (x + 50 < width) and (y + 10 < height): # watermark is 15 characters long + ~30 character long timestamp, so space 50 pixels apart for redundancy
                xtemp = x
                for i in range(len(WATERMARK_BINARY)): # apply invisible watermark
                    [r, g, b] = _img[x, y] # get rgb of current pixel
                    r = set_last_digit(r, i, WATERMARK_BINARY, False) # accordingly set red channel (watermark)
                    img.putpixel((x, y), (r, g, b)) # draw marked pixel
                    x += 1 # shift x position by 1

                for i in range(len(t)): # apply timestamp
                    [r, g, b] = _img[x, y]
                    r = set_last_digit(r, i, t, False)
                    img.putpixel((x, y), (r, g, b))
                    x += 1
                x = xtemp

                ytemp = y
                y += 5
                for i in range(len(WATERMARK_BINARY)): # apply complement: if the watermark is inverted and reapplied, then the watermark cannot be destroyed if a bad actor adds 1 to every rgb value to "sanitize" the photo
                    [r, g, b] = _img[x, y]
                    r = set_last_digit(r, i, WATERMARK_BINARY, True)
                    img.putpixel((x, y), (r, g, b)) 
                    x += 1
                
                for i in range(len(t)): # apply complement of timestamp
                    [r, g, b] = _img[x, y]
                    r = set_last_digit(r, i, t, True)
                    img.putpixel((x, y), (r, g, b))
                    x += 1
                
                x = xtemp
                y = ytemp
    
    # print(t)
    # img.show() # show image
    img = img.save(fileName.removesuffix('.jpg') + '_watermarked.jpg') # save watermarked image to same file path

def main():
    fileExists = False
    while not fileExists:
        name = input('Enter name of file in current folder: ')
        for file in os.listdir():
            if file == name:
                fileExists = True
        if not fileExists:
            print(name + " not found.")

    apply_watermark(name)

if __name__ == "__main__":
    main()