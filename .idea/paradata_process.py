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
    def __init__(self, x, y):
        self.startx = x
        self.starty = y
        self.height = 0

def GetFileData(filename):
    f = open(filename, 'r')
    rawdatastart = 0
    #rectpointstart = 0
    #rect = Rectangle(0, 0)
    #rectlist = []
    linelist = []
    linedata = Linedata(0, 0)
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
        linedata.startx = x
        linedata.starty = y
        linedata.height = height
        linelist.append(linedata)
    return linelist

def MakeRectList(linelist,delt =3):
    rectlist=[]
    rect = Rectangle(0, 0)
    startline = linelist.pop()
    rect.leftuperx = startline.startx
    rect.leftupery = startline.starty
    rect.area = startline.height
    currentx =startline.startx
    currenty =startline.starty
    for line in linelist:
        if line.startx>currentx and line.startx - currentx <delt and abs(line.starty - currenty <delt):
            rect.area += line.height
            currentx = line.startx
            currenty = line.starty
        elif line.startx>currentx and abs(line.starty - currenty <delt):  # next rect
            rectlist.append(rect)
            rect.leftuperx = startline.startx
            rect.leftupery = startline.starty
            rect.area = startline.height
            currentx = line.startx
            currenty = line.starty
        elif line.startx  < currentx and line.starty > currenty



#config
cp = ConfigParser.SafeConfigParser()
cp.read('D:/photo/imageinfo.conf')

imgfile= cp.get('path', 'filename')
outfile =cp.get('path','datafile')



    if rectpointstart == 0 :
        rect.startx = x
        rect.starty = y
        rect.lastx = x
        rect.lasty =y
        rect.area = height
        rectpointstart =1
    elif rectpointstart==1:
        if abs(x - rect.lastx)<3 and abs(y-rect.lasty)<3 :
            rect.lastx =x
            rect.lasty =y
            rect.area += height
        else :
            rectpointstart =0
            rectlist.append(rect)

