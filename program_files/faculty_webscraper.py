from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import numpy as np
import time
import re

class Bot:
  def __init__(self):
    self.search_mode = "email" # options -- email / map
    self.search_term = " fine art department alumni directory contact"
    # self.search_term = " fine art gallery"
    self.current_search = ""
    print(chr(27) + "[2J")
    print("Initiating new Bot...\n")
    self.start = self.printtime()
    self.path = "./chromedriver"
    self.input = 'schools.txt'
    self.visitedurls = {"cat", "dog"}
    self.badwords = ["science", "drama", "theatre", "mathmatics"]
    self.badwords2 = ["recruitment", "admissions"]
    self.email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    self.googlinksmax = 3
    self.searches = []
    self.driver = None
    self.stack = []
    self.stack2 = []
    self.stack3 = []
    self.list = []
    self.max = 10
    self.arts = [] # useless but beautiful...

  def cycle(self):
    self.writestart()
    self.set()
    self.txt()
    if self.search_mode == "email":
      self.google()
    elif self.search_mode == "map":
      self.map_search()
    self.writestop()
    self.quit()

  def map_search(self):
    print("running google()...")
    self.driver.get("http://maps.google.com")
    # self.filter()
    self.sleep()
    # try:
    inputs = self.driver.find_elements_by_tag_name('input')
    self.current_search = self.searches.pop()
    term = self.current_search + self.search_term
    print('searching for', term, '...')
    for input in inputs:
      try:
        input.send_keys(term)
        input.send_keys(Keys.RETURN)
        self.get_map_names()
      except:
        print("input failure")

  def get_map_names(self):
    self.sleep()
    names = self.driver.find_elements_by_css_selector('.section-result-title span')
    print("names list length ------------------> ", len(names))
    print("names list --------------------------> ", names)
    for ele in names:
      name = ele.get_attribute('innerText')
      name_and_city = name + ", " + self.current_search
      print("inner html --------------------------> " + name_and_city)
      file = open("output.txt", "a")
      file.write(name_and_city)
      file.write("\n")
      print("done with new addition")
    self.sleep()
    print("is_not_last_page() -----> ", self.is_not_last_page())
    if self.is_not_last_page():
      print("more pages, recursing get_map_names()...")
      self.click_map_next()
      self.get_map_names()
    print("no more pages, exiting get_map_names() call...")
    

  def click_map_next(self):
    next_id = "n7lv7yjyC35__section-pagination-button-next"
    next_button = self.driver.find_element_by_id(next_id)
    next_button.click()
    self.sleep()

  def is_not_last_page(self):
    eles = self.driver.find_elements_by_css_selector('#n7lv7yjyC35__section-pagination-button-next.n7lv7yjyC35__button-disabled')
    if len(eles) > 0:
      return False
    return True


  # def add_to_output(self):
  #   file = open("output.txt", "a")
  #   while len(self.list) > 0:
  #     file.write(email)
  #     file.write("\n")
  #   self.popschool()

  def add_to_output(self, string):
    print("adding " + name_and_city + " to output")
    # file = open("output.txt", "a")
    # file.write(string)
    # file.write("\n")
    # print("done with new addition")


  def isartpage(self):
    source = self.driver.page_source
    str = self.removelinks(source.lower())
    if not any(x in str for x in self.badwords):
      return False
    return True

  def removelinks(self, urlstring):
    split = urlstring.split("<a")
    returnArr = []
    for ele in split:
      if "/a>" in ele:
        subSplit = ele.split("/a>")
        returnArr.append(subSplit[1])
      else:
        returnArr.append(ele)
    return "".join(returnArr)

  def writestart(self):
    file = open("output.txt", "a")
    file.write("starting at ----> ")
    file.write(self.start.strftime("%H:%M:%S"))
    file.write("\n")

  def writestop(self):
    now = datetime.now()
    file = open("output.txt", "a")
    file.write("stopping at ----> ")
    file.write(now.strftime("%H:%M:%S"))
    file.write("\n")

  def sleep(self):
    max = self.max
    min = 5
    totaltime = (max - min)*np.random.random() + min
    while totaltime > 0.5:
      # try:
      #   driver.set_context("chrome")
      #   win = driver.find_element_by_tag_name("window")
      #   if totaltime % 2 == 0:
      #     win.send_keys(Keys.COMMAND + "-")
      #   else:
      #     win.send_keys(Keys.COMMAND + "+")
      #   driver.set_context("content")
      # except:
      #   print("attempted zoom but no window element found")
      pause = 0.5 * np.random.random()
      totaltime = totaltime - pause
      print("pausing for", totaltime, "sec...")
      try:
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * Math.random());")
      except:
        print("no driver yet")
      time.sleep(pause)
    
  def emails(self):
    print("running self.emails()...")
    source = self.driver.page_source
    print("charactor length of source is", len(source))
    source = re.split('>|<|. |\)|\(|[|]|\"|\'|\`|\\n|/', source)
    # source = re.split('>|<|. ', source) # original glory...
    # print(source) # open the universe...
    self.arts.append(source)
    p = re.compile(self.email_regex)
    temps = [s for s in source if p.match(s)]
    for email in temps:
      if email not in self.list:
        if not any(wrd in self.badwords for wrd in email):
          self.list.append(email)
    print(self.list)
    print("closing self.emails ✓\n")

  def empty(self):
    print("running self.empty()...")
    print(len(self.list), " in self.list")
    file = open("output.txt", "a")
    while len(self.list) > 0:
      email = self.list.pop()
      print("adding", email, "to output.txt")
      file.write(email)
      file.write("\n")
    print(len(self.list), " in self.list")
    print("removing school from input txt file...\n")
    self.popschool()
    print("closing self.empty ✓\n")

  def set(self):
    print("running self.set()...")
    self.driver = webdriver.Chrome(self.path)
    print("closing self.set ✓\n")

  def check(self):
    print("\nrunning self.check()...")
    print(len(self.stack), 'items left in self.stack')
    print(len(self.searches), 'items left in self.searches')
    if len(self.stack) > 0:
      return self.unstack()
    if len(self.searches) > 0:
      self.empty()
      return self.google()
    self.quit()

  def google(self):
    print("running google()...")
    self.driver.get("http://google.com")
    self.filter()
    self.sleep()
    try:
      search = self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
      term = self.searches.pop() + self.search_term
      print('searching for', term, '...')
      search.send_keys(term)
      search.send_keys(Keys.RETURN)
      self.filter()
    except:
      print("failed to load page")
    self.sleep()
    self.getlinks()
    self.check()
    print("closing self.google ✓\n")

  def getlinks(self, stacknum = 1):
    print("running getlinks()...")
    searchdiv = self.driver.find_element_by_id("search")
    self.links = searchdiv.find_elements_by_tag_name("a") # delete later
    links = searchdiv.find_elements_by_tag_name("a")
    count = 0
    for link in links:
      url = link.get_attribute('href')
      if url != None:
        if "google" not in url:
          if not any(wrd in self.badwords for wrd in url):
            if ".edu" in url:
              if "@" not in url:
                if url not in self.visitedurls:
                  if count < self.googlinksmax:
                    self.visitedurls.add(url)
                    count = count + 1
                    if url not in self.stack:
                      if stacknum == 2:
                        self.stack2.append(url)
                      elif stacknum == 3:
                        self.stack3.append(url)
                      else:
                        self.stack.append(url)
    print("closing self.getlinks ✓\n")

  def getlinks2(self, stacknum = 1):
    print("running getlinks2()...")
    links = self.driver.find_elements_by_tag_name("a")
    for link in links:
      url = link.get_attribute('href')
      if url not in self.stack:
        if "google" not in url:
          if not any(wrd in self.badwords for wrd in url):
            if ".edu" in url:
              if "@" not in url:
                if "faculty" in url or "directory" in url or "staff" in url or "contact" in url:
                  if url not in self.visitedurls:
                    self.visitedurls.add(url)
                    if stacknum == 2:
                      self.stack2.append(url)
                      print("adding url to self.stack2 ----->", url)
                    elif stacknum == 3:
                      self.stack3.append(url)
                      print("adding url to self.stack3 ----->", url)
                    else:
                      self.stack.append(url)
                      print("adding url to self.stack ----->", url)
    print("closing self.getlinks2 ✓\n")

  def popschool(self):
    string = []
    with open(self.input, "r") as file:
      content = file.readlines()
      string = "".join(content[:-1])
    with open(self.input, "w") as file:
      file.write(string)

  def filter(self):
    # self.driver.execute_script("document.querySelector('body').style.filter = 'brightness(.8) saturate(0) contrast(10)';")
    self.driver.execute_script("document.querySelectorAll('*').forEach(ele => ele.style.filter = 'brightness(.8) saturate(0) contrast(10)');")
    self.driver.execute_script("document.querySelectorAll('*').forEach(ele => ele.style.border = '1px solid black');")

  def unstack(self):
    print("running unstack()...")
    while len(self.stack) > 0:
      url = self.stack.pop()
      print('\npopping new url off self.stack')
      print(len(self.stack), 'items in self.stack')
      print('redirecting to\n', url)
      try:
        self.driver.get(url)
        self.filter()
        self.sleep()
        if self.isartpage():
          self.emails()
        self.getlinks2(2)
      except:
        print("url / href is None")
    print('self.stack empty')
    if len(self.list) > 20:
      self.stack2 = []
    while len(self.stack2) > 0:
      self.stack2 = self.stack2[0:30]
      if len(self.list) > 50:
        self.stack2 = []
      try:
        url = self.stack2.pop()
      except:
        print("error bypassed ----> attempted stack2.pop on empty stack")
      print('\npopping new url off self.stack2')
      print(len(self.stack2), 'items in self.stack2')
      print('redirecting to\n', url)
      try:
        self.driver.get(url)
        self.filter()
        self.sleep()
        if self.isartpage():
          self.emails()
        self.getlinks2(3)
      except:
        print("url / href is None")
    print('self.stack2 empty')
    if len(self.list) > 20:
      self.stack3 = []
    while len(self.stack3) > 0:
      self.stack3 = self.stack2[0:30]
      if len(self.list) > 50:
        self.stack3 = []
      try:
        url = self.stack3.pop()
      except:
        print("error bypassed ----> attempted stack3.pop on empty stack")
      print('\npopping new url off self.stack3')
      print(len(self.stack3), 'items in self.stack3')
      print('redirecting to\n', url)
      try:
        self.driver.get(url)
        self.filter()
        self.sleep()
        if self.isartpage():
          self.emails()
      except:
        print("url / href is None")
    print('self.stack3 empty')
    print('\nall stacks empty')
    self.check()
    print("\nclosing self.unstack ✓\n")

  def txt(self):
    print("running txt()...")
    with open(self.input) as file:
      text = file.readline()
      while text:
          line = text.strip()
          self.searches.append(line)
          text = file.readline()
    self.sleep()
    print("closing self.txt ✓\n")

  def quit(self):
    if len(self.list) > 0:
      self.empty()
    self.printtime()
    print("started at ----> ", self.start.strftime("%H:%M:%S"))
    print("running quit()... all done!")
    self.driver.quit()

  def printtime(self):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("current time ---->", current_time)
    return now

test = Bot()
test.cycle()
