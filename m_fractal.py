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

#mutation generation and subgeneration
mutate = True
minmutate = 0
maxmutate = 8
mutatedim = 0.7
maxstrength = 0.5
maxseedstrength = 0.5

ignoremutate = False
lengthmutate = True
rotatemutate = True
seedmutate = True
cutmutate = True

if ignoremutate == False:
    lengthmutate = mutate
    rotatemutate = mutate
    seedmutate = mutate
    cutmutate = mutate

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
        mutaterate = randint(minmutate, maxmutate)
        seedstrength = randint(0,round(maxseedstrength*100))/100
        
        #helps me manage loop and some random stuff
        loop = True
        count = 0
        linecount = 0
        mutatecount = 0

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
                    
                    if lengthmutate:
                        if randint(0, 10000) < mutaterate:
                            mutatecount += 1
                            mutaterate *= mutatedim
                            randomindex = randint(0, len(mix) - 1)
                            mix[randomindex] += randint(-round(maxstrength * (maxlength - minlength)), round(maxstrength * (maxlength - minlength)))
                            if mix[randomindex] < minlength:
                                mix[randomindex] = minlength
                            elif mix[randomindex] > maxlength:
                                mix[randomindex] = maxlength

                    if rotatemutate:
                        if randint(0, 10000) < mutaterate:
                            mutatecount += 1
                            mutaterate *= mutatedim
                            randomindex = randint(0, len(rotatelist) - 1)
                            rotatelist[randomindex] += randint(-round(maxstrength * 180), round(maxstrength * 180))
                            if rotatelist[randomindex] < 0:
                                rotatelist[randomindex] += 360
                            elif rotatelist[randomindex] > 360:
                                rotatelist[randomindex] -= 360

                    if seedmutate:
                        if randint(0, 10000) < mutaterate:
                            mutatecount += 1
                            mutaterate *= mutatedim
                            rate = seedstrength * 10000
                            for item in seed:
                                if randint(0, 10000) < rate:
                                    randomindex = randint(0, len(rotatelist) - 1)
                                    item += randint(-round(maxstrength * 180), round(maxstrength * 180))
                                    if rotatelist[randomindex] < 0:
                                        rotatelist[randomindex] += 360
                                    elif rotatelist[randomindex] > 360:
                                        rotatelist[randomindex] -= 360

                    if cutmutate:
                        if randint(0, 10000) < mutaterate:
                            mutatecount += 1
                            mutaterate *= mutatedim
                            rate = (randint(0,round(maxstrength*100))/100) * (randint(0,round(seedstrength*100))/100) * 10000
                            for item in seed:
                                if randint(0, 10000) < rate:
                                    del item
                if loop == False:
                    break
                seed.extend([i+rotate%360 if i+rotate >= 360 else i+rotate for i in seed])

        #save image
        img.save('fractal.png')
        print("done")
        print("Mutations: " + str(mutatecount) + "\n")
