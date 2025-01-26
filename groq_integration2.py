import time
import signal
from groq import Groq
from google_sheets_util import write_to_sheet
import pandas as pd
import threading

# Global flag to handle script shutdown
shutdown_flag = False

# Groq API key
GROQ_API_KEY = "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"  # Replace with your actual API key
client = Groq(api_key=GROQ_API_KEY)

# Google Sheets configuration
SHEET_NAME = "Transcriptions and Responses"  # Replace with your Google Sheet name

# Dataset path
DATASET_PATH = "mutual_funds_dataset.csv"

# Load and preprocess the dataset
def load_and_preprocess_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    structured_text = ""
    for _, row in df.iterrows():
        structured_text += (
            f"Scheme Name: {row['scheme_name']}, Min SIP: {row['min_sip']}, "
            f"Expense Ratio: {row['expense_ratio']}, "
            f"Fund Size: {row['fund_size_cr']}, "
            f"Risk Level: {row['risk_level']} "
            f"Rating: {row['rating']}, Category: {row['category']}, "
            f" Return 1yr (%): {row['returns_1yr']}, "
            f"Return 3yr (%): {row['returns_3yr']}.\n"
        )
    return structured_text

# Preprocessed dataset
dataset_text = load_and_preprocess_dataset(DATASET_PATH)

# Function to process text with Groq API
def process_text_with_groq(text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a mutual fund analyst specializing in analyzing investment data. "
                        "Use the following dataset to answer user queries and provide insights:\n\n"
                        f"{dataset_text}\n\n"
                        "Always provide professional, concise, and data-driven responses. "
                        "Respond with sentiment and intent of the customer. "
                        "Also, provide a response that helps the salesperson convert the customer's intent into a positive one. "
                        "Negotiate with him well by advising better deals or improving the current adviced deal."
                    )
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=512,
        )
        response = chat_completion.choices[0].message.content
        return response
    except Exception as e:
        return f"Error with Groq API: {e}"

# Function to save summary responses only (not recognized text)
def save_summary(responses):
    try:
        with open("post_call_summary.txt", "w") as f:  # Overwrite file with only the summary
            f.write(responses + "\n")
        print("Summary successfully saved in post_call_summary.txt.")
    except Exception as e:
        print(f"Error saving summary: {e}")

# Function to write to Google Sheets (Transcriptions and Responses sheet)
def write_to_transcriptions_sheet(sheet_name, conversation_data):
    try:
        # Write transcription and response to the sheet
        write_to_sheet(sheet_name, conversation_data)  # Ensure data is passed as a list
        print(f"Conversation written to Google Sheet '{sheet_name}'. Data: {conversation_data}")
    except Exception as e:
        print(f"Error writing to Google Sheet '{sheet_name}': {e}")

# This Function is used  to generate the HTML file and append new responses
def generate_html_response(response):
    try:
        # Read the existing HTML file
        with open("assistant.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        # Locate the response container
        start_index = html_content.find('<div id="analysis" class="response-container">') + len('<div id="analysis" class="response-container">')
        if start_index == -1:
            raise ValueError("Response container not found in HTML content.")

        # Format the response as a list
        formatted_response = f"""
        <div class="response">
            <h2>Analysis Complete!</h2>
            <ul>
                {''.join(f'<li>{item.strip()}</li>' for item in response.split(','))}
            </ul>
        </div>
        """

        # Inject the response into the HTML
        end_index = html_content.find('</div>', start_index)
        updated_html = html_content[:start_index] + formatted_response + html_content[end_index:]

        # Write the updated HTML back to the file
        with open("assistant.html", "w", encoding="utf-8") as f:
            f.write(updated_html)

        print("Response successfully added to assistant.html.")

    except Exception as e:
        print(f"Error generating HTML response: {e}")

# Function to continuously monitor and process recognized text
def monitor_text():
    conversation_log = []  # To store the conversation history

    while not shutdown_flag:
        try:
            # Read text from the file
            with open("recognized_text.txt", "r") as f:
                text = f.read().strip()
        except FileNotFoundError:
            text = ""
        
        if text:
            # Process text with Groq
            response = process_text_with_groq(text)

            # Save the recognized text only (erase previous content)
            with open("recognized_text.txt", "w") as f:  # Always overwrite with new recognized text
                f.write(text)
            
            # Add to conversation log
            conversation_log.append({"user": text, "response": response})

            # Generate HTML response and append
            generate_html_response(response)

            # Write transcription and response to Google Sheet
            write_to_transcriptions_sheet(SHEET_NAME, [text, response])

        time.sleep(1)  # Check for new text every second

# Main function to initiate the monitoring process
def main():
    global shutdown_flag

    print("Starting the Groq integration with text file handling and Google Sheets...")
    
    # Start the text monitoring function in a separate thread
    text_monitor_thread = threading.Thread(target=monitor_text, daemon=True)
    text_monitor_thread.start()

    # Let the user type 'exit' to end the program
    while True:
        user_input = input("Type 'exit' to stop the script and generate summary: ")
        if user_input.lower() == "exit":
            print("Exiting and generating the summary...")
            shutdown_flag = True
            break
    
    # After user types 'exit', summarize and generate the final response
    conversation_history = ""  # Aggregate conversation text
    with open("recognized_text.txt", "r") as file:
        conversation_history = file.read().strip()

    if conversation_history:
        suggestions = process_text_with_groq(f"Conversation summary: {conversation_history}\nProvide suggestions and actions for future engagement with the customer.It should be like the assistant explaining everything in a way the mutual fund salesperson could understand what he has to do in next call?")
        
        # Save the final suggestion to post_call_summary.txt (overwrite with the summary)
        save_summary(f"Summary and Suggestions: {suggestions}")

        # Write this suggestion to Google Sheets
        write_to_transcriptions_sheet(SHEET_NAME, ["Summary and Suggestions", suggestions])

    print("Summary generated successfully.")

if __name__ == "__main__":
    main()
