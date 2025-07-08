from time import sleep, time
from typing import List
from playwright.sync_api import sync_playwright

def login_notebooklm():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://notebooklm.google.com/")
        input("🟢 Log in manually and press ENTER when done...")

        context.storage_state(path="state.json")
        print("✅ Login state saved to state.json")

        browser.close()

def deploy_reports(file_paths: List[str]) -> None:
    """
    Launches browser, opens Google NotebookLM, and uploads provided report files.

    Args:
        file_paths (List[str]): Full paths to the report .txt files to upload.
    """
    if not file_paths:
        raise ValueError("No file paths provided to upload.")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            storage_state="state.json"
        )
        page = context.new_page()

        page.goto("https://notebooklm.google.com/")
        page.wait_for_load_state()

        print("🧠 Opening NotebookLM...")

        # Start creating a notebook
        page.get_by_role("button", name="Create new notebook").click()
        sleep(1)

        page.get_by_role("button", name="choose file").click()
        sleep(1)

        # Upload file(s)
        file_input = page.locator('input[type="file"]')
        file_input.set_input_files(file_paths)
        print(f"📤 Uploaded {len(file_paths)} file(s)")

        # Close the upload dialog
        page.get_by_role("button", name="Close dialog").click()

        # Wait for "Generate" button to become enabled (up to 20 minutes)
        generate_button = page.get_by_role("button", name="Generate")
        start = time()
        timeout_secs = 1200

        print("⏳ Waiting for 'Generate' button to activate...")

        while not generate_button.is_enabled():
            if time() - start > timeout_secs:
                raise TimeoutError(f"'Generate' button not enabled after {timeout_secs} seconds.")
            sleep(1)

        generate_button.click()
        sleep(10) 
        print("✅ File uploaded and 'Generate' clicked successfully.")

