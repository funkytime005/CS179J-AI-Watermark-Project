import os
from PIL import Image

def set_value(channel): # sets individual color channel value within one pixel
    return round(channel / 10) * 10 # divides channel value by 10, rounds to nearest whole number, then appends 0. effectively rounds channel value to nearest 10

def apply_watermark(fileName): # applies watermark pattern to entire image
    img = Image.open(fileName) # open passed filename
    _img = img.load()
    [width, height] = img.size

    for x in range(width): # parse over image
        for y in range(height):
            if (x % 10 == 0) and (y % 10 == 0): # watermark pattern: edit every 10th pixel on x, y (figure out something with unlikely FP rate)
                [r, g, b] = _img[x, y] # get triplet of rgb values in current pixel
                
                r = set_value(r) # watermark pixel
                g = set_value(g)
                b = set_value(b)
                
                '''
                print('red channel: ' + str(r) + '\n' + # test print: ensure that each color channel has had its last digit removed
                      'green channel: ' + str(g) + '\n' + 
                      'blue channel: ' + str(b) + '\n')
                '''
                
                img.putpixel((x, y), (r, g, b)) # set pixel value to watermarked pixel value
                #img.putpixel((x, y), (0, 0, 0)) # TODO: current test method blackens pixel, set values to tweak rgb values specifically
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