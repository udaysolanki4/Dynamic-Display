import max7219.led as led
from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT 
from firebase import firebase

firebase=firebase.FirebaseApplication('Enter Firebase API') # Enter your firebase api
data=("bright","font","orient","inverted","speed") 
data1=[15,None,0,0,0.05]
flag=0
device = led.matrix(cascaded=4)
def crop(n):# this function used to crop string to appropriate manner
   return n[1:len(n)-1]
def initialize(s):# initialzing function for all data entry
    b=firebase.get('/iot',s)
    
    if(s=="bright"):
        b=bright(b)
    elif(s=="font"):
        b=crop(b)
        b=fon(b)
    elif(s=="orient"):
        b=crop(b)
        b=ori(b)
    elif(s=="inverted"):
        b=crop(b)
        b=inve(b)
    else:
        b=spee(b)
    return b
def bright(b):
    if(b.isdigit()==1):
        b=int(b)%16
    else:
        b=15
    return b
def fon(c):
    
     if(c=="Style 1"):
         c=SINCLAIR_FONT
     elif(c=="Style 2"):
         c=TINY_FONT
     elif(c=="Style 3"):
         c=CP437_FONT
     else:
         c=None
    
     return c
def ori(d):
    if(d.isdigit()==True):
        d=int(d)
        
        if(d not in [90,180,270]):
            d=0
    else:
        d=0
    
    return d
def inve(e):
    if(e.isdigit()==True):
        e=int(e)
        if(e!=1):
            e=0
    else:
        e=0
    return e
def spee(f):
    if(f.isdigit()):
        f=int(f)
        if(f>=1 and f<=10):
            f=f/float(100)
        else:
            f=0.05
    else:
        f=0.05
    return f
def ser1():
    global flag
    while(flag==0):

        global device
        a=firebase.get('/iot','message')
        g=firebase.get('/iot','commit')
        a=crop(a)
        g=crop(g)
        
        if(g=='1'):
            
            for i in range(5):
                data1[i]=initialize(data[i])
            firebase.put('/iot','commit','\"0\"')
                
        
        
            
        device.invert((data1[3]))
        device.orientation((data1[2]))
        device.brightness((data1[0]))
        device.show_message(a,data1[1],data1[4])
        print(a)
        h=firebase.get('/iot','stat')
        h=crop(h)
        if(h=="1"):
            flag=1
    ser2()
            
    
            
def ser2():
    global flag
    global device
    while(flag==1):
        device.flush()
        h=firebase.get('/iot','stat')
        h=crop(h)
        if(h=="0"):
            flag=0
    ser1()
ser1()
