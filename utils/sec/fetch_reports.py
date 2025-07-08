import os
import shutil
from sec_edgar_downloader import Downloader
from utils.config import REPORTS_DIR
from typing import List, Optional


def fetch_sec_reports(
    ticker: str,
    forms: Optional[List[str]] = None,
    after_date: Optional[str] = None,
    before_date: Optional[str] = None,
    limit: int = 1
) -> List[str]:
    """
    Downloads SEC filings for a given ticker and consolidates the results.

    Args:
        ticker (str): Company ticker symbol.
        forms (list[str], optional): List of form types (e.g., ["10-K", "8-K", "4"]) or ["all"].
        after_date (str, optional): Fetch filings after this date (YYYY-MM-DD).
        before_date (str, optional): Fetch filings before this date (YYYY-MM-DD).
        limit (int): Max number of filings per form if no date filters are used.

    Returns:
        List[str]: List of file paths to downloaded SEC reports.
    """
    print(f"\n🚀 Fetching SEC reports for: {ticker}")

    email = "analystcastai@mail.com"
    dl = Downloader(ticker, email, REPORTS_DIR)

    default_forms = [
        ("10-K", {}),
        ("10-Q", {}),
        ("8-K", {"include_amends": True}),
        ("4", {}),
        ("3", {}),
        ("5", {}),
        ("SC 13G", {}),
        ("SC 13D", {}),
        ("13F-HR", {}),
        ("13F-NT", {}),
        ("SD", {}),
    ]

    forms_to_download = (
        default_forms if not forms or forms == ["all"]
        else [(form, {}) for form in forms]
    )
    print(f"📋 Using forms: {[f[0] for f in forms_to_download]}")

    for form, extra_kwargs in forms_to_download:
        print(f"\n⬇️ Downloading {form} filings...")

        try:
            params = {}
            if after_date:
                params['after'] = after_date
                print(f"🕒 After: {after_date}")
            if before_date:
                params['before'] = before_date
                print(f"🕒 Before: {before_date}")
            if not (after_date or before_date):
                params['limit'] = limit
                print(f"🔢 Limit: {limit}")

            params.update(extra_kwargs)

            dl.get(form, ticker, **params)
            print(f"✅ Downloaded {form}")
        except Exception as e:
            print(f"❌ Failed to download {form}: {e}")

    print("\n🧹 Renaming files...")
    rename_sec_files(ticker)

    print("\n📦 Consolidating into 'all-reports'...")
    created_files = consolidate_reports(ticker)

    print("\n🎉 Done.")
    return created_files


def rename_sec_files(ticker: str) -> None:
    ticker_path = os.path.join(REPORTS_DIR, "sec-edgar-filings", ticker)
    if not os.path.exists(ticker_path):
        print(f"⚠️ No directory for ticker: {ticker}")
        return

    for form in os.listdir(ticker_path):
        form_path = os.path.join(ticker_path, form)
        if not os.path.isdir(form_path):
            continue

        for entry in os.listdir(form_path):
            entry_path = os.path.join(form_path, entry)
            if not os.path.isdir(entry_path):
                continue

            for filename in os.listdir(entry_path):
                full_path = os.path.join(entry_path, filename)
                if not os.path.isfile(full_path):
                    continue

                new_name = f"{form}-{entry}.txt"
                new_path = os.path.join(entry_path, new_name)

                try:
                    os.rename(full_path, new_path)
                    print(f"🔤 Renamed: {filename} → {new_name}")
                except Exception as e:
                    print(f"⚠️ Rename failed: {filename} in {entry_path}: {e}")


def consolidate_reports(ticker: str) -> List[str]:
    base_dir = os.path.join(REPORTS_DIR, "sec-edgar-filings", ticker)
    all_reports_dir = os.path.join(base_dir, "all-reports")
    os.makedirs(all_reports_dir, exist_ok=True)

    created_files = []

    for form in os.listdir(base_dir):
        form_path = os.path.join(base_dir, form)
        if not os.path.isdir(form_path) or form == "all-reports":
            continue

        for entry in os.listdir(form_path):
            entry_path = os.path.join(form_path, entry)
            if not os.path.isdir(entry_path):
                continue

            for filename in os.listdir(entry_path):
                if not filename.endswith(".txt"):
                    continue

                src = os.path.join(entry_path, filename)
                dst = os.path.join(all_reports_dir, filename)

                try:
                    shutil.copy2(src, dst)
                    created_files.append(dst)
                    print(f"📁 Copied: {filename}")
                except Exception as e:
                    print(f"⚠️ Failed to copy {filename}: {e}")

    return created_files
