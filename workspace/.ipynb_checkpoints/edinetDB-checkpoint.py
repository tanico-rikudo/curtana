from util import *
import pymysql.cursors
class edinetDB:
	def __init__(self,env,service_name,config_path):
		#set log
		self.util = UTIL(version=env,service_name=service_name)
		self.util.read_config(config_path)
		
	def get_connection(self):
		conn = pymysql.connect(
			user=self.util.config.get('USER'),
			passwd=self.util.config.get('PASSWORD'),
			host=self.util.config.get('HOST'),
			db=self.util.config.get('DB'),
			cursorclass=pymysql.cursors.DictCursor
		)
		# logging.info("[DONE]Get connection")
		return conn
	
	def close_connection(self,conn):
		try:
			conn.close()
			# logging.info("[DONE]Close connection")
		except Exception as e:
			logging.warning("[Failure] connection. Cannot find conn:{0}".format(e))
			
		
	def select(self,table):
		conn = self.get_connection()
		result = None
		try:
			sql = 'SELECT * FROM {table}'.format(table=table)
			with conn.cursor() as cursor:
				cursor.execute(sql)
				result = cursor.fetchall()
				# logging.info("[DONE]Select")
		except Exception as e:
			logging.warning("[Failure] connection. Cannot find conn:{0}".format(e))
		finally:
			self.close_connection(conn)
		return result

	def insert(self,table, data):
		conn = self.get_connection()
		try:
			keys = ','.join(data.keys())
			values = ','.join(['%s'] *len(data))
			sql = 'INSERT INTO {table} ({keys}) VALUES({values})'.format(table=table, keys=keys, values=values)
			with conn.cursor() as cursor:
				cursor.execute(sql, tuple(data.values()))
			conn.commit()
			# logging.info("[DONE]Insert")
		except Exception as e:
			logging.warning("[Failure] connection. Cannot find conn:{0}".format(e))
		finally:
			self.close_connection(conn)

	def update(self,table, data,cond):
		conn = self.get_connection()
		try:
			_vs = []
			sql = 'UPDATE  {0}  SET '.format(table)
			for _i , (_k,_v) in enumerate(data.items()):
				if _i > 0:
					sql += ', '
				sql += '`{0}`=%s '.format(_k )
				_vs.append(_v)
			sql += ' where REPORT_ID={0}'.format(cond['REPORT_ID'])
			with conn.cursor() as cursor:
				cursor.execute(sql, tuple(_vs))
			conn.commit()
			# logging.info("[DONE]UPDATE")
		except Exception as e:
			logging.warning("[Failure] connection. Cannot find conn:{0},{1}".format(e,sql,tuple(_vs)),exc_info=True)
		finally:
			self.close_connection(conn)


class edinetDBOperator:
	def __init__(self,env,service_name,config_path):
		self.dbOp = edinetDB(env,service_name,config_path)

	
	def insert_search_result(self,result):
		data={
			"SUBMIT_DT":result['submit_date'],
			"SUBMIT_TYPE":result['report_name'],
			"EDINET_CODE":result['edinet_code'],
			"SUBMITTER_NAME":result['submitter_name'],
			"DETAIL_URL":result['detail_url'],
			"PDF_URL":result['pdf_url'],
			"XBRL_URL":None,
			"FETCH_DT":dt.now().strftime("%Y-%m-%d %H:%M"),
			"SUCCESS_FLG":result['success_search_result'],
			"CRETAE_DT":dt.now().strftime("%Y-%m-%d %H:%M:%S"),
			"UPDATE_DT":dt.now().strftime("%Y-%m-%d %H:%M:%S")
		}
		self.dbOp.insert('search_result',data)
		
	def insert_detail_result(self,result):
		data={
			"BUYBUCK_DATE":result['date'],
			"BUYBUCK_VALUE":result['value'],
			"BUYBUCK_AMOUNT":result['amount'],
			"REPORT_ID":result['report_id'],
			"CRETAE_DT":dt.now().strftime("%Y-%m-%d %H:%M:%S"),
			"UPDATE_DT":dt.now().strftime("%Y-%m-%d %H:%M:%S")
		}
		self.dbOp.insert('detail_result',data)

	def update_search_result_sum(self,result,cond):
		data={
			"TOTAL_AMOUNT":result['sum_amount'],
			"TOTAL_VALUE":result['sum_value'],
			"TOTAL_COUNT":result['sum_count'],
			"UPDATE_DT":dt.now().strftime("%Y-%m-%d %H:%M:%S")
		}
		cond = {"REPORT_ID":cond['report_id']}
		self.dbOp.update('search_result',data,cond)	 
		  

		
	def get_fetched_search_result_rows(self):
		fetched_rows = []
		for row in self.dbOp.select('search_result'):
			row_result = {}
			row_result['report_id'] = row['REPORT_ID']
			row_result['submit_date'] = row['SUBMIT_DT']
			row_result['submit_type'] = row['SUBMIT_TYPE']
			row_result['edinet_code'] = row['EDINET_CODE']
			row_result['detail_url'] = row['DETAIL_URL']
			fetched_rows.append(row_result)
		return fetched_rows


	def check_already_fetched(self,submit_date,submit_type,edinet_code,db):
		# todo: change
		if len(db) == 0:
			return 0
		result = db.loc[
			((db.submit_date==submit_date)&
			(db.submit_type==submit_type)&
			(db.edinet_code==edinet_code)),:
		]
		return result.shape[0]


DB_SENTENCE_CONFIG= 'dbQuery.conf' 
class DBSentConf:
	def __init__(self,service_name,config_path):
		self.util = UTIL(version=service_name,service_name=service_name)
		self.util.read_config(config_path)
		self.__insertSearchResultRows=self.util.config.get("insertSearchResultRows")
		
	@property
	def insertSearchResultRows(self):
		pass
	
	@insertSearchResultRows.getter
	def insertSearchResultRows(self):
		return self.__insertSearchResultRows
