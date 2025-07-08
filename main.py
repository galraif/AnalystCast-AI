from core.pipeline import run_pipeline
from utils.playwrite.playwrite import login_notebooklm


if __name__ == "__main__":
    # Before running the pipeline, you need to login to NotebookLM and save the state.json file.
    # After login comment out the login_notebooklm() and uncomment the run_pipeline()
    # login_notebooklm()

    # options: ["10-K", "10-Q", "8-K", "4", "3", "5", "SC 13G", "SC 13D", "13F-HR", "13F-NT", "SD"]
    # run_pipeline("FROG", ["10-Q", "10-K"], after_date="2021-01-01", before_date="2022-01-01")
    run_pipeline("FROG", ["10-K", "10-Q"], limit=4)