# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback
from datetime import datetime

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.fishwars
users=db.users

fighthours=[12, 17, 22]
sealist=['crystal', 'black', 'moon']
officialchat=441399484

try:
    pass

except Exception as e:
    print('Ошибка:\n', traceback.format_exc())
    bot.send_message(441399484, traceback.format_exc())

    
def seafight():
    seas={}
    cusers=users.find({})
    for ids in sealist:
        seas.update(createsea(ids))
    for ids in cusers:
        if ids['battle']['action']=='def':
            seas[ids['sea']]['defers'].update({ids['id']:ids})
        elif ids['battle']['action']=='attack':
            seas[ids['battle']['target']]['attackers'].update({ids['id']:ids})
    
    for ids in seas:
        sea=seas[ids]
        for idss in sea['defers']:
            user=sea['defers'][idss]
            sea['defpower']+=user['stats']['def']
        for idss in sea['attackers']:
            user=sea['attackers'][idss]
            sea['attackerspower']+=user['stats']['attack']
            
        if sea['defpower']<sea['attackpower']:
            sea['saved']=False
    text=''
    for ids in seas:
        sea=seas[ids]
        if sea['saved']==False:
            text+='🗡'+sea_ru(sea['name'])+' море потерпело поражение в битве! Топ атакующих:\n'
            who='attackers'
            stat='attack'
            text+=battletext(sea, who, stat)
            text+='Топ защитников:\n'
            who='defers'
            stat='def'
            text+=battletext(sea, who, stat)
        else:
            text+='🛡'+sea_ru(sea['name'])+' море отстояло свою территорию! Топ защитников:\n'
            who='defers'
            stat='def'
            text+=battletext(sea, who, stat)
            text+='Топ атакующих:\n'
            who='attackers'
            stat='attack'
            text+=battletext(sea, who, stat)
    bot.send_message(officialchat, 'Результаты битвы:\n\n'+text)
            
            
         
        
def battletext(sea, who, stat):
    top=5
    i=0
    text=''
    alreadyintext=[]
    while i<top:
        intext=None
        maxstat=0
        for idss in sea[who]:
            user=sea[who][idss]
            if user['stats'][stat]>maxstat and user['id'] not in alreadyintext:
                maxstat=user['stats'][stat]
                intext=user
        if intext!=None:
            alreadyintext.append(intext['id'])
            text+=intext['gamename']
            if i+1==top:
                text+=', '
            else:
                text+='.\n\n'
        i+=1
    return text
            
            
   
def sea_ru(sea):
    if sea=='crystal':
        return '💎Кристальное'
    if sea=='black':
        return '⚫️Чёрное'
    if sea=='moon':
        return '🌙Лунное'

   
def createsea(sea):
    return {
        'name':sea,
        'defpower':0,
        'attackerspower':0,
        'defers':{},
        'attackers':{},
        'saved':True
    }

def timecheck():
    ctime=str(datetime.fromtimestamp(time.time()+3*3600)).split(' ')[1]
    chour=int(ctime.split(':')[0])
    if chour in fighthours:
        seafight()
    
    
    
print('7777')
bot.polling(none_stop=True,timeout=600)

