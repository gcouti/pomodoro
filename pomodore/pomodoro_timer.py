#! /usr/bin/python

# The MIT License (MIT)

# Copyright (c) <year> <copyright holders>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import os
import gobject
import gtk
import appindicator
import time
import threading 
import pynotify
import settings
import logging 

logging.basicConfig(format=settings.LOG_FORMAT) 
LOG = logging.getLogger(__name__)
LOG.setLevel(settings.LOG_LEVEL)

gtk.gdk.threads_init()
pynotify.init("Timekpr notification") 

class PomodoroTimer():
    """
    This class represent master object of ubuntu indicator.

    Every pomodoro timer has indicator and timer
    """

    def __init__(self):
        LOG.debug("Init pomodoro")

        # create a menu
        self.menu = gtk.Menu()
        self.ind = Indicator()

        # create option to start pomodore
        self.menu_items = gtk.MenuItem("Start")
        self.menu_items.connect("activate", self.item_start_action)
        self.menu_items.show()
      
        self.menu.append(self.menu_items) 
      
        # create option to start pomodore
        self.menu_items = gtk.MenuItem("Exit")
        self.menu_items.connect("activate", self.item_exit_action)
        self.menu_items.show()
      
        self.menu.append(self.menu_items) 

        # Set menu for this indicator
        self.ind.ind.set_menu(self.menu)
        self.reset()

    def item_start_action(self,w):
        """
            Change conditions to START one pomodore cicle
        """
        LOG.debug("Start action")

        self.status = settings.STARTED 
        w.hide()
        
        # Option to reset pomodore
        self.menu_items = gtk.MenuItem("Reset")
        self.menu_items.connect("activate", self.item_reset_action)
        self.menu_items.show() 
        self.menu.prepend(self.menu_items) 

        # Option to stop pomodore
        self.menu_items = gtk.MenuItem("Stop")
        self.menu_items.connect("activate", self.item_stop_action)
        self.menu_items.show() 
        
        self.menu.prepend(self.menu_items) 

        LOG.debug("Start thread")
        thread = Timer(self,settings.WORK_TIME)
        thread.start()
      
        self.thread = thread
        
        LOG.debug("Status %s"%(self.status))
        LOG.debug("Cicles %s"%(self.worked_cicles))  

    def item_reset_action(self,w):
        """
            Change condition status to STARTED and reset worked cicles	
        """
        LOG.debug("Reseting action")

        self.status = settings.STARTED
        self.worked_cicles = 0 

        LOG.debug("Status %s"%(self.status))
        LOG.debug("Cicles %s"%(self.worked_cicles))

     
    def item_stop_action(self,w):
        """
          Change condition status to STOPPED and reset worked cicles
        """
        self.thread.stop()
        self.reset()
     
        visible_itens = ["Exit","Start"]

        for item in self.menu:
            if item.get_label() in visible_itens:
                item.show()
            else:
                item.hide()
 
        LOG.debug("Status %s"%(self.status))
        LOG.debug("Cicles %s"%(self.worked_cicles)) 


    def item_exit_action(self,w):
        """
          Exit from program
        """
        LOG.debug("Exiting program...")
        
        self.status=settings.STOPPED
        settings.EXIT=True
        gtk.main_quit()                     
        
        
        self.reset() 

    def reset(self):
        LOG.debug("Reset class")

        self.worked_time = 0
        self.worked_cicles = 0 
        
        self.thread = None
        self.status = settings.STOPPED 
        self.callback = self.end_pomodore_work 
        
    def end_pomodore_work(self):         
        """
            When pomodore work ends it must be execute
        """
        LOG.debug("End pomodore work")

        n = pynotify.Notification("Hora do descanso!","Fim do ciclo "+str(self.worked_cicles)+" de trabalho. Vamos descansar?")
        n.set_urgency(pynotify.URGENCY_CRITICAL)
        n.set_timeout(settings.NOTIFY_TIME)
        n.set_category("device")
        n.show()
    
        self.worked_cicles = self.worked_cicles + 1
        
        if self.worked_cicles >= settings.WORK_CICLES:
            self.callback = self.end_pomodore_cicle
            thread = Timer(self,settings.STOP_TIME)
            thread.start()
        else:
            self.callback = self.end_pomodore_rest
            thread = Timer(self,settings.REST_TIME)
            thread.start()
              
        self.thread = thread

    def end_pomodore_rest(self): 
        """
        """

        n = pynotify.Notification("Nao tem chororo!","O seu tempo acabou. Fim do ciclo de descanso, vamos trabalhar?")
        n.set_urgency(pynotify.URGENCY_CRITICAL)
        n.set_timeout(settings.NOTIFY_TIME) 
        n.set_category("device")
        n.show()

        self.callback =  self.end_pomodore_work
        thread = Timer(self,settings.WORK_TIME)
        thread.start()
            
        self.thread = thread

    def end_pomodore_cicle(self):
        """
        """

        n = pynotify.Notification("Fim dos ciclos pomodoro","Voce pode reiniciar seus ciclos")
        n.set_urgency(pynotify.URGENCY_CRITICAL)
        n.set_timeout(settings.NOTIFY_TIME)
        n.set_category("device")
        n.show()
        
        self.ind.reset()  

        # Hide unused menus
        for item in self.menu:
            LOG.debug("NM: " + item.get_label())
            if item.get_label() == "Stop" or item.get_label() == "Reset":
                item.hide()
            if item.get_label() == "Start":
                item.show()



class Indicator():
    """
      Indicator class for systray. Here we change values that will be showed for users
    """
    def __init__(self):
        LOG.debug("Init indicator")        
        self.ind = appindicator.Indicator("pomodore-indicator",
                                          "pomodore-init",
                                          appindicator.CATEGORY_APPLICATION_STATUS,
                                          settings.MEDIA + "indicator/")
        self.ind.set_status(appindicator.STATUS_ACTIVE)
    
    def change_icon(self,seconds,status=settings.WORKING):
        LOG.debug("Change icon pomodore-%s%s"%(status,seconds))
        self.ind.set_icon("pomodore-%s%s"%(status,seconds))

    def reset(self):
        LOG.debug("Reset pomodoro icon")
        self.ind.set_icon("pomodore-init") 


class Timer(threading.Thread):    
    """
        Timer is a thread that count time of pomodore timer 
    """
    def __init__(self,timer,time=0):
        threading.Thread.__init__(self)
        self.time = time
        self.timer = timer
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        self._Thread__stop()

    def stop_conditions(self):
        return settings.EXIT or self.timer.status == settings.STOPPED

    def run(self):
        i = self.time
        
        while i > 0:
            
            if self.time < settings.WORK_TIME:
                self.timer.ind.change_icon(i,settings.RESTING)
            else:
                self.timer.ind.change_icon(i)

            j = settings.MINUTES
            i = i -1
            
            while j > 0:
                time.sleep(1)
       
                if not self.timer.status == settings.PAUSED:
                    j = j -1
                
                if self.stop_conditions():
                    self.timer.ind.reset()
                    return 
             
        # The callback runs a GUI task, so wrap it!
        LOG.debug("End timer")
        gobject.idle_add(self.timer.callback) 

def main():
    """
        Initialize main pomodore    
    """
  
    LOG.debug("Start pomodore")
    
    PomodoroTimer()
  
    LOG.debug("Create GTK thread")
    gtk.main()
    LOG.debug("Exit main")

main()        
