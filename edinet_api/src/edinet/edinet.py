import logging
import zipfile
import os
from bs4 import BeautifulSoup
from arelle import Cntlr
import requests
import json
import re
import yaml
import logging
logging.basicConfig(filename='/workspace/src/edinet/edinet.log', encoding='utf-8')


class Edinet:
    def __init__(self):
        self.config = {}
        self.api_base_path = ""
        self.tx_board_buyback_key = ""
        self.tx_shareholder_buyback_key = ""
        self.local_data_path = ""
        self.load_config()
        pass

    def load_config(self, config_path=None):
        config_path = "/workspace/src/edinet/edinet.yaml" if config_path is None else config_path
        try:
            with open(config_path) as file:
                yaml_obj = yaml.safe_load(file)
            self.config = yaml_obj
            self.api_base_path = self.config["api"]["base_path"]
            self.tx_shareholder_buyback_key = self.config["taxonomy"]["shareholder_buyback_key"]
            self.tx_board_buyback_key = self.config["taxonomy"]["board_buyback_key"]
            self.local_data_path = self.config["local"]["data_folder_path"]
        except Exception as e:
            logging.warning(f'Exception occurred while loading YAML...{e}', exc_info=True)

    def fetch_headlines(self, date):
        """
        Fetch headlines from EDINET
        Args:
            date (str): YYYY-MM-DD
        Returns:
            list: dict list
        """

        assert type(date) == str, "date must be string"
        headline_url = os.path.join(self.api_base_path, "documents.json")
        params = {"date": date, "type": 2}

        # proxies = {
        #     "http_proxy" : "http://username:password@proxy.example.com:8080/",
        #     "https_proxy" : "https://username:password@proxy.example.com:8080/"
        # }
        proxies = None
        res = requests.get(headline_url, params=params, proxies=proxies)
        headlines = json.loads(res.content)
        return headlines

    @staticmethod
    def filter_headline(headline, doc_description=None, doc_type_code=None):
        """
        Filter headlines
        Args:
            headline (dict): API return dict object
            docDescription (str): provided key
            docTypeCode (str):

        Returns:
            bool:
        """
        if doc_description is not None:
            if doc_description not in headline.get("docDescription"):
                return False
        if doc_type_code is not None:
            if doc_type_code != headline.get("docTypeCode"):
                return False
        return True

    def fetch_xbrl(self, doc_id):
        """

        Args:
            doc_id (str):

        Returns:
            str: download path
        """
        document_url = os.path.join(self.api_base_path, "documents", doc_id)
        params = {"type": "1"}
        res = requests.get(document_url, params=params)
        filepath = os.path.join(self.local_data_path, f"{doc_id}.zip")
        if res.status_code == 200:
            with open(filepath, 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)
                    logging.info(f"[DONE] Download xbrl zip: {filepath}")
        else:
            logging.error(f"Invalid doc id or Fail to fetch data path:{res}")
        return filepath

    @staticmethod
    def get_xbrl_directories(zip_file_path):
        """
        Search xbrf files
        Args:
            zip_file_path (str):

        Returns:

        """

        file_datas = []
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_data:
                infos = zip_data.infolist()
                # in_xbrl_dir = os.path.join(zip_file_path,'XBRL','PublicDoc/')

                for info in infos:
                    root, ext = os.path.splitext(info.filename)

                if ext == ".xbrl" and "PublicDoc" in root:
                    xbrl_file_dir = os.path.join(zip_file_path,info.filename)
                    file_datas.append(xbrl_file_dir)
                    logging.info(f"[DONE] Founf xbrf file in {zip_file_path}")
        except zipfile.BadZipFile:
            logging.error(f"Fail to search xbrl directory: {zip_file_path}")

        return file_datas

    @staticmethod
    def parse_buyback_xbrf_form(xbrl_file):
        """
        parse xbrf files and parse html inside
        - For only buyback(220) docs
        Args:
            xbrl_file (str):

        Returns:
            dict: result
        """
        print(xbrl_file)
        ctrl = Cntlr.Cntlr(logFileName='logToPrint')
        model_xbrl = ctrl.modelManager.load(xbrl_file)
        data = {}
        for fact in model_xbrl.facts:
            if fact.concept.qname.localName == "DocumentTitleCoverPage":
                if fact.value != "自己株券買付状況報告書":
                    return {}

        shareholder_data = {}
        board_data = {}
        for fact in model_xbrl.facts:
            html = fact.value
            if fact.concept.qname.localName == "AcquisitionsByResolutionOfShareholdersMeetingTextBlock":
                shareholder_data["acquition_type"] = "shareholder"
                shareholder_data.update(Edinet.parse_buyback_table(html))
            if fact.concept.qname.localName == "AcquisitionsByResolutionOfBoardOfDirectorsMeetingTextBlock":
                board_data["acquition_type"] = "board"
                board_data.update(Edinet.parse_buyback_table(html))
        return {"shareholder_data": shareholder_data, "board_data": board_data}

    @staticmethod
    def parse_buyback_table(html):
        """
        Parse html in buyback html doc
        Args:
            html (str):

        Returns:
            dict: result
        """
        soup = BeautifulSoup(html)
        bar_pattern = '.*[-ー－―]+'
        void_dt_pattern = '[月日\s]'
        report_result = {'daily': [], 'total': {}}

        try:
            table = soup.find_all("table")[1]  # only 1
        except Exception as e:
            logging.warning("Fail to fetch data")
            return report_result
        data_row_flag = False
        for ele in table.find_all("tr"):
            if "報告月における取得自己株式" in ele.get_text():
                data_row_flag = True
            if data_row_flag:
                cols = [td.get_text().replace(",", "").replace(" ", "").replace("\n", "") for td in ele.find_all("td")]
                cols = [_str for _str in [re.sub(bar_pattern, "", _str) for _str in cols]]
                date_string = cols[1]
                if re.match(bar_pattern, date_string) is None and re.sub(void_dt_pattern, '', date_string) != '':
                    try:
                        month = str(int(date_string.split('月')[0])).zfill(2)
                        day = str(int(date_string.split('月')[1].split('日')[0])).zfill(2)
                        dt = month + day
                        qty = int(cols[2].replace(',', ''))
                        value = int(cols[3].replace(',', ''))
                        if qty is not None:
                            report_result['daily'].append({'date': dt, 'qty': qty, 'value': value})
                            logging.info("Data: {0}".format(report_result['daily'][-1]))
                        else:
                            logging.info("Data: No data")
                            pass
                    except Exception as e:
                        logging.warning("No Daily")
                        pass
            if "計" in ele.get_text():
                cols = [td.get_text().replace(",", "").replace(" ", "").replace("\n", "") for td in ele.find_all("td")]
                data_row_flag = True
                if re.match(bar_pattern, cols[2]) is None:
                    sum_qty = int(cols[2].replace(',', ''))
                    sum_value = int(cols[3].replace(',', ''))
                    if sum_qty is not None:
                        report_result['total'] = {'qty': sum_qty, 'value': sum_value}
                        logging.info("Sum : {0}".format(report_result['total']))
                    else:
                        logging.info("Sum: No data")
                break
        return report_result




