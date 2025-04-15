import os
import time
import json
import pandas as pd
from datetime import datetime
import subprocess

FEEDBACK_FILE = "logs/feedback.jsonl"
DATASET_FILE = "all_tickets_processed_improved_v3.csv"
THRESHOLD = 10

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        print(f"[{datetime.now()}] Feedback file not found.")
        return pd.DataFrame(columns=["Document", "Topic_group"])

    with open(FEEDBACK_FILE, "r") as f:
        lines = [json.loads(line.strip()) for line in f if line.strip()]

    if not lines:
        return pd.DataFrame(columns=["Document", "Topic_group"])

    df = pd.DataFrame(lines)
    if "text" not in df or "true_label" not in df:
        print(f"[{datetime.now()}] Invalid feedback schema.")
        return pd.DataFrame(columns=["Document", "Topic_group"])

    df = df.rename(columns={"text": "Document", "true_label": "Topic_group"})
    return df[["Document", "Topic_group"]]

def merge_and_save(feedback_df):
    df_orig = pd.read_csv(DATASET_FILE)
    df_merged = pd.concat([df_orig, feedback_df], ignore_index=True)
    df_merged.drop_duplicates(subset=["Document", "Topic_group"], inplace=True)
    df_merged.to_csv(DATASET_FILE, index=False)

    with open(FEEDBACK_FILE, "w") as f:
        f.write("")  # clear feedback

    print(f"[{datetime.now()}] ✅ Feedback merged and dataset updated.")

import subprocess

def trigger_retrain():
    print(f"[{datetime.now()}] 🚀 Retraining started...", flush=True)
    try:
        result = subprocess.run(
            ["python", "model_script.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print(result.stderr)
        print(f"[{datetime.now()}] ✅ Retraining complete.", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] ❌ Retraining failed:", flush=True)
        print(e.stdout, flush=True)
        print(e.stderr, flush=True)



def run_watcher():
    print(f"[{datetime.now()}] 👀 Retrainer started. Watching for feedback...")
    while True:
        feedback_df = load_feedback()
        count = len(feedback_df)

        if count >= THRESHOLD:
            print(f"[{datetime.now()}] 📊 Found {count} feedback entries.")
            merge_and_save(feedback_df)
            trigger_retrain()
        else:
            print(f"[{datetime.now()}] Waiting... ({count}/{THRESHOLD} feedbacks)")

        time.sleep(30)

if __name__ == "__main__":
    run_watcher()
