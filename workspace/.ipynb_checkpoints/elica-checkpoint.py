#basis
import datetime
from	datetime import datetime as dt
import time

#debug
import pickle

#util
import subprocess
import configparser
import logging
import csv
import socket
import time

from selenium import webdriver

# mail 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

from timeout_decorator import timeout, TimeoutError

import pandas as pd

# cron is run when current dir. pls move to your dir 




logging.basicConfig(level=logging.INFO,format='%(asctime)s:%(message)s')

from util import UTIL

class ELICA:
	def __init__(self,env,service_name,config_path):

		#True/False
		self.headless = True

		#set log
		self.util = UTIL(version=env,service_name=service_name)
		self.util.read_config(config_path)

		# sec
		self.default_timeout_sec = 200

		# history
		self.ls_url_sucess = []
		self.ls_url_failed = []



		self.browser_height = self.util.config.get('BROWSER_HEIGHT')
		self.browser_width  = self.util.config.get('BROWSER_WIDTH')

		#driver
		self.set_driver()

	def set_driver(self):
		options = webdriver.ChromeOptions()
		if self.headless:
			# options.add_argument('--headless')
			options.add_argument('--window-size='+str(self.browser_width)+','+str(self.browser_height))
			options.add_argument('--disable-gpu')
			options.add_argument('--disable-infobars')
			options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")
		if self.util.hostname == 'gcp':
			self.driver = webdriver.Chrome(options=options,executable_path="/home/kotetsu219specialpartner/bin/chromedriver")
		if self.util.hostname == 'macico':
			self.driver = webdriver.Chrome(options=options) 

		return True

	def del_driver(self):
		try:
			self.driver.quit()
			self.util.logger.info('[OK]Driver was killed')
		except Exception as e:
			self.util.logger.warning('[NG]Driver wasn\'t killed')
			return False

		try:
			self.util.run_cmd('pkill -9 chromedriver')
			self.util.logger.info('[OK]chromedriver process was killed')
		except Exception as e:
			self.util.logger.warning('[NG]chromedriver process wasn\'t killed:')
			return False

		return True

	def scroll_page(self, width, height):
		try:
			self.driver.execute_script("window.scrollTo(" + str(width) + "+, " + str(height) + ");")
			self.util.logger.info('[OK]Scrolled')	
		except Exception as e:
			self.util.logger.info('[NG]Cannot scroll')
			return False
		return True

	def stop_driver(self,time_for_wait):
		try:
			self.util.logger.info('[・]Driver enter wait time : %d',time_for_wait)
			time.sleep(time_for_wait)
			self.util.logger.info('[OK]Driver restart from wait time')
		except Exception as e:
			self.util.logger.warning('[NG]Driver occur error in waiting: %s',e)
			return False
		return True


	def to_page(self,url,**kwargs):

		if 'waittime' in kwargs.keys():
			waittime = kwargs['waittime']
		else:
			waittime = 0			
		if 'timeout_sec' in kwargs.keys():
			timeout_sec = kwargs['timeout_sec']
		else:
			timeout_sec = 120

		@timeout(timeout_sec)
		def access_page(url):
			self.driver.get(url)

		try:
			self.util.logger.info('[・]Accessing Web page.. : %s',url)
			access_page(url)
			self.util.logger.info('[OK]Driver get web page: %s',url)
			self.ls_url_sucess.append(url)
		except TimeoutError :
			self.util.logger.warning('[NG]Driver cannot get web page for timeout: %s',url)
			self.ls_url_failed.append(url)
			return False
		except Exception as e:
			self.util.logger.warning('[NG]Driver occur error in access page: %s',e)	
			self.ls_url_failed.append(url)
			return False

		if waittime>0:
			self.stop_driver(waittime)

		return True

