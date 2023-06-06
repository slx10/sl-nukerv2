import requests
import time
import os
from pystyle import Anime, Colorate, Colors, Center, System, Write, Box

vertical_bar = chr(124)

def send(web, msg, loop):
    data = requests.post(web, json={'content':msg})
    if data.status_code == 204:
        if loop == 0: 
            loop = 1
        print(Colorate.Horizontal(Colors.green_to_white,f"Message sent successfully [{msg}] [{loop}]",1))
        os.system(f"title Coffee v1.0 / Sent with success: {loop}")
        return "204"
    else:
        try:
            time.sleep(data.json()["retry_after"]/1000)
            return "rate_limit"
        except:
            pass

def spam(web, msg, inv, amount):
    loop = 0
    if amount == 0:
        while True:
            time.sleep(inv)
            if send(web, msg, loop) == "204":
                if loop == 0: loop += 2 
                else: loop += 1
            else:
                print(Colorate.Horizontal(Colors.red_to_white,f"Rate limit",1))
    else:
        amount += 1
    print(Colorate.Horizontal(Colors.green_to_red, f"Webhook link > {web}\nMessage > {msg}\nInterval > {inv}\nAmount > {amount-1}"))
    while loop < amount:
        time.sleep(inv)
        if send(web, msg, loop) == "204":
            if loop == 0: loop += 2 
            else: loop += 1
        else:
            print(Colorate.Horizontal(Colors.red_to_white,f"Rate limit",1))

banner = '''        ..
      ..  ..
            ..
             ..
            ..
           ..
         ..
##       ..    ####
##.............##  ##
##.............##   ##
##.............## ##
##.............###
 ##...........##
  #############
  #############
#################

   Press Enter'''

banner2 = '''    ___      __  __         
  / __|___ / _|/ _|___ ___ 
 | (__/ _ \  _|  _/ -_) -_)
  \___\___/_| |_| \___\___|'''

def init():
    System.Clear()
    System.Title("Coffee v1.0")
    Anime.Fade(text=Center.Center(banner), color=Colors.white_to_black, mode=Colorate.DiagonalBackwards, enter=True)

def setup():
    System.Clear()
    print(Colorate.DiagonalBackwards(Colors.rainbow, Center.XCenter(banner2), 1))
    print()
    print(Colorate.Horizontal(Colors.rainbow, Center.XCenter(Box.DoubleCube("Credits > SL#5115 | Follow me in TikTok > @silencebr"))))
    web = Write.Input("Webhook Url > ", Colors.white, interval=0.03)
    msg = Write.Input("Message > ", Colors.white, interval=0.03)
    inv = Write.Input("Interval > ", Colors.white, interval=0.03)
    amount = Write.Input("Amount(0 = Infinite) > ", Colors.white, interval=0.03)

    if bool(web) and bool(msg) and bool(inv) and bool(amount) == False:
        print(Colorate.Horizontal(Colors.red_to_white,f"Some value is empty",1))

    if inv.find("."):
        inv = float(inv)
    else:
        inv = int(inv)

    spam(web,msg,inv,int(amount))

if __name__ == '__main__':
    init()
    while True:
        setup()