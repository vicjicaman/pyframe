import sys
import tkinter
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
import time
import os
from dotenv import load_dotenv
import airtable
from typing import Dict
import random

load_dotenv()

BASE_ID = os.getenv('BASE_ID')
API_KEY = os.getenv('API_KEY')
TABLE_NAME = os.getenv('TABLE_NAME')

at = airtable.Airtable(BASE_ID, API_KEY)
images = []
root = tkinter.Tk()
duration=1000*60*1
msgs=[u"Retweeted by @vicjicama 🎉", 
u"+20 Likes this week!", 
u"Awesome place! - @natgeo",
u"Photo of the month",
u"From the last year",
u"Most Retweeted",
u"Amazing photo! - @discovery",
u"Retweeted by @commitdev 🎉"]

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()    
canvas = tkinter.Canvas(root,width=w,height=h)
canvas.pack()
canvas.configure(background='black')
font = ImageFont.truetype("./font/OpenSansEmoji.ttf", 28, encoding="unic")

def lookup():
    global images
    images = []
    result = []
    for r in at.iterate(TABLE_NAME):
        result.append(r)

    for row in result:
        val=list(row.values())[2]
        for field in list(val.values()):
            itv=field[0]
            if isinstance(itv, Dict):
                attachment=list(itv.values())
                images.append(attachment[3])
                print(attachment[3])

def close(event):
    root.withdraw() # if you want to bring it back
    root.destroy()
    sys.exit() # if you want to exit the entire thing

def showPIL(pilImage, msg): 
    imgWidth, imgHeight = pilImage.size
    #if imgWidth > w or imgHeight > h:
    #    ratio = min(w/imgWidth, h/imgHeight)
    #    imgWidth = int(imgWidth*ratio)
    #    imgHeight = int(imgHeight*ratio)
    #    pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    imgHeight = int(imgHeight*w/imgWidth)
    pilImage = pilImage.resize((w,imgHeight), Image.ANTIALIAS)
        
    pilImageMod = ImageDraw.Draw(pilImage)
    pilImageMod.rectangle(((0, 0), (500, 40)), fill="black")
    pilImageMod.text((5,5), msg, 'white', font)
    
    image = ImageTk.PhotoImage(pilImage)
    root.one = image
    imagesprite = canvas.create_image(w/2,imgHeight/2,image=image)

def clock(num):
    lookup()
    if num == len(images):
        root.after(duration,lambda : clock(0))
    else:
    	print(num)
    	im = Image.open(requests.get(images[num], stream=True).raw)
    	root.after(duration,lambda : clock(num+1))
    	msidx=random.randint(0, 7)
    	showPIL(im, msgs[msidx])
    	
root.bind('<Escape>', close)     	
clock(0)
root.mainloop()




