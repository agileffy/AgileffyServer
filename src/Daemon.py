import threading
import time


def remove_incomplete_document():  # fixme
    pass


def Daemon():
    remove_incomplete_document()
    timer = threading.Timer(5, Daemon)
    timer.start()


def initDaemon():
    Daemon()
