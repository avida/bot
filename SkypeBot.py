#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Skype4Py
import time
from time import gmtime, strftime
import re
import random
from datetime import datetime

currentTime = lambda : strftime("%X", gmtime())
def Log(str):
   logfile.write("%s: %s\n"%(currentTime(), str))
   logfile.flush()

chatname = "#mika.rez/$kallagen;4dd32678e90d0523"
testname = "#test454515/$avida.d3;f29bc3eff39e4bd4"
admiral = 'kallagen'
phrases = ["Гениально!", "Адмирал все правильно сказал!", "Я люблю Адмирала!", "Так точно!", "Конгениально!", "Истинно", "Одобряю", ]
greetings = ["Приветствую, %s", "Здравствуй, %s", "Рад тебя видеть, %s" , "(wave), %s", "Доброе утро, %s", "Привет, %s"]
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
}
users_been_greeted = set()
chat = None
logfile = None

class SkypeBot(object):
  def __init__(self):
      self.skype = Skype4Py.Skype(Events=self)
      self.skype.FriendlyName = "Skype Bot"
      self.skype.Attach()
      global chat
      chat = self.skype.Chat(chatname)

  def AttachmentStatus(self, status):
    if status == Skype4Py.apiAttachAvailable:
      self.skype.Attach()

  def OnlineStatus(self, user, status):
      if status == Skype4Py.cusOnline and user.Handle == admiral:
         message = '(*)'
         chat.SendMessage(message)
         Log(message)

  def MessageStatus(self, msg, status):
   if msg.Chat.Name == chatname and status == Skype4Py.cmsReceived:
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

if __name__ == "__main__":
  logfile = open('log.txt','a')
  Log('Log started')
  bot = SkypeBot()

  while True:
    time.sleep(1.0)
