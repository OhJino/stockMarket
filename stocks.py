import robin_stocks as r
import pyotp
import getpass
import pygame
import sys
import random
from pygame.locals import *


screen_width = 1250
screen_height = 800
purple = (150, 0, 200)
red = (200, 0, 0)
blue = (0, 0, 200)
green = (0, 200, 0)
black = (0, 0, 0)

pygame.init()
surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crypto Graph")
surface.fill(black)
x = 0
y = 0

#Reference for doge price
j = 3600
doge_array = []
while (j < 4800):
    doge_array.append(j)
    j += 1

#price_height array
j = 100
price_height_array = []
while j < 1300:
    price_height_array.append(j)
    j += 1



x = screen_height
y = screen_width

robin_user = "jinoe@surewest.net"
robin_pass = "J!noe02000"
#robin_user = input("Enter your RH Username: ")
#robin_pass = getpass.getpass(prompt ='Enter your RH Password: ', stream=None)
totp = pyotp.TOTP("My2FactorAppHere").now()
print("Current OTP: ", totp)
login = r.login(robin_user, robin_pass)

 
my_stocks = r.build_holdings()
watchlist = r.profiles.load_investment_profile()
weekly_hour_opens = []
weekly_hour_closes = []
doge_dayprice = r.crypto.get_crypto_historicals('DOGE')
open_array = []
for sort_price in doge_dayprice:
    open_array.append(float(sort_price['open_price']))
open_array = sorted(open_array)
print(open_array)
spot_x = 50
close_spot_flag = 0
close_spot_x = 0
close_y = 0
for day in doge_dayprice:
    converted_open = float(day['open_price'])
    converted_close = float(day['close_price'])
    weekly_hour_opens.append(converted_open)
    weekly_hour_closes.append(converted_close)
    if int(converted_open * 1000000) in doge_array:
        #need to get corresponding index between doge_array and price_height_array
        graph_spot = doge_array.index(int(converted_open * 1000000))
        price_y = (1300 - price_height_array[graph_spot])
        start_spot_x = spot_x
        pygame.draw.rect(surface, blue, [start_spot_x, price_y, 3, 3])
        spot_x += 3
    if int(converted_close * 1000000) in doge_array:
        if (close_spot_flag == 0):
            close_spot_x = start_spot_x
            close_y = price_y
            close_spot_flag += 1
        old_close_spotx = close_spot_x
        old_close_spoty = close_y
        graph_spot = doge_array.index(int(converted_close * 1000000))
        close_y = (1300 - price_height_array[graph_spot])
        close_spot_x = spot_x
        pygame.draw.rect(surface, blue,[close_spot_x, close_y, 3, 3])
        spot_x += 3
        pygame.draw.line(surface, green, (old_close_spotx, old_close_spoty), (start_spot_x, price_y))
        pygame.draw.line(surface, green, (start_spot_x+1, price_y), (close_spot_x+1, close_y))
        

#print(weekly_hour_closes)
#print(weekly_hour_opens)


    #print(day['open_price'])
#list_length = len(btc_dayprice)

btc_price = r.crypto.get_crypto_info('BTC')
#print(btc_price)
#print(my_stocks.items)
#for key,item in my_stocks.items():
    #print(key,item)

doge = r.crypto.get_crypto_quote("DOGE")
#print(doge['ask_price'])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit
        if event.type == KEYDOWN and event.key == K_RETURN:
            pygame.draw.line(surface, green, (savestartx, savestarty), (ranstartx, ranstarty))
    pygame.display.update()

r.logout()