#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Skype4Py
import time
from time import localtime, strftime
import re
import random
from datetime import datetime

currentTime = lambda : strftime("%X", localtime())
def Log(str):
   logfile.write("%s: %s\n"%(currentTime(), str))
   logfile.flush()

chatname = "#mika.rez/$kallagen;4dd32678e90d0523"
testname = "#test454515/$avida.d3;f29bc3eff39e4bd4"
admiral = 'kallagen'
phrases = ["Гениально!", "Адмирал все правильно сказал!", 
            "Я люблю Адмирала!", "Так точно!", "Согласен!", 
            "Истинно", "Одобряю", "Восхитительно!", "Я тоже так думаю",
            "Адмиралу виднее", "Золотые слова", "(Y)" ]
greetings = ["Приветствую, %s", "Здравствуй, %s", "Рад тебя видеть, %s" , "(wave), %s", "Доброе утро, %s", "Привет, %s", "Ку, %s"]
known_users = {
   'hawkeye_atm' : 'Хоукай',
   'andrew.rumm' : 'Рэйз',
   'asp_sn' : 'Ахилес',
   'den_flimitz' : 'Рамкей',
   'inv1zt' : 'Инвизич',
   'andrey.bembel' :  'Шизоид',
   'biruman_xpomocom' : 'Бируман',
   'unit_0013' : 'Татц',
   'trayich' : 'BlindedRageZ',
   'test454515' : 'Скайп бот',
   'browserofmetal' : 'Брауз',
   'ofelok' : 'Офелок',
   'mk777gif' : 'Ёж',
   'pelmeshko-s' : 'Пельмешко',
   'kallagen' : 'Адмирал',
   'podockonnik' : 'Подоконник',
   'kraken112' : 'Отрава',
   'enotpotoskyn' : 'Глебстер',
   'tussunplus' : 'Макар',
   'berdishenko' : 'Бердыщенко',
   'nikolaikopernik' : 'Коперник',
}
users_been_greeted = set()
chat = None
logfile = None
lastAttached = None
secondsToWait = 10
lastMessageTimestamp = time.mktime(localtime())
time4fun = 600

class SkypeBot(object):
  def __init__(self):
      self.skype = Skype4Py.Skype(Events=self)
      self.skype.FriendlyName = "Skype Bot"
      global lastAttached
      self.skype.Attach(Wait=False)
      lastAttached = time.mktime(localtime())
      global chat
      chat = self.skype.Chat(chatname)

  def AttachmentStatus(self, status):
    global lastAttached
    if status == Skype4Py.apiAttachAvailable:
      self.skype.Attach()
      lastAttached = time.mktime(localtime())

  def OnlineStatus(self, user, status):
      if time.mktime(localtime()) - lastAttached < secondsToWait:
         return
      if user.Handle == admiral:
         mesage = None
         if status == Skype4Py.cusOnline:
            message = '(*)'
         elif status == Skype4Py.cusOffline:
            message = 'Зима близится'
         if not message is None:
            chat.SendMessage(message.decode('cp1251'))
            Log(message)

  def MessageStatus(self, msg, status):
      global lastMessageTimestamp
      if time.mktime(localtime()) - lastAttached < secondsToWait:
         return
      if msg.Chat.Name == chatname and status == Skype4Py.cmsReceived:
         lastMessageTimestamp =  time.mktime(time.strptime(str(msg.Datetime), "%Y-%m-%d %H:%M:%S"))
         sender = msg.Sender
         if not sender.Handle in users_been_greeted:
            if sender.Handle in known_users:
               DisplName = known_users[sender.Handle]
            else:
               DisplName = sender.FullName.encode('cp1251')
            message = random.choice(greetings) % DisplName
            chat.SendMessage(message.decode('cp1251'))
            Log(message)
            users_been_greeted.add(sender.Handle)
         else:
            if msg.Sender.Handle == admiral:
               if random.random() < 0.4:
                  message = random.choice(phrases)
                  chat.SendMessage(message.decode('cp1251'))
                  Log(message)

def renewAnekdots():
   import urllib
   from bs4 import BeautifulSoup
   page = urllib.urlopen("http://www.anekdot.ru/scripts/rand_anekdot.php?t=j")
   soup = BeautifulSoup(page.read(), from_encoding="cp1251")
   return [ i.getText() for i in soup.findAll(attrs={'class':'text'}) ]
                 
if __name__ == "__main__":
  logfile = open('log.txt','a')
  Log('Log started')
  bot = SkypeBot()

  anekdots = renewAnekdots()
  while True:
    time.sleep(1.0)
    if time.mktime(localtime()) - lastMessageTimestamp > time4fun:
      if len(anekdots) == 0:
         anekdots = renewAnekdots()
      anek = anekdots.pop()         
      chat.SendMessage(anek)
      Log(anek.encode('cp1251', errors='ignore'))
