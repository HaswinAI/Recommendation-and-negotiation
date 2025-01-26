import gspread
from google.oauth2.service_account import Credentials

# Define the scope for Google Sheets and Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = "credentials.json"

# Authenticate and create a Google Sheets client
def authenticate_google_sheets():
    try:
        # Authenticate using the service account JSON file
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

# Function to write data to Google Sheets
def write_to_sheet(sheet_name, data):
    try:
        # Authenticate and get the client
        client = authenticate_google_sheets()
        if not client:
            raise Exception("Failed to authenticate with Google Sheets.")

        # Open the sheet and append data
        sheet = client.open(sheet_name).sheet1
        sheet.append_row(data)
        print("Data written to Google Sheet successfully.")
    except Exception as e:
        print(f"Error writing to Google Sheet: {e}")


# Function to write the summary to the sheet
def write_summary_to_sheet(sheet_name, row_index, summary):
    try:
        # Authenticate and get the client
        client = authenticate_google_sheets()
        if not client:
            raise Exception("Failed to authenticate with Google Sheets.")

        # Open the sheet
        sheet = client.open(sheet_name).sheet1

        # Update the summary in the correct row and column
        sheet.update_cell(row_index, 3, summary)  # Update column 3 (Summary) in the row

        print("Summary written to Google Sheet successfully.")
    except Exception as e:
        print(f"Error writing summary to Google Sheet: {e}")





# Function to fetch conversation data from Google Sheets
def fetch_conversation_data(sheet_name):
    try:
        # Authenticate and get the client
        client = authenticate_google_sheets()
        if not client:
            raise Exception("Failed to authenticate with Google Sheets.")

        # Open the sheet
        sheet = client.open(sheet_name).sheet1

        # Fetch all rows from the sheet
        rows = sheet.get_all_records()

        # Log the rows to see what data is fetched
        print("Fetched rows from sheet:", rows)

        if not rows:
            print("No conversation history found in the sheet.")
            return None

        # Example assuming a column 'User Query' exists in the sheet
        conversation_history = "\n".join([row['User Query'] for row in rows])  # Adjust column name
        return conversation_history
    except Exception as e:
        print(f"Error fetching conversation data: {e}")
        return None



def analyze_sentiment(user_input):
    # Use a model or API to analyze the sentiment of the input
    # This is a simplified example
    if "offer" in user_input:
        return "positive"
    else:
        return "neutral"

def generate_negotiation_suggestion(user_input, sentiment):
    if sentiment == "positive":
        return f"That's a great offer! You could add more value by offering a payment plan or discount."
    elif sentiment == "neutral":
        return f"Consider framing your offer in a more compelling way by highlighting the benefits."
    else:
        return f"It seems like there's room for improvement in the tone. Try focusing on the mutual benefits of the deal."







# Example usage
if __name__ == "__main__":
    # Replace with your actual Google Sheet name
    sheet_name = "Your Google Sheet Name"
    data = ["Sample Transcription", "Sample Response"]
    write_to_sheet(sheet_name, data)
