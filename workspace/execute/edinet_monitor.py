

def fetch_edinet_buyback(date):

    date = "2023-04-04"
    res = fetch_headlines(date)
    buyback_headlines = [ headline for headline in headlines.get("results") if  filter_headline(headline, docTypeCode="220")]
    filepaths = []
    for buyback_headline in buyback_headlines[:3]:
        doc_id = buyback_headline.get("docID")
        filepaths.append(fetch_xbrl(doc_id))

    data = []
    for filepath in filepaths:
        xbrf_files = get_xbrl_directories(filepath)
        for xbrf_file in xbrf_files:
            print(xbrf_files)
            data.append(parse_buyback_xbrf_form(xbrf_file))
        
def fetch_edinet_amend_buyback(date):

    date = "2023-04-04"
    res = fetch_headlines(date)
    buyback_headlines = [ headline for headline in headlines.get("results") if  filter_headline(headline, docTypeCode="230")]
    filepaths = []
    for buyback_headline in buyback_headlines[:3]:
        doc_id = buyback_headline.get("docID")
        filepaths.append(fetch_xbrl(doc_id))

    data = []
    for filepath in filepaths:
        xbrf_files = get_xbrl_directories(filepath)
        for xbrf_file in xbrf_files:
            print(xbrf_files)
            data.append(parse_buyback_xbrf_form(xbrf_file))
        