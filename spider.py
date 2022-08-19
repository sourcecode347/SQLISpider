#!/usr/bin/python3
# -*- coding utf-8 -*-
# Author SourceCode347
# SQLISpider

license = '''
MIT License

Copyright (c) 2021 Nikolaos Bazigos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

https://github.com/sourcecode347/SQLISpider/
'''

print(license)
import random,time,requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from termcolor import colored
from urllib.parse import urljoin
from random_word import RandomWords
import sys

r = RandomWords()
sqlilist="sqlilist.txt"
r_args=['-h','-f','-w','-n']
hless = False
iforms = False
cwind = False
nvuln = False
for arg in range(0,len(sys.argv)):
    if sys.argv[arg-1]=="-h":
        hless=True
    if sys.argv[arg-1]=="-f":
        iforms=True
    if sys.argv[arg-1]=="-w":
        cwind=True
    if sys.argv[arg-1]=="-w":
        nvuln=True
if cwind == True:
    import colorama
    colorama.init ()
logo = '''

 _______  _______  _       _________   _______  _______ _________ ______   _______  _______ 
(  ____ \(  ___  )( \      \__   __/  (  ____ \(  ____ )\__   __/(  __  \ (  ____ \(  ____ )
| (    \/| (   ) || (         ) (     | (    \/| (    )|   ) (   | (  \  )| (    \/| (    )|
| (_____ | |   | || |         | |     | (_____ | (____)|   | |   | |   ) || (__    | (____)|
(_____  )| |   | || |         | |     (_____  )|  _____)   | |   | |   | ||  __)   |     __)
      ) || | /\| || |         | |           ) || (         | |   | |   ) || (      | (\ (   
/\____) || (_\ \ || (____/\___) (___  /\____) || )      ___) (___| (__/  )| (____/\| ) \ \__
\_______)(____\/_)(_______/\_______/  \_______)|/       \_______/(______/ (_______/|/   \__/

                                                                                            

Coded By SourceCode347
'''
print(colored(logo , "green"))
def openbrowser():
    global browser
    options = webdriver.FirefoxOptions()
    if hless==True:
        options.add_argument("--headless")
    ser=Service("/home/zerocode/Desktop/SQLISpider/geckodriver")
    browser = webdriver.Firefox(service=ser,options=options)
    time.sleep(5)
def navigate(link):
    browser.get(link)
    time.sleep(8)
def is_vulnerable(source):
    """A simple boolean function that determines whether a page 
    is SQL Injection vulnerable from its `response`"""
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }
    for error in errors:
        # if you find one of these errors, return True
        if error in source.lower():
            return True
    # no error detected
    return False
openbrowser()
while True:
   rnum = random.randint(0,2)
   if rnum ==0:
       dork = "https://duckduckgo.com/?q="+str(r.get_random_word())+"&t=h_&ia=web"
   elif rnum ==1:
       dork = "https://duckduckgo.com/?q=%3Fid%3D"+str(random.randint(0,100000))+"&t=h_&ia=web"
   else:
       dork = "https://duckduckgo.com/?q=php%3Fid%3D"+str(random.randint(0,100000))+"&t=h_&ia=web"
   navigate(dork)
   testlinks=[]
   for x in range(0,5):
       try:
           m=browser.find_element(By.PARTIAL_LINK_TEXT,"More Results")
           m.click()
           time.sleep(3)
       except:
           pass
   fl = browser.find_elements(By.XPATH,"//a[@data-testid='result-title-a']")
   for l in fl:
       tl = l.get_attribute("href")
       #print(tl)
       testlinks.append(tl)
   for tl in testlinks:
       try:
           if "=" in tl:
               navigate(tl.replace("=","='"))
               source = browser.page_source
               if is_vulnerable(source) == True:
                   print(tl , colored("Vuln Found" , "green" , attrs=['bold']))
                   with open(sqlilist,"a") as f:
                      f.write(tl+"\n")
                      f.close()
               elif iforms==False and nvuln==True:
                   print(tl , colored("Not Found" , "red" , attrs=['bold']))
               else:
                   if iforms==True:
                       forms = browser.find_elements(By.XPATH,"//form")
                       print(f"[+] Detected {len(forms)} forms on {tl}.")
                       if len(forms) > 0:
                           for form in forms:
                               form_inputs = form.find_elements(By.XPATH,"//input")
                               action = form.get_attribute('action')
                               action=action.lower()
                               method = form.get_attribute('method')
                               method=method.lower()
                               for c in "\"'":
                                   # the data body we want to submit
                                   data = {}
                                   for fi in form_inputs:
                                       if fi.get_attribute('value') or fi.get_attribute('type') == "hidden":
                                           # any input form that has some value or hidden,
                                           # just use it in the form body
                                           try:
                                               data[fi.get_attribute('name')] = fi.get_attribute('value') + c
                                           except:
                                               pass
                                       elif fi.get_attribute('type') != "submit":
                                           # all others except submit, use some junk data with special character
                                           data[fi.get_attribute('name')] = f"test{c}"
                                   # join the url with the action (form request URL)
                                   url = urljoin(tl, action)
                                   if method == "post":
                                       res = requests.post(url, data=data)
                                       source=res.text
                                   elif method == "get":
                                       res = requests.get(url, data=data)
                                       source=res.text
                                   # test whether the resulting page is vulnerable
                                   if is_vulnerable(source) == True:
                                       #print("[+] SQL Injection vulnerability detected, link:", url)
                                       print(tl , colored("Vuln Found" , "green" , attrs=['bold']))
                                       with open(sqlilist,"a") as f:
                                          f.write(tl+"\n")
                                          f.close()
                                          break
                                   else:
                                       if nvuln==True:
                                           print(tl , colored("Not Found" , "red" , attrs=['bold']))
                       else:
                           if nvuln==True:
                               print(tl , colored("Not Found" , "red" , attrs=['bold']))
       except:
           pass
   #browser.quit()
   #break
