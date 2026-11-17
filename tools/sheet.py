import sys,glob,os
from PIL import Image,ImageDraw
pat,out,cols,sc=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4])
fs=sorted(glob.glob(pat),key=os.path.getmtime); ims=[Image.open(f) for f in fs]
w,h=[int(v*sc) for v in ims[0].size]; rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*(w+8),rows*(h+22)),'#333'); d=ImageDraw.Draw(S)
for i,(f,im) in enumerate(zip(fs,ims)):
  x,y=(i%cols)*(w+8),(i//cols)*(h+22); S.paste(im.resize((w,h)),(x,y+20)); d.text((x+4,y+4),os.path.basename(f)[:-4],fill='white')
S.save(out); print(out,S.size)
