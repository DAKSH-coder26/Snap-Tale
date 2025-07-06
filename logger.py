import csv

LOG_FILE = "ugc_log.csv"

def log_initial_request(order_id, name, phone):
    file_exists = False
    try:
        file_exists = open(LOG_FILE).readline().strip() != ""
    except:
        pass

    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Order ID", "Customer Name", "Phone", "Raw Review", "Drive Link"])
        writer.writerow([order_id, name, phone, "request sent", "review awaited"])
        print(f"[Log] 📩 Initial request logged for {order_id}")

def update_log_entry(order_id, raw_review, drive_link):
    rows = []
    found = False

    try:
        with open(LOG_FILE, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Order ID"] == order_id:
                    row["Raw Review"] = raw_review
                    row["Drive Link"] = drive_link
                    found = True
                rows.append(row)
    except FileNotFoundError:
        print(f"[Log] ❌ Log file not found.")
        return

    if not found:
        print(f"[Log] ❌ No entry to update for Order ID: {order_id}")
        return

    with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Order ID", "Customer Name", "Phone", "Raw Review", "Drive Link"])
        writer.writeheader()
        writer.writerows(rows)
        print(f"[Log] ✏️ Updated log entry for {order_id}")

def read_log():
    logs = []
    try:
        with open(LOG_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append(row)
    except FileNotFoundError:
        pass
    return logs
