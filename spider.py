#!/usr/bin/python3
# -*- coding utf-8 -*-
# Author SourceCode347
# SQLISpider

license = '''
MIT License

Copyright (c) 2021 SourceCode347

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
import random,time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from termcolor import colored

sqlilist="sqlilist.txt"

logo = '''
Simple

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
    options.add_argument("--headless")
    browser = webdriver.Firefox(executable_path="/home/baz/Desktop/geckodriver",options=options)
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
   dork = "https://duckduckgo.com/?q=php%3Fid%3D"+str(random.randint(0,100000))+"&t=h_&ia=web"
   navigate(dork)
   testlinks=[]
   for x in range(0,5):
       try:
           m=browser.find_element_by_partial_link_text("More Results")
           m.click()
           time.sleep(3)
       except:
           pass
   fl = browser.find_elements_by_xpath("//a[@class='result__url js-result-extras-url']")
   for l in fl:
       tl = l.text
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
               else:
                   print(tl , colored("Not Found" , "red" , attrs=['bold']))
       except:
           pass
   #browser.quit()
   #break
