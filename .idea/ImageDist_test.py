#load line data ,draw  yellow  line.
import re
from PIL import Image, ImageDraw
import ConfigParser
#config
cp = ConfigParser.SafeConfigParser()
cp.read('D:/photo/imageinfo.conf')

imgfile= cp.get('path', 'filename')
outfile =cp.get('path','datafile')

im =  Image.open(imgfile)
draw = ImageDraw.Draw(im)

f = open(outfile, 'r')
rawdatastart =0
for line in f.readlines():
    if rawdatastart ==0 and re.match('.*height', line):
        rawdatastart =1
        continue
    if rawdatastart ==0:
        continue
    list = re.split(r'\s+', line)
    x =int(list[0])
    y=int(list[1])
    height=int(list[2])
    draw.line(((x, y), (x, y+height)), fill=255)

im.save("D:/photo/debug/test1_show.jpg")

