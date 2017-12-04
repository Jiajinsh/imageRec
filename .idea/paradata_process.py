import re
from PIL import Image, ImageDraw
import ConfigParser
class Rectangle(object):
    def __init__(self,x,y):
        self.leftuperx=x
        self.leftupery=y
        self.rightuperx =0
        self.rightupery =0
        self.area =0

class Linedata(object):
    def __init__(self, x, y,height):
        self.startx = x
        self.starty = y
        self.height =height

def GetFileData(filename):
    f = open(filename, 'r')
    rawdatastart = 0
    #rectpointstart = 0
    #rect = Rectangle(0, 0)
    #rectlist = []
    linelist = []

    for line in f.readlines():
        if rawdatastart == 0 and re.match('.*height', line):
            rawdatastart = 1
            continue
        if rawdatastart == 0:
            continue
        list = re.split(r'\s+', line)
        x = int(list[0])
        y = int(list[1])
        height = int(list[2])
        linedata = Linedata(x, y,height)
        linelist.append(linedata)
    return linelist

def GetNextLine(list,curline,delt =20):
    for line in linelist:
        if line.startx > curline.startx and abs(line.starty - curline.starty)<delt:
            return line
        elif line.startx < curline.startx and line.starty > curline.starty + curline.height :
            return  line
    return None


def OrderLineList(linelist,delt =3):
    orderlinelist=[]
    lenth = len(linelist)
    currentline = linelist.pop(0)
    for i in range(1,lenth):
        line =GetNextLine(list,currentline)
        if line != None:
            currentline = line
            orderlinelist.append(line)
        else :
            print ('OrderLine list has None !')
            break
    return orderlinelist


def MakeRectList(linelist,delt =3):
    rectlist=[]
    rect = Rectangle(0, 0)
    startline = linelist.pop(0)
    rect.leftuperx = startline.startx
    rect.leftupery = startline.starty
    rect.area = startline.height
    currentx =startline.startx
    currenty =startline.starty
    for line in linelist:
        if line.startx>currentx and line.startx - currentx <delt and abs(line.starty - currenty) <20:
            rect.area += line.height
            rect.rightuperx =line.startx
            rect.rightupery=line.starty +line.height
            currentx = line.startx
            currenty = line.starty
        elif line.startx>currentx and abs(line.startx - currentx )>delt:  # next rect
            rectlist.append(rect)
            rect = Rectangle(line.startx, line.starty)
            rect.area = line.height
            rect.rightuperx =line.startx
            rect.rightupery=line.starty +line.height
            currentx = line.startx
            currenty = line.starty
        elif line.startx <currentx :  #next line
            rectlist.append(rect)
            rect = Rectangle(line.startx, line.starty)
            rect.area = line.height
            currentx = line.startx
            currenty = line.starty
    return rectlist

def DrawRect(rectlist,imgfile):
    im = Image.open(imgfile)
    draw = ImageDraw.Draw(im)
    for rect in rectlist:
        if rect is not None:
            draw.rectangle(((rect.leftuperx,rect.leftupery), (rect.rightuperx, rect.rightupery)), fill=255)

    im.save("D:/photo/debug/test1_rectshow.jpg")
#config
cp = ConfigParser.SafeConfigParser()
cp.read('D:/photo/imageinfo.conf')

imgfile= cp.get('path', 'filename')
outfile =cp.get('path','datafile')

linelist = GetFileData(outfile)

orderlist = OrderLineList(linelist)

rectlist = MakeRectList(orderlist)

DrawRect(rectlist,imgfile)

print ('finished!')