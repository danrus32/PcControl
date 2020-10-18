import random
import time
import datetime
import requests
import re
import os
import pyautogui
import sqlite3


token = ""
grupid = ""
v = 5.95
def RandomId():
    a = random.randint(1,100000)
    return a
def Time():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d %H:%M:%S")

debug_mode = True



