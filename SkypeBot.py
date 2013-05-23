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
def LogMessage(msg):
   DisplName = msg.Sender.Handle
   if DisplName in known_users:
      DisplName = known_users[DisplName]
   Log( DisplName+': '+msg.Body.encode('cp1251', errors='ignore'))
   

chatname = "#mika.rez/$kallagen;4dd32678e90d0523"
testname = "#test454515/$avida.d3;e755df567b71784f"
#chatname = testname
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
urlPattern = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^%s\s]|/)))')
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

  def MessageStatus(self, msg, status):
      global lastMessageTimestamp
      if msg.Chat.Name != chatname:
         return
      if status == Skype4Py.cmsSent:
         LogMessage(msg)
      elif status == Skype4Py.cmsReceived:
         LogMessage(msg)
         #if not urlPattern.search(msg.Body) is None:
         #  pass
         if time.mktime(localtime()) - lastAttached < secondsToWait:
            return
         lastMessageTimestamp =  time.mktime(time.strptime(str(msg.Datetime), "%Y-%m-%d %H:%M:%S"))
         sender = msg.Sender
         if not sender.Handle in users_been_greeted:
            if sender.Handle in known_users:
               DisplName = known_users[sender.Handle]
            else:
               DisplName = sender.FullName.encode('cp1251')
            message = random.choice(greetings) % DisplName
            chat.SendMessage(message.decode('cp1251'))
            users_been_greeted.add(sender.Handle)
         else:
            if msg.Sender.Handle == admiral:
               if random.random() < 0.4:
                  message = random.choice(phrases)
                  chat.SendMessage(message.decode('cp1251'))

def renewAnekdots():
   import urllib2
   from bs4 import BeautifulSoup
   page = urllib2.urlopen("http://www.anekdot.ru/scripts/rand_anekdot.php?t=j")
   soup = BeautifulSoup(page.read(), from_encoding="cp1251")
   return [ i.getText() for i in soup.findAll(attrs={'class':'text'}) ]
                 
if __name__ == "__main__":
  logfile = open('log-%s.txt' % strftime("%d-%m-%Y", localtime()),'a')
  Log('Log started')
  bot = SkypeBot()

  anekdots = renewAnekdots()
  while True:
    time.sleep(3.0)
    if time.mktime(localtime()) - lastMessageTimestamp > time4fun:
      if len(anekdots) == 0:
         anekdots = renewAnekdots()
      anek = anekdots.pop()         
      chat.SendMessage(anek)
      lastMessageTimestamp = time.mktime(localtime())
