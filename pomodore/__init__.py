#

"""
    Hello welcome to pomodore tecnic. This application will mark your
    work time and will notify you when you must rest

    ROADMAP:

    1 - BEEP when cicles are done
    2 - ALERT when cicles are done
    3 - In rest choose some options to do, see twitter, facebook rest
        eyes, read some news or links in remember the milk
            1 - List some options to do. See twitter, see facebook, chat, with some friend.
            2 - Improve list, choose list
            3 - Remember the milk or similar
            4 - Knows if i am tired and show me something more happy

    4 - Future: Transform it in something "inteligent" 
        * Say me how many e-mails does i have
        * Pause when i have some meet
        * In start of the day say to me what is my events.

"""
import os
import gtk
import pynotify
import settings
import logging
import settings

from pomodoro_timer import *

logging.basicConfig(format=settings.LOG_FORMAT) 
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

gtk.gdk.threads_init()
pynotify.init("Timekpr notification")


def main():
    """
        Initialize main pomodore    
    """
  
    LOG.debug("Start pomodore")
    
    pomodoro_timer.PomodoroTimer()
  
    LOG.debug("Create GTK thread")
    gtk.main()
    LOG.debug("Exit main")

main()
