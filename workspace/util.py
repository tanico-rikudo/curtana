import logging
import socket
from datetime import datetime as dt
import configparser
import pandas as pd
#独自
class NotFoundElementException(Exception):
	pass

class AccessFailedException(Exception):
	pass

class UTIL:

	def __init__(self,version,service_name):

		# order should be kept
		####	start
		self.version = version
		self.service_name =service_name
		self.set_logger()
		#### end

		# 
		self.dt_init = dt.now()
		self.get_machine_localname()

	def set_logger(self):
		self.logger = logging.getLogger(self.service_name)

	def read_config(self,path_conf):
		logging.info(path_conf)
		config = configparser.ConfigParser(default_section="COMMON")
		config.read(path_conf,encoding='utf-8')
		target_config = config[self.version]
		if target_config is None:
			return False
		else: 		
			self.config = target_config
			return True

	def set_time(self):
		self.now = datetime.datetime.now()

	def run_cmd(self,cmd):
		try:
			subprocess.call(cmd.split())	
		except Exception as e:
			self.logger.warning('[NG]Cannot execute cmd: %s', e)
			return False
		return True

	def get_machine_localname(self):
		try:
			hostname = socket.gethostname()
			if hostname == 'Macico.local':
				self.hostname = 'macico'
			elif hostname == 'elica03':
				self.hostname = 'gcp'
			else:
				self.hostname = 'unknown'
				raise NotFoundElementException('Cannot find host in known host list : '+hostname)

			self.logger.info('[OK]Set host: %s', hostname)

		except NotFoundElementException as e:
			self.logger.warning('[NG]Set unknown host: %s', e)

		except Exception as e:
			self.logger.warning('[NG]Cannot find host for unknown error: %s', e)
			return False

		return True

	def create_dataframe(self,data,columns):
		return pd.DataFrame(data,columns=columns)
