import random
import time
import datetime
import requests
import re
import os
import pyautogui
import sqlite3


token = "d27d9d1ca274a8f89a1bf7ffad503c440e96eba2ef6c2bd483ced57c7d0addfcf10fddb0f6eff541572e6"
grupid = "199561725"
v = 5.95
def RandomId():
    a = random.randint(1,100000)
    return a
def Time():
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d %H:%M:%S")

debug_mode = True



