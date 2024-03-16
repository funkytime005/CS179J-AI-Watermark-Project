import os
from PIL import Image
from datetime import datetime

# import watermark from the apply function
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

def decode(filename):
    # compares two indexes
    def compare(x, y):
        return x == y
    
    # user built python function built to convert binary to decimal
    # use twos complement to return the decimal value
    # needs an integer sent to it, MAKE SURE TO CONVERT FIRST
    def binaryToDecimal(binary):
 
        decimal, i = 0, 0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return decimal

    img = Image.open(filename) # open passed filename
    _img = img.load()
    [width, height] = img.size
    # set the watermark found to false initially
    # if found, then break out of all loops and return
    watermark_found = False

    for x in range(width):
        for y in range(height):
            # each watermark is about 60 pixels from each other
            # make sure no out of bounds access occurs
            if (x + 60 < width) and (y + 60 < height):
                # check the lenght of the binary watermark using two loops
                # iterator doesnt matter, just make sure its only for that 2D array
                watermark_bits = [['' for _ in range(len(WATERMARK_BINARY))] for _ in range(len(WATERMARK_BINARY[0]))]
                for j in range(len(WATERMARK_BINARY)):
                    # set temporary variable to hold the position
                    xtemp = x + j
                    for i in range(len(WATERMARK_BINARY[0])):
                        # temporary variable
                        ytemp = y + i
                        # get the r,g,b of the selected pixel,
                        # if even, bit is even
                        # if odd, bit is odd
                        # add that to the watermark bits
                        [r, g, b] = _img[xtemp, ytemp]

                        if r % 2 == 0:
                            bit = '0'
                        else:
                            bit = '1'
                        
                        # print(i, j)
                        watermark_bits[i][j] += bit
                        # timestamp temp variable
                        y2 = ytemp
                    # timestamp temp variable
                    x2 = x

                # compare for every iteration
                # as soon as its true, return with the timestamp and IP
                if compare(watermark_bits, WATERMARK_BINARY):
                    #print("b")
                    watermark_found = True
                    timestamp_bits = ''
                    y2 = y2+1
                    i = 1
                    # simple while loop
                    # the UNIX time stamp is 31 bits long
                    # extract it from the image and then convert
                    while (i < 32):
                        [r,g,b] = (_img[x2,y2])
                        #r = r % 10
                        if r % 2 == 0:
                            bit = '0'
                        else:
                            bit = '1'
                        #print(x,y2, bit)
                        timestamp_bits += bit  # Extract last digit of red value as part of timestamp
                        x2+=1
                        i+=1
                    # for IP address
                    x3 = x
                    y3 = y2 + 1
                    i = 1
                    ip_bits = ''
                    # same logic here, except the IP address is 32 bits long in binary
                    while (i < 33):
                        [r,g,b] = (_img[x3,y3])
                        #r = r % 10
                        if r % 2 == 0:
                            bit2 = '0'
                        else:
                            bit2 = '1'
                        #print(x3,y3, bit2)
                        ip_bits += bit2  # Extract last digit of red value as part of IP
                        x3+=1
                        i+=1

                    # CONVERT TO INTEGER FIRST
                    # BEFORE SENDING IT TO THE BINARYTO DECIMAL
                    timestamp = int(timestamp_bits)
                    #print(timestamp)
                    val = binaryToDecimal(timestamp)
                    # UTC is internet time
                    # if want UTC, prepend that to fromtimestamp
                    # for now, we'll keep local time zone
                    timestamp_datetime = datetime.fromtimestamp(val)
                    
                    print(f"Watermark applied on: {timestamp_datetime.strftime('%m-%d-%Y %H:%M:%S')}")


                    #print(ip_bits)
                    # each val is 8 bits long, convert string to integer, then the binary to decimal
                    val1 = binaryToDecimal(int(ip_bits[:8]))
                    val2 = binaryToDecimal(int(ip_bits[8:16]))
                    val3 = binaryToDecimal(int(ip_bits[16:24]))
                    val4 = binaryToDecimal(int(ip_bits[24:32]))

                    # print the IP address
                    ip_address = f"{val1}.{val2}.{val3}.{val4}"
                    print("IP Address of the Watermark:", ip_address)
                    
                    break
                # for every iteration, if the comparison is false, reset watermark_bits
                else:
                    watermark_found = False
                    watermark_bits = []
            
            if watermark_found:
                break
        if watermark_found:
            break

    if not watermark_found:
        print("Watermark not found")
    else:
        print("Watermark found")

def main():
    fileExists = False
    while not fileExists:
        name = input('Enter name of file in current folder: ')
        for file in os.listdir():
            if file == name:
                fileExists = True
        if not fileExists:
            print(name + " not found.")

    decode(name)

if __name__ == "__main__":
    main()