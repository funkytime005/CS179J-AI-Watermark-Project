import glob, os
from PIL import Image

def apply_watermark(fileName):
    img = Image.open(fileName)
    # img.load()
    [width, height] = img.size

    for x in range(width):
        for y in range(height):
            if (x % 10 == 0) and (y % 10 == 0): # watermark pattern (decide on this w group)
                img.putpixel((x, y), (0, 0, 0)) # TODO: current test method blackens pixel, set values to tweak rgb values specifically
    img.show()

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