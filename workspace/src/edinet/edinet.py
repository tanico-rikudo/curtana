
import logging
import zipfile
import os
from bs4 import BeautifulSoup
from arelle import Cntlr

class Edinet:
    def __init__():
        pass 
    
    
    def load_config():
        pass
        
        
    
    def fetch_headlines(date):
        
        
        headdline_url = f"{s}/documents.json"
        params = {"date": date, "type": 2}
        
        # proxies = {
        #     "http_proxy" : "http://username:password@proxy.example.com:8080/",
        #     "https_proxy" : "https://username:password@proxy.example.com:8080/"
        # }
        proxies=None
        res = requests.get(headdline_url, params=params ,proxies=proxies)
        headlines = json.loads(res.content)
        return headlines
        
    def filter_headline(headline, docDescription=None,docTypeCode=None):
        if docDescription is not None:
            if docDescription not in headline.get("docDescription"):
                return False
        if docTypeCode is not None:
            if docTypeCode != headline.get("docTypeCode"):
                return False
        return True

    def fetch_xbrl(doc_id):
        document_url = f"{API_BASE_URL}/documents/{doc_id}"
        params = {"type": "1"}
        res = requests.get(document_url, params=params)
        download_base_path = "/workspace/data"
        filepath = f"{download_base_path}/{doc_id}.zip"
        if res.status_code == 200:
            with open(filepath, 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)
        return filepath


    def get_xbrl_directories(zip_file):

        file_datas = []
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_data:
                infos = zip_data.infolist()
                in_xbrl_dir = zip_file + '/XBRL/PublicDoc/'

                for info in infos:
                    root, ext = os.path.splitext(info.filename)

                if ext == ".xbrl" and "PublicDoc" in root:
                    xbrl_file_dir = zip_file + "/" +info.filename
                    file_datas.append(xbrl_file_dir)
                    print("OK")
        except zipfile.BadZipFile:
            print(traceback.format_exc())
            
        return file_datas

    def parse_buyback_xbrf_form(xbrl_file):
        print(xbrl_file)
        ctrl = Cntlr.Cntlr(logFileName='logToPrint')
        model_xbrl = ctrl.modelManager.load(xbrl_file)
        data = {}
        for fact in model_xbrl.facts:
            if fact.concept.qname.localName == "DocumentTitleCoverPage":
                if(fact.value!="自己株券買付状況報告書"):
                    return {}
        
        shareholder_data = {}
        board_data = {}
        for fact in model_xbrl.facts:
            html =fact.value
            if (fact.concept.qname.localName=="AcquisitionsByResolutionOfShareholdersMeetingTextBlock"):
                shareholder_data["acquition_type"] = "shareholder"
                shareholder_data.update(parse_buyback_table(html))
            if (fact.concept.qname.localName=="AcquisitionsByResolutionOfBoardOfDirectorsMeetingTextBlock"):
                board_data["acquition_type"] = "board"
                board_data.update(parse_buyback_table(html))
        return [shareholder_data, board_data]
                
    def parse_buyback_table(html):
        soup = BeautifulSoup(html)
        bar_pattern = '.*[-ー－―]+'
        void_dt_pattern = '[月日\s]'
        # print(soup)
        report_result = {'daily':[],'total':{}}
        
        try:
            table = soup.find_all("table")[1] # only 1
        except Exception as e:
            print(e)
            return report_result
        tbody = table.find_all("tbody")[0] # only 1
        data_row_flag = False
        for ele in tbody.find_all("tr"):
            if "報告月における取得自己株式" in ele.get_text():
                data_row_flag = True
            if data_row_flag:
                cols = [td.get_text().replace(",","").replace(" ","").replace("\n","") for td in ele.find_all("td")]
                cols = [ _str  for _str in [re.sub(bar_pattern,"",_str) for _str in cols] ]
                date_string = cols[1]
                if  re.match(bar_pattern, date_string) is None and re.sub(void_dt_pattern, '', date_string) != '':
                    try:
                        month = str(int(date_string.split('月')[0])).zfill(2)
                        day = str(int(date_string.split('月')[1].split('日')[0])).zfill(2)
                        dt = month+day
                        qty = int(cols[2].replace(',', ''))
                        value = int(cols[3].replace(',', ''))
                        if qty is not None:
                            report_result['daily'].append({'date':dt,'qty':qty,'value':value})
                            print("Data: {0}".format(report_result['daily'][-1]))
                        else:
                            print("Data: No data")
                            pass
                    except Exception as e:
                        # logging.warning("No Daily")
                        print(e)
                        pass
            if "計" in ele.get_text():
                cols = [td.get_text().replace(",","").replace(" ","").replace("\n","") for td in ele.find_all("td")]
                data_row_flag = True
                if  re.match(bar_pattern, cols[2]) is None:
                    sum_qty = int(cols[2].replace(',', ''))
                    sum_value = int(cols[3].replace(',', ''))
                    if sum_qty is not None:
                        report_result['total'] = {'qty':sum_qty,'value':sum_value}
                        print("Sum : {0}".format(report_result['total']))
                    else:
                        print("Sum: No data")
                break
        return report_result