# -*- coding: utf-8 -*-
from PIL import Image
import ConfigParser
import os

class Rectangle(object):
    def __init__(self,x,y,w,h):
        self.x=x
        self.y=y
        self.w =w
        self.h =h

class Line(object):
    def __init__(self,x,y,h):
        self.x=x
        self.y=y
        self.h =h

def binarizing(img,threshold=140):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


#romove no use data radius >=2
def img_filter_precess(img,radius=15):
    w,h =img.size
    pixdata = img.load()
    for x in range(0,w):
        for y in range(0,h):
            #left adge
            if x<radius and pixdata[x,y] == 255 :
                for i in range(2,radius):
                    if pixdata[x+i,y] ==0 and pixdata[x+i-1,y]==0 :
                        pixdata[x, y] =0
                        break
                    # vetical isolated
                    if y>=radius and y <=h-radius and pixdata[x, y - i] == 0 and pixdata[x, y - i + 1] == 0 and pixdata[x, y + i] == 0 and pixdata[
                        x, y + i - 1] == 0:
                        pixdata[x, y] = 0
                        break

            # right adge
            if x >w- radius and pixdata[x, y] == 255:
                for i in range(2, radius):
                    if pixdata[x - i, y] ==0 and pixdata[x - i + 1, y] ==0:
                        pixdata[x, y] = 0
                        break
            #uper adge
            if y<radius and pixdata[x,y]== 255 :
                for i in range(2,radius):
                    if pixdata[x,y+i] ==0 and pixdata[x,y+i-1]==0 :
                        pixdata[x, y] =0
                        break
                    #horizental isolated
                    if x> radius and x <w-radius and pixdata[x-i, y ] ==0 and pixdata[x-i+1, y ] ==0 and pixdata[x+i, y] ==0 and pixdata[x+i-1, y ] ==0 :
                        pixdata[x, y] = 0
                        break
            #down adge
            if y>h-radius and pixdata[x,y]== 255 :
                for i in range(2,radius):
                    if pixdata[x,y -i] ==0 and pixdata[x,y-i+1]==0 :
                        pixdata[x, y] =0
                        break
                    #horizental isolated
                    if x> radius and x <w-radius and pixdata[x-i, y ] ==0 and pixdata[x-i+1, y ] ==0  and pixdata[x+i, y] ==0 and pixdata[x+i-1, y ] ==0 :
                        pixdata[x, y] = 0
                        break
            #center
            if y>=radius and y <= h-radius and x>=radius and x <=w-radius and pixdata[x,y]== 255:
                for i in range(2,radius):
                    #vetical isolated
                    if pixdata[x,y-i]==0 and pixdata[x,y-i+1]==0 and pixdata[x,y+i] ==0 and pixdata[x,y+i-1]==0 :
                        pixdata[x, y] =0
                        break
                    #horizental isolated
                    if pixdata[x-i, y ] ==0 and pixdata[x-i+1, y ] ==0  and pixdata[x+i, y] ==0and pixdata[x+i-1, y ] ==0 :
                        pixdata[x, y] = 0
                        break
    return img

#yellow color process
def yellowFilter(img,rgthr=200,bthr=10):   #input: org image
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            rval,gval,bval =im.getpixel((x,y))
            if rval > rgthr and gval > rgthr :
                im.putpixel((x,y),(255,255,0))
    return img

#save tezheng data depth =20
def savecharacteristicvalue(img,outputfile,heightthreshold =20):
    w,h =img.size
    pixdata = img.load()
    f = open(outputfile, 'w')
    filehead = "image info :format= %s size=%s mode=%s \n" % (im.format,im.size,im.mode)
    f.write(filehead)
    f.write("image data:\nx     y       height\n" )
    for x in range(1,w-1):
        height =0
        linestart =0
        for y in range(1,h-1):
            if linestart ==0 and pixdata[x,y] ==255 and pixdata[x,y+1] ==255:
                linestart =1
                ystart = y
                height =1
            elif linestart ==1 and pixdata[x,y] ==0 and pixdata[x,y+1] ==0 :
                if height >heightthreshold:
                    content = "%d       %d      %d\n" % (x, ystart, height)
                    f.write(content)
                height =0
                linestart =0
                continue
            elif pixdata[x,y] == 255:
                height += 1

        if height >heightthreshold:
            content = "%d       %d      %d\n" % (x,ystart,height)
            f.write(content)
    f.close()


#config
cp = ConfigParser.SafeConfigParser()
cp.read('D:/photo/imageinfo.conf')

orgimgfile= cp.get('path', 'filename')
workimgfile= cp.get('path', 'workfilename')
orgoutfile =cp.get('path','datafile')
debugpath = cp.get('path','debugpath')

#parameter
graythreshold = cp.getint('para','greythreshold')
filterdepth = cp.getint('para','imgfilterdepth')
filterdepth2 = cp.getint('para','imgfilterdepth2')
imgheight = cp.getint('para','imgheight')

if not os.path.isdir(debugpath):
    os.makedirs(debugpath)


cmd = raw_input('plesease select init or test \ninit: for build orignal parameter\ntest:for test the image \n')
if cmd == 'init':
    imgfile = orgimgfile
    outfile = orgoutfile
else:
    imgfile = workimgfile
    outfile = debugpath +"output_01.txt"
#image file
im =  Image.open(imgfile)
#yelow = yellowFilter(im)
#yelow.save("D:/photo/debug/test1_yellow.jpg")

#gray convert
gray = im.convert("L")
gray.save(debugpath+"test1_gray.jpg")

#bin precess
bin = binarizing(gray,graythreshold)


bin.save(debugpath+"test1_bin.jpg")
bin = img_filter_precess(bin,filterdepth)
bin.save(debugpath+"test1_bin_filter.jpg")

bin = img_filter_precess(bin,filterdepth2)
bin = img_filter_precess(bin,filterdepth2)
bin.save(debugpath+"test1_bin_filter8.jpg")
#save the  regtangle data
savecharacteristicvalue(bin,outfile,imgheight)

print("OK! image is:",im.format, im.size, im.mode)