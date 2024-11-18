import json
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import APIError
import sys

# Function to load data from JSON
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Function to update Google Sheet with JSON data
def update_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Tool Inventory").sheet1  # Or whatever you decide to name the google sheet

    existing_data = sheet.get_all_values()
    headers = existing_data[0] if existing_data else []

    for tool in data:
        found = False
        for i, row in enumerate(existing_data[1:], start=2):  # Start from the second row
            if row[headers.index("description")] == tool["description"]:
                found = True
                for key, value in tool.items():
                    if key in headers:
                        col_idx = headers.index(key) + 1
                        if row[headers.index(key)] != str(value):
                            try:
                                sheet.update_cell(i, col_idx, value)
                                time.sleep(0.5)
                            except APIError as e:
                                print(f"API error on row {i}, column {col_idx}: {e}")
                                time.sleep(60)
                break
        
        if not found:
            new_row = [tool.get(header, '') for header in headers]
            try:
                sheet.append_row(new_row)
                time.sleep(0.5)
            except APIError as e:
                print(f"API error while appending new row: {e}")
                time.sleep(60)

def main():
    if len(sys.argv) < 2:
        print("Error: No JSON file path provided.")
        sys.exit(1)
    
    file_path = sys.argv[1]  # Get the file path from command-line arguments
    sheet_data = load_json_data(file_path)
    update_sheet(sheet_data)

if __name__ == "__main__":
    main()
