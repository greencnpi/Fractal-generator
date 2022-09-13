from PIL import Image
from random import randint
import math
import os

#pure generation
size = 1000
maxcount = 1000000
minlength = 1
maxlength = 40
minmix = 1
maxmix = 4
minseed = 1
maxseed = 15
minrotate = 1
maxrotate = 5

print("Just press enter to generate a fractal. Type save to save it\n")

cd = os.getcwd()

#main loop
while True:
    prompt = input(">")
    if prompt == "save":
        number = 1
        if os.path.exists(os.path.join(cd, "fractals")) == False:
            os.mkdir(os.path.join(cd, "fractals"))
        for path in os.listdir(os.path.join(cd, "fractals")):
            if os.path.isfile(os.path.join(cd, "fractals", path)):
                number += 1
        os.rename(os.path.join(cd, "fractal.png"), os.path.join(cd, "fractals", str(number) + ".png"))
        print("done\n")
    else:
        print("start...")

        #make image
        img = Image.new("RGB", (size, size))

        #randomize variables
        x, y = size/2, size/2
        mix = [randint(minlength,maxlength) for i in range(randint(minmix,maxmix))]
        seed = [randint(0,359) for i in range(randint(minseed, maxseed))]
        tempseed = []
        rotatelist = [randint(0,359) for i in range(randint(minrotate, maxrotate))]
        
        #helps me manage loop and some random stuff
        loop = True
        count = 0
        linecount = 0

        while loop:
            for rotate in rotatelist:
                for i in seed:
                    for j in range(1, mix[linecount % len(mix)] + 1):
                        x += math.cos(math.radians(i))
                        y += math.sin(math.radians(i))
                        if abs(size/2 - x) > (size/2 - 10) or abs(size/2 - y) > (size/2 - 10) or count > maxcount:
                            loop = False
                            break
                        img.putpixel((round(x),round(y)), (255,255,255))
                        count += 1
                    linecount += 1
                if loop == False:
                    break
                seed.extend([i+rotate%360 if i+rotate >= 360 else i+rotate for i in seed])

        #save image
        img.save('fractal.png')
        print("done\n")
