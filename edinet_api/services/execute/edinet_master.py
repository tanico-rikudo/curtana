import os
import time
from services.src.edinet.edinet import Edinet
from edinet_logging import EdinetLogger
logger = EdinetLogger.get_loggger()

def get_detail(date=None):
    edinet_obj = Edinet()
    result = edinet_obj.get_details()
    return result

def get_headlines(date=None):
    edinet_obj = Edinet()
    result = edinet_obj.get_headlines()
    return result


def update_headline(date,doc_type):
    assert  doc_type in ["buyback","buyback_amend"], f"invalid doc_type: {doc_type}"
    if doc_type == "buyback":
        buyback_headlines = fetch_edinet_buyback_headlines(date=date)
        zip_file_paths = fetch_edinet_buyback_details(buyback_headlines=buyback_headlines)
        cleaned_details = process_edinet_buyback_details(zip_file_paths=zip_file_paths)
    else:
        raise NotImplemented("buy back amend")
        # buyback_headlines = fetch_edinet_buyback_headlines(date=date)
        # zip_file_paths = fetch_edinet_buyback_details(buyback_headlines=buyback_headlines)
        # cleaned_details = process_edinet_buyback_details(zip_file_paths=zip_file_paths)

    return cleaned_details

def fetch_edinet_buyback_headlines(date):
    """

    Args:
        date (int): ex. 20230404

    Returns:

    """
    date = str(date)
    date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    edinet_obj = Edinet()

    # get headline
    raw_headlines = edinet_obj.fetch_headlines(date)
    buyback_headlines = [headline for headline in raw_headlines.get("results") if
                         edinet_obj.filter_headline(headline, doc_type_code="220")]
    buyback_headlines = [ edinet_obj.clean_headline(headline=headline) for headline in buyback_headlines ]

    #save
    edinet_obj.save_headline(headlines=buyback_headlines)
    return buyback_headlines


def fetch_edinet_buyback_details(buyback_headlines):
    """

    Args:
        buyback_headlines (list): dict list

    Returns:

    """
    edinet_obj = Edinet()

    # get document set
    zip_file_paths = []
    for buyback_headline in buyback_headlines:
        try:
            time.sleep(1.0)
            doc_id = buyback_headline.get("docID")
            submit_datetime = buyback_headline.get("submitDateTime")
            submit_date = submit_datetime.split()[0].replace("-", "")
            zip_file_path = {"doc_id": doc_id,
                             "submit_datetime": submit_datetime,
                             "filepaths": edinet_obj.fetch_xbrl(doc_id=doc_id,
                                                                folder_path=os.path.join(edinet_obj.local_data_path,
                                                                                         submit_date))}
            zip_file_paths.append(zip_file_path)
        except Exception as e:
            logger.warning(f"[Skip] Failure fetch Edinet buyback detail:{e}")
    return zip_file_paths


def process_edinet_buyback_details(zip_file_paths):
    edinet_obj = Edinet()

    # get detail
    details = []
    for zip_file_path in zip_file_paths:

        try:

            # Fetch xbrf files
            xbrf_file_paths = edinet_obj.get_xbrl_directories(zip_file_path.get("filepaths"))

            # parse xbrf
            detail_figures = []
            for xbrf_file_path in xbrf_file_paths:
                detail_figure = {"figures": edinet_obj.parse_buyback_xbrf_form(xbrf_file_path),
                                 "file_path": xbrf_file_path}
                detail_figures.append(detail_figure)

            #  Add Optional root value.
            detail = {"doc_id": zip_file_path["doc_id"],
                      "submit_datetime": zip_file_path["submit_datetime"],
                      # "filer_name": zip_file_path["filer_name"],
                      "details": detail_figures}
            details.append(detail)


        except Exception as e:
            logger.warning(f"[Skip] Failure parsing Edinet buyback detail:{e}")

    cleaned_details = []
    logger.warning(f"[Running...] Detail deta cleaning")
    for detail in details:
        try:
            cleaned_details.extend(edinet_obj.clean_buyback_fetch_data(fetched_raw_data=detail))
        except Exception as e:
            logger.warning(f"[Skip] Failure Detail deta cleaning.: {e}", exc_info=True)
    logger.warning(f"[DONE] Detail deta cleaning.")

    edinet_obj.save_detail(details=cleaned_details)

    return cleaned_details


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
