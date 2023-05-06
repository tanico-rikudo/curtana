import logging
import zipfile
import os
import pandas as pd

from bs4 import BeautifulSoup
from arelle import Cntlr
import requests
import json
import re
import yaml
import logging

from ..db.tables import BuyBackHeadline, BuyBackDetail
from ..db.client import DBclient

logging.basicConfig(filename=os.path.join(os.environ["HOME_PATH"], 'log/edinet.log'),
                    encoding='utf-8',
                    level=logging.INFO)


class Edinet:
    def __init__(self):
        self.config = {}
        self.api_base_path = ""
        self.tx_board_buyback_key = ""
        self.tx_shareholder_buyback_key = ""
        self.local_data_path = ""
        self.load_config()

        self.db = None
        self.init_db()

        pass

    def load_config(self, config_path=None):
        config_path = os.path.join(os.environ["HOME_PATH"], 'src/edinet/edinet.yaml') \
            if config_path is None else config_path
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

    def init_db(self):
        self.db = DBclient()

    def fetch_headlines(self, date):
        """
        Fetch headlines from EDINET
        Args:
            date (str): YYYY-MM-DD
        Returns:
            list: dict list
        """
        assert type(date) == str, "date must be string"
        logging.info(f"[Fetching...] Headline date={date}")
        headline_url = os.path.join(self.api_base_path, "documents.json")
        params = {"date": date, "type": 2}

        # proxies = {
        #     "http_proxy" : "http://username:password@proxy.example.com:8080/",
        #     "https_proxy" : "https://username:password@proxy.example.com:8080/"
        # }
        proxies = None
        res = requests.get(headline_url, params=params, proxies=proxies, timeout=(5, 120))
        headlines = json.loads(res.content)
        logging.info(f"[DONE] Fetched Headline date={date}")
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

    def save_headline(self, headlines):
        objects = []
        for headline in headlines:
            try:
                obj = BuyBackHeadline(
                    edinet_code=headline.get("edinetCode"),
                    doc_id=headline.get("docID"),
                    filer_name=headline.get("filerName"),
                    doc_type_code=headline.get("docTypeCode"),
                    submit_datetime=headline.get("submitDateTime"),
                    xbrl_flag=headline.get("xbrlFlag") == "1"
                )
                objects.append(obj)
            except Exception as e:
                logging.warning(f"[Failure] Save headline...:{e}", exc_info=True)

        if len(objects) > 0:
            self.db.insert_data(buyback_objects=objects)
        else:
            logging.warning("[Skip] Save headlines")

    def save_detail(self, details):
        objects = []
        for detail in details:
            try:
                date = str(int(detail.get("date_full")))

                obj = BuyBackDetail(
                    doc_id=detail.get("doc_id"),
                    acquition_type=detail.get("acquition_type"),
                    buy_qty=detail.get("qty"),
                    buy_notional=detail.get("value"),
                    buy_date=f"{date[:4]}-{date[4:6]}-{date[6:8]}",
                )
                objects.append(obj)
            except Exception as e:
                logging.warning(f"[Failure] Save detail...:{e}", exc_info=True)

        if len(objects) > 0:
            self.db.insert_data(buyback_objects=objects)
        else:
            logging.warning("[Skip] Save details")

    def fetch_xbrl(self, doc_id, folder_path=None):
        """

        Args:
            doc_id (str):

        Returns:
            str: download path
        """
        logging.info(f"[Fetching...] Download xbrl zip. doc_id={doc_id}")
        document_url = os.path.join(self.api_base_path, "documents", doc_id)
        params = {"type": "1"}
        res = requests.get(document_url, params=params, timeout=(5, 120))

        folder_path = self.local_data_path if folder_path is None else folder_path
        filepath = os.path.join(folder_path, f"{doc_id}.zip")
        if res.status_code == 200:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)
                logging.info(f"[DONE] Download xbrl zip. doc_id={doc_id}, path={filepath}")
        else:
            logging.error(f"[Failure] Invalid doc id or Fail to fetch data path. doc_id={doc_id}, {res}")
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
                    xbrl_file_dir = os.path.join(zip_file_path, info.filename)
                    file_datas.append(xbrl_file_dir)
                    logging.info(f"[DONE] Found xbrf file in {zip_file_path}")
        except zipfile.BadZipFile as e:
            logging.error(f"Fail to search xbrl directory: {zip_file_path}: {e}")

        logging.info(f"[DONE] Found {len(file_datas)} xbrf file in {zip_file_path}")

        return file_datas

    @staticmethod
    def parse_buyback_xbrf_form(xbrl_file_path):
        """
        parse xbrf files and parse html inside
        - For only buyback(220) docs
        Args:
            xbrl_file_path (str):

        Returns:
            dict: result
        """
        logging.info(f"[Loading...] Parse buybuck xbrf:{xbrl_file_path}")
        ctrl = Cntlr.Cntlr(logFileName='logToPrint')
        model_xbrl = ctrl.modelManager.load(xbrl_file_path)
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
                logging.info("[Parse...] AcquisitionsByResolutionOfShareholders ")
                shareholder_data["acquition_type"] = "shareholder"
                shareholder_data.update(Edinet.parse_buyback_table(html))
                logging.info("[DONE] Parse AcquisitionsByResolutionOfShareholders ")

            if fact.concept.qname.localName == "AcquisitionsByResolutionOfBoardOfDirectorsMeetingTextBlock":
                logging.info("[Parse...] AcquisitionsByResolutionOfBoardOfDirectors")
                board_data["acquition_type"] = "board"
                board_data.update(Edinet.parse_buyback_table(html))
                logging.info("[DONE] Parse AcquisitionsByResolutionOfBoardOfDirectors")

        logging.info(f"[DONE] Loaded Parse buybuck xbrf:{xbrl_file_path}")
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
        logging.info("[Parse...] Html ")

        try:
            table = soup.find_all("table")[1]  # only 1
        except Exception as e:
            logging.warning("Fail to fetch data. No table elements")
            return report_result

        try:
            data_row_flag = False
            for ele in table.find_all("tr"):
                if "報告月における取得自己株式" in ele.get_text():
                    data_row_flag = True
                if data_row_flag:
                    cols = [td.get_text().replace(",", "").replace(" ", "").replace("\n", "") for td in
                            ele.find_all("td")]
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
                    cols = [td.get_text().replace(",", "").replace(" ", "").replace("\n", "") for td in
                            ele.find_all("td")]
                    if re.match(bar_pattern, cols[2]) is None:
                        sum_qty = int(cols[2].replace(',', ''))
                        sum_value = int(cols[3].replace(',', ''))
                        if sum_qty is not None:
                            report_result['total'] = {'qty': sum_qty, 'value': sum_value}
                            logging.info("Sum : {0}".format(report_result['total']))
                        else:
                            logging.info("Sum: No data")
                    break

            logging.info("[DONE] Parse Html ")

        except Exception as e:
            logging.warning(f"[Failure] Parse HTML: {e}")

        return report_result

    def clean_buyback_fetch_data(self, fetched_raw_data):
        """
        Clean data by doc id
        Args:
            fetched_raw_data:

        Returns:

        """

        # get default values
        details = fetched_raw_data.get("details")
        doc_id = fetched_raw_data.get("doc_id")
        submit_datetime = fetched_raw_data.get("submit_datetime")
        submit_date = submit_datetime.split()[0].replace("-", "")
        daily_acquition_results = []
        total_acquition_results = []

        logging.info(f"[Cleaning...] doc_id={doc_id}")

        # cleaning
        for detail in details:
            figures = detail["figures"]
            for figure in figures.values():
                for daily_acquition_result in figure.get("daily"):
                    daily_acquition_result["acquition_type"] = figure.get("acquition_type")
                    daily_acquition_result["doc_id"] = doc_id
                    daily_acquition_result["submit_date"] = submit_date
                    daily_acquition_results.append(daily_acquition_result)
                total_acquition_result = figure.get("total")
                if total_acquition_result.get("qty") is not None:
                    total_acquition_result["acquition_type"] = figure.get("acquition_type")
                    total_acquition_result["doc_id"] = doc_id
                    total_acquition_result["submit_date"] = submit_date
                    total_acquition_results.append(total_acquition_result)

        df_daily = pd.DataFrame(daily_acquition_results)
        df_total = pd.DataFrame(total_acquition_results)

        # count check
        if df_daily.shape[0] == 0:
            if df_total.shape[0] == 0:
                logging.info(f"[PASS] doc_id={doc_id}. No dairy data")
            else:
                logging.error(f"[Failure] doc_id={doc_id}. Dairy and Total are not same. {df_total}")
            return []

        # add full date
        df_daily["date_full"] = df_daily["submit_date"].str[:4] + df_daily["date"]

        # if date is over year. fix it
        idxs = df_daily.loc[df_daily.date_full > df_daily.submit_date].index
        if len(idxs) > 0:
            logging.info("[Fixing...] Over year submission")
            logging.info(f"{df_daily.loc[idxs,:]}")

            for idx in idxs:
                srs = df_daily.loc[idx, :]
                df_daily.loc[idx, "date_full"] = srs["submit_date"][:4] + srs["date_full"][4:8]

        # if total qty is not same. invalid record
        if df_daily.qty.sum() != df_total.qty.sum():
            logging.error(
                f"[Failure]  doc_id={doc_id} Qty is not same. Daily:{df_daily.qty.sum()} != Total:{df_total.qty.sum()}")
            return []
        else:
            logging.error(f"[PASS] doc_id={doc_id} Qty is same. Total:{df_total.qty.sum()}")

        # Convert to record style
        daily_acquition_results = df_daily.to_dict(orient="records")

        logging.info(f"[DONE] Cleaning. doc_id={doc_id}")
        return daily_acquition_results
