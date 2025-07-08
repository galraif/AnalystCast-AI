from utils.sec.fetch_reports import fetch_sec_reports
from utils.playwrite.playwrite import deploy_reports

def run_pipeline(ticker: str, forms: list[str], after_date: str = None, before_date: str = None, limit = 1):
    reports = fetch_sec_reports(ticker, forms=forms, after_date=after_date, before_date=before_date, limit=limit)
    deploy_reports(reports)