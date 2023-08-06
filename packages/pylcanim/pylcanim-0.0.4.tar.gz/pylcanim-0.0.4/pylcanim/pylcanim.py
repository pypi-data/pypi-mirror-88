import pygame
import json
pygame.init()

fps=0
c=0
data={}
img=0
width,height=0,0
def init(sfile):
    global data,img,width,height
    with open(sfile) as f:
        data=json.load(f)

    width=data['textureAtlas']['regionWidth']
    height = data['textureAtlas']['regionHeight']
   
    img=pygame.image.load(data['textureAtlas']['texture'])
def getList(d):
    l=[]
    for key in d.keys():
        l.append(key)
    return l
    
def lcAnim(fpslimit=2,animpos=0):
    global fps,c
    fps+=1
    l=getList(data['cycles'])
    if c>=len(data['cycles'][l[animpos]]['frames']):
        c=0
    if c<len(data['cycles'][l[animpos]]['frames']):
        img.set_clip(pygame.Rect(data['cycles'][l[animpos]]['frames'][c-1]*width,animpos*height,width,height))  # Locate the sprite you want
        draw_me = img.subsurface(img.get_clip())  # Extract the sprite you want
        if(fps>fpslimit):
            c =c+1
            fps=0
        #print(c)
        return draw_me

