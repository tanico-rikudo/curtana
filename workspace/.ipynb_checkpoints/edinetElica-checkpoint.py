import re
import pandas as pd
import time

#crawl

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# diy
from edinetDB import  edinetDBOperator
from util import *

bar_pattern = '.*[-ー－―]+'
void_dt_pattern = '[月日\s]'


class edinet_elica:
    def __init__(self,env,service_name,agent,db_obj,config_path):
        self.agent = agent
        self.db_obj = db_obj
        self.util = UTIL(version=env,service_name=service_name)
        self.util.read_config(config_path)
        self.search_result_in_db = None
        self.fetch_search_result_db()

    def fetch_search_result_db(self):
        self.search_result_in_db = self.util.create_dataframe(
            self.db_obj.get_fetched_search_result_rows(),["report_id","submit_date","submit_type","edinet_code","detail_url"] )

    def to_search_results(self,current_page_no=0,go_to_page=1):
        assert go_to_page!=0, "Cannnot move myself"
        assert (current_page_no+go_to_page)>=0,  "page_no must be higher than min."
        upper_pager = self.agent.driver.find_elements(By.XPATH, "//p[@class='pageLink']")[0] # get upper
        page_link_btns = [ pageLink for pageLink in (upper_pager.find_elements(By.XPATH, "span[not(contains(@class,'current'))]")) if "ページ" not in pageLink.text]
        max_pages = len(page_link_btns)
        
        #adjust
        if go_to_page > 0:
            go_to_page-=1
        new_age_no =  current_page_no+go_to_page
        assert new_age_no < max_pages, "page_no must be lower than max({0}).".format(max_pages)
        page_link_btns[new_age_no].click()
        
        #adjust
        if go_to_page >= 0:
            new_age_no+=1
        return new_age_no,max_pages
        
    def get_search_result_rows(self):
        search_result_table_parent = self.agent.driver.find_elements(By.XPATH, "//div[@class='result']")[0] # get resutl
        search_result_table = search_result_table_parent.find_elements(By.XPATH, "table")[0] #get table 
        search_result_rows = search_result_table.find_elements(By.XPATH, "tbody/tr[not(contains(@class,'tableHeader'))]") #get row
        return search_result_rows

    def analyze_search_result_row(self,row):
        tds = row.find_elements(By.XPATH, "td")
        submit_date = tds[0].text
        detail_link_obj = tds[1]
        edinet_code = tds[2].text
        submitter_name= tds[3].text
        pdf_url= tds[5].find_element_by_tag_name('a').get_attribute("href")
        xbrl_link_obj= tds[6]
        report_name =  detail_link_obj.text
        logging.info("{0}-{1}".format(edinet_code,submitter_name))
        row_result = {'submit_date':self.connvert_edinet_submit_date_to_dt(submit_date),'report_name':report_name, 'edinet_code':edinet_code, 
                    'submitter_name':submitter_name,'pdf_url':pdf_url,'xbrl_link_obj':xbrl_link_obj,'detail_link_obj':detail_link_obj }
        return row_result


    def to_content_in_detail(self):
        # Action to display Content
        self.agent.driver.switch_to.frame(self.agent.driver.find_elements(By.XPATH, "//frame")[1])
        self.agent.driver.switch_to.frame(self.agent.driver.find_elements(By.XPATH, "//frame")[1])

        leftbar_body = self.agent.driver.find_elements(By.XPATH, "//body")[0]
        fetch_content_btn = self.agent.driver.find_elements(By.XPATH, "//a[contains(text(), '取得状況')]")[0]
        fetch_content_btn.click()
        self.agent.driver.switch_to.default_content()
        time.sleep(1)

        # Action to move onto Content
        self.agent.driver.switch_to.frame(self.agent.driver.find_elements(By.XPATH, "//frame")[1])
        self.agent.driver.switch_to.frame(self.agent.driver.find_elements(By.XPATH, "//frame")[2])

        content = self.agent.driver.find_elements(By.XPATH, "//body")[0]
        return content

    def scrtutinize_contetnt_in_detail_bytext(self,content):
        progress_reports = content.find_elements(By.XPATH, "//*[contains(text(), '報告月における取得自己株式')]")
        content_result = {}
        if len(progress_reports) == 0:
            logging.warning("[Skip] No mutch 報告月における取得自己株式 ")
        for type_no in  range(len(progress_reports)):
            # Expected: 株主総会決議による取得の状況】 and 【取締役会決議による取得の状況】
            content_result[type_no] = None

            #find table obj ( it is parent obj)
            parent_report_table =progress_reports[type_no]
            cannot_find_record_tr =False
            while parent_report_table.tag_name != 'tr':
                try:
                    # If html tag, error
                    parent_report_table = parent_report_table.find_element_by_xpath('..')
                except:
                    cannot_find_record_tr = True
                    break
            if cannot_find_record_tr:
                break

            # Search base on upper level tr
            parent_report_table = parent_report_table.find_element_by_xpath('..')
            report_rows = parent_report_table.find_elements_by_tag_name('tr')
            report_result = {'daily':[],'total':None}
            logging.info("Find {0} rows. Look up rows".format(len(report_rows)))

            # replace text
            table_strs = parent_report_table.text.replace(",","").replace(" ","").split("\n")
            table_strs = [ _str  for _str in [re.sub(bar_pattern,"",_str) for _str in table_strs] if _str != ""]
            logging.info(table_strs)
            try:
                sum_idx = table_strs.index("計")
                report_rows=table_strs[[ _i  for _i, _str in enumerate(table_strs) if '報告月における取得自己株式' in _str ][0]+1:sum_idx]
                for _i in range(0,len(report_rows),3):
                    date_col_txt =  report_rows[_i]
                    if "月" in date_col_txt:
                        if "日" in date_col_txt:
                            if  re.match(bar_pattern, date_col_txt) is None and re.sub(void_dt_pattern, '', date_col_txt) != '':
                                try:
                                    month = str(int(date_col_txt.split('月')[0])).zfill(2)
                                    day = str(int(date_col_txt.split('月')[1].split('日')[0])).zfill(2)
                                    dt = month+day
                                    qty = int(report_rows[_i+1].replace(',', ''))
                                    value = int(report_rows[_i+2].replace(',', ''))
                                    if qty is not None:
                                        report_result['daily'].append({'date':dt,'qty':qty,'value':value})
                                        logging.info("Data: {0}".format(report_result['daily'][-1]))
                                    else:
                                        logging.info("Data: No data")
                                except:
                                    logging.warning("No Daily")

                # sum
                qty_col_txt = table_strs[sum_idx+1]
                if  re.match(bar_pattern, qty_col_txt) is None:
                    try:
                        sum_qty = int(qty_col_txt.replace(',', ''))
                        sum_value = int(table_strs[sum_idx+2].replace(',', ''))
                        if sum_qty is not None:
                            report_result['total'] = {'qty':sum_qty,'value':sum_value}
                            logging.info("Sum : {0}".format(report_result['total']))
                        else:
                            logging.info("Sum: No data")
                    except Exception as e:
                        logging.warning("No Daily sum")
                else:
                    report_result['total'] = {'qty':0,'value':0}

                report_result['daily_total'] = len(report_result['daily'])
                content_result[type_no] = report_result
                logging.info("Daily report: {0} rows are fetched.".format(len(report_result['daily'])))
            except Exception as e:
                logging.warning("No 計")
        return content_result

    def scrtutinize_contetnt_in_detail(self,content):
        progress_reports = content.find_elements(By.XPATH, "//*[contains(text(), '報告月における取得自己株式')]")
        content_result = {}
        if len(progress_reports) == 0:
            logging.warning("[Skip] No mutch 報告月における取得自己株式 ")
        for type_no in  range(len(progress_reports)):
            # Expected: 株主総会決議による取得の状況】 and 【取締役会決議による取得の状況】
            content_result[type_no] = None

            #find table obj ( it is parent obj)
            parent_report_table =progress_reports[type_no]
            cannot_find_record_tr =False
            while parent_report_table.tag_name != 'tr':
                try:
                    # If html tag, error
                    parent_report_table = parent_report_table.find_element_by_xpath('..')
                except:
                    cannot_find_record_tr = True
                    break
            if cannot_find_record_tr:
                break

            # Search base on upper level tr
            parent_report_table = parent_report_table.find_element_by_xpath('..')
            report_rows = parent_report_table.find_elements_by_tag_name('tr')
            report_result = {'daily':[],'total':None}
            logging.info("Find {0} rows. Look up rows".format(len(report_rows)))
            for i_report_row in range(len(report_rows)):
                report_row = report_rows[i_report_row]
                qty, value = None, None
                sum_qty, sum_value = None, None
                report_cols = report_row.find_elements_by_tag_name('td')

                if "日現在" in report_cols[0].text:
                    continue
                if len(report_cols) <=1:
                    continue

                date_col_txt = report_cols[1].text
                if "月" in date_col_txt:
                    if "日" in date_col_txt:
                        if  re.match(bar_pattern, date_col_txt) is None and re.sub(void_dt_pattern, '', date_col_txt) != '':
                            month = str(int(date_col_txt.split('月')[0])).zfill(2)
                            day = str(int(date_col_txt.split('月')[1].split('日')[0])).zfill(2)
                            dt = month+day
                            qty = int(report_cols[2].text.replace(',', ''))
                            value = int(report_cols[3].text.replace(',', ''))
                            if qty is not None:
                                report_result['daily'].append({'date':dt,'qty':qty,'value':value})
                                logging.info("Data: {0}".format(report_result['daily'][-1]))
                            else:
                                logging.info("Data: No data")

                #　計がきたらおしまい（ループ）
                if report_row.text.startswith("計") and report_row.tag_name == 'tr':
                    report_cols = report_row.find_elements_by_xpath('td')
                    qty_col_txt = report_cols[2].text
                    if  re.match(bar_pattern, qty_col_txt) is None:
                        sum_qty = int(report_cols[2].text.replace(',', ''))
                        sum_value = int(report_cols[3].text.replace(',', ''))
                        if sum_qty is not None:
                            report_result['total'] = {'qty':sum_qty,'value':sum_value}
                            logging.info("Sum : {0}".format(report_result['total']))
                        else:
                            logging.info("Sum: No data")
                    break
            report_result['daily_total'] = len(report_result['daily'])
            content_result[type_no] = report_result
            logging.info("Daily report: {0} rows are fetched.".format(len(report_result['daily'])))
        return content_result


    def connvert_edinet_submit_date_to_dt(self,text):
        try:
            year,mmddhhmm=text.split(".",1)
            jp_year_num=int(re.sub('[^0-9]','',year))
            jp_year_unit=re.sub('[0-9]','',year)
            dt_obj = dt.strptime(mmddhhmm,"%m.%d %H:%M")
            jp_calendar_to_ad={"R":2019,'H':1989}
            ad_year=jp_calendar_to_ad[jp_year_unit]+jp_year_num
            return dt_obj.replace(year=ad_year).strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            return text
        return 

    def fetch_search_result(self):
        self.agent.to_page(self.util.config.get("BUYBUCK_SEARCH_RESULT_URL"))
        time.sleep(2)
        page_no = 0 
        while True:
            search_result_rows = self.get_search_result_rows()
            page_result = []
            for i_row in range(len(search_result_rows)):
                try: 
                    row_result = self.analyze_search_result_row(search_result_rows[i_row])
                    row_result['success_search_result'] = 0
                    
                    # Only 自己
                    if row_result['report_name'] != '自己株券買付状況報告書（法２４条の６第１項に基づくもの）':
                        continue
                        
                    # check in db
                    n_db_result = self.db_obj.check_already_fetched(
                        row_result['submit_date'],row_result['report_name'],row_result['edinet_code'],self.search_result_in_db)
                    if n_db_result>0:
                        logging.info("[Skip] Already Fetched and Inseted into DB: {0}-{1}".format(row_result['submit_date'],row_result['edinet_code']))
                        continue
                        
                    
                    row_result['detail_link_obj'].click()
                    time.sleep(3)
                    try:
                        # Entry detail window
                        self.agent.driver.switch_to.window(self.agent.driver.window_handles[1])
                        
                        # record
                        row_result['detail_url']= self.agent.driver.current_url
                        row_result['success_search_result'] = 1 
                        
                        #end
                        self.agent.driver.switch_to.default_content()
                        self.agent.driver.close() 

                    except Exception as e :
                        logging.warning("Detail screen error(L2): {0}".format(e),exc_info=True)
                    finally:
                        #　return search  result
                        handle_array = self.agent.driver.window_handles
                        self.agent.driver.switch_to.window(handle_array[0])

                except Exception as e :
                    logging.warning("Detail screen error(L1): {0}".format(e),exc_info=True)
                    
                self.db_obj.insert_search_result(row_result)
                page_result.append(row_result)
                logging.info("Done: {0}-{1}".format(row_result['submit_date'],row_result['edinet_code']))
            
            logging.info("[DONE] Page={0}".format(page_no))
            try:
                page_no, n_pages = self.to_search_results(page_no,1)
                logging.info("Next Page={0}".format(page_no))
            except:
                logging.info("Finish. Now Page={0}".format(page_no))
                break

    def fetch_detail(self,url):
        self.agent.to_page(url)
        time.sleep(2)
        detail_result = {}
        try:
            content=self.to_content_in_detail()
            # detail_result = self.scrtutinize_contetnt_in_detail(content)
            detail_result = self.scrtutinize_contetnt_in_detail_bytext(content)
        except Exception as e :
            logging.warning("Detail screen error(L3): {0}".format(e),exc_info=True)
        finally:
            pass

        return detail_result



    def fetch_detail_form_search(self):
        for _idx in self.search_result_in_db.index:
            _row = self.search_result_in_db.loc[_idx,:]
            report_id = _row['report_id']
            detail_url = _row['detail_url']
            submit_dt = dt.strptime(str(_row['submit_date']),'%Y-%m-%d %H:%M')
            submit_date = int(submit_dt.strftime('%Y%m%d'))
            submit_y    = int(submit_dt.strftime('%Y'))
            submit_mmdd = int(submit_dt.strftime('%m%d'))
            submit_code = _row['edinet_code']
            submit_y , submit_mmdd = submit_date//10000 , submit_date%10000
            detail_results=self.fetch_detail(detail_url)
            success_cnt,total_cnt=0,0
            for _key in detail_results.keys():
                _result = detail_results[_key]
                try:
                    if _result is None:
                        # No Table
                        continue
                    if "daily" in _result.keys():
                        daily_results = _result['daily']
                        for _result in daily_results:
                            try:
                                total_cnt+=1
                                insert_data = {}
                                insert_data['report_id'] = report_id
                                buybuck_date=int(_result['date'])
                                if buybuck_date < submit_mmdd:
                                    insert_data['date'] = buybuck_date+submit_y*10000
                                else:
                                    insert_data['date'] = buybuck_date+(submit_y-1)*10000
                                insert_data['date'] = dt.strptime(str(insert_data['date']),'%Y%m%d').strftime('%Y-%m-%d')
                                insert_data['amount'] = _result['qty']
                                insert_data['value'] = _result['value']
                                self.db_obj.insert_detail_result(insert_data)
                                success_cnt+=1
                            except Exception as e:
                                logging.warning("[Failure] Cannot transact. Code={0}:{1}".format(submit_code,e),exc_info=True)
                        logging.info("[DONE] Inserted Daily EdinetCode={0}, Date={1}, {2}/{3}".format(submit_code,submit_date,success_cnt,total_cnt ))

                    update_data = {}
                    update_data_cond= {'report_id' : report_id }  
                    logging.info(detail_results)   
                    #todo: want to be better
                    if "total" in detail_results[0].keys():
                        sum_results = detail_results[0]['total']
                    else:
                        sum_results = None
                    update_data['sum_value'] = int(sum_results['value']) if sum_results is not None else 0 
                    update_data['sum_amount'] = int(sum_results['qty'])if sum_results is not None else 0 
                    update_data['sum_count'] = total_cnt if sum_results is not None else 0 
                    logging.info("[DONE] Inserted Sum ID={0},EdinetCode={1}, Date={2}, Val={3}, Amount={4}, Cnt={5}".format(report_id,submit_code,submit_date,update_data['sum_value'],update_data['sum_amount'] ,update_data['sum_count']  ))
                    self.db_obj.update_search_result_sum(update_data,update_data_cond)
                except Exception as e:
                    logging.warning("[Failure] Maybe more visible table.:{0}".format(e))


                







