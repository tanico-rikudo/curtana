from ..src.edinet.edinet import *
from ..src.db.client import *

def save(data):
    pass

def fetch_edinet_buyback(date):
    date = "2023-04-04"
    edinet_obj = Edinet()
    headlines = edinet_obj.fetch_headlines(date)
    buyback_headlines = [headline for headline in headlines.get("results") if
                         edinet_obj.filter_headline(headline, doc_type_code="220")]
    zip_file_paths = []
    for buyback_headline in buyback_headlines:
        doc_id = buyback_headline.get("docID")
        zip_file_paths.append(edinet_obj.fetch_xbrl(doc_id))

    data = []
    for zip_file_path in zip_file_paths:
        xbrf_files = edinet_obj.get_xbrl_directories(zip_file_path)
        for xbrf_file in xbrf_files:
            data.append(edinet_obj.parse_buyback_xbrf_form(xbrf_file))
    return data


def fetch_edinet_amend_buyback(date):
    date = "2023-04-04"
    edinet_obj = Edinet()
    headlines = edinet_obj.fetch_headlines(date)
    buyback_headlines = [headline for headline in headlines.get("results") if
                         edinet_obj.filter_headline(headline, doc_type_code="230")]
    zip_file_paths = []
    for buyback_headline in buyback_headlines:
        doc_id = buyback_headline.get("docID")
        zip_file_paths.append(edinet_obj.fetch_xbrl(doc_id))

    data = []
    for zip_file_path in zip_file_paths:
        xbrf_files = edinet_obj.get_xbrl_directories(zip_file_path)
        for xbrf_file in xbrf_files:
            data.append(edinet_obj.parse_buyback_xbrf_form(xbrf_file))
    return data
