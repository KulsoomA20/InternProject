from datetime import datetime
import csv 
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_chat_log(user_input, bot_response):
    return {
        "timestamp": get_timestamp(),
        "user": user_input,
        "bot": bot_response
    }

def save_chat_log_to_csv(log_entry, filename="chat_logs.csv"):
    fieldnames = ["timestamp", "user", "bot"]
    try:
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            # Write header only if the file is empty
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(log_entry)
    except Exception as e:
        print(f"Error saving chat log: {e}")
