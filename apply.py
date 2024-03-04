import os
from PIL import Image

WATERMARK_BINARY = [1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0] # 15-digit watermark creates 0.0031% FP rate, can be changed arbitrarily

def set_last_digit(r, i, complement): # if the current binary digit of the watermark is 0, red channel's value should be even. else, red channel's value should be odd
    if not complement:
        if WATERMARK_BINARY[i] == 0: # current digit is 0, make red channel even
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
        if WATERMARK_BINARY[i] == 1: # check opposite digit to exactly invert above branch
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

def apply_timestamp(complement): # TODO: stub
    pass

def apply_watermark(fileName): # applies watermark pattern to entire image
    img = Image.open(fileName) # open passed filename
    _img = img.load()
    [width, height] = img.size
    [x, y] = (int(width / 2), int(height / 2))
    xtemp = x

    for i in range(len(WATERMARK_BINARY)): # apply invisible watermark
        [r, g, b] = _img[xtemp, y]
        r = set_last_digit(r, i, False)
        
        img.putpixel((xtemp, y), (r, g, b)) # draw marked pixel
        xtemp += 1 # shift x position by 1

    # TODO: APPLY UNIX TIMESTAMP IN BINARY TO END OF WATERMARK HERE
    xtemp = x # reset temp position to center

    ytemp = y + 10
    for i in range(len(WATERMARK_BINARY)): # apply complement: if the watermark is inverted and reapplied, then the watermark cannot be destroyed if a bad actor adds 1 to every rgb value to "sanitize" the photo
        [r, g, b] = _img[xtemp, ytemp]
        r = set_last_digit(r, i, True)
    
        img.putpixel((xtemp, ytemp), (r, g, b)) # draw marked pixel
        xtemp += 1 # shift x position by 1

    # TODO: APPLY COMPLEMENT OF UNIX TIMESTAMP IN BINARY TO END OF WATERMARK HERE
    xtemp = x # reset temp positions to center
    ytemp = y

    img.show() # show image

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