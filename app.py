from flask import Flask, request, render_template, jsonify
import threading
import os
from groq_integration2 import process_text_with_groq, save_summary
from google_sheets_util import write_to_sheet, fetch_conversation_data, write_summary_to_sheet, analyze_sentiment, generate_negotiation_suggestion 

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# API route to process transcription and generate Groq response
@app.route('/process', methods=['POST'])
def process_text():
    user_text = request.json.get('text')
    if not user_text:
        return jsonify({"error": "No text provided."}), 400

    # Process the text with Groq
    try:
        groq_response = process_text_with_groq(user_text)

        # Save to Google Sheets
        sheet_name = "Transcriptions and Responses"
        write_to_sheet(sheet_name, [user_text, groq_response])

        return jsonify({"response": groq_response})
    except Exception as e:
        print(f"Error during processing: {e}")
        return jsonify({"error": "Error processing the text. Please try again."}), 500


# Route for generating post-call summary
@app.route('/summary', methods=['POST'])
def generate_summary():
    conversation_history = request.json.get('conversation')
    if not conversation_history:
        return jsonify({"error": "No conversation history provided."}), 400

    # Generate summary using Groq
    summary = process_text_with_groq(f"Conversation summary: {conversation_history}")
    
    if summary:
        # Save summary to Google Sheets
        sheet_name = "Transcriptions and Responses"  # Your sheet name
        data = [conversation_history, summary]  # Add summary to the same row
        write_to_sheet(sheet_name, data)  # Save data to the sheet

    return jsonify({"summary": summary})

# Route to fetch conversation history from Google Sheets and generate summary
@app.route('/fetch_summary', methods=['GET'])
def fetch_summary():
    # Fetch conversation history from the sheet
    sheet_name = "Transcriptions and Responses"
    conversation_history = fetch_conversation_data(sheet_name)

    if not conversation_history:
        return jsonify({"error": "No conversation history found."}), 400

    # Generate summary using Groq
    summary = process_text_with_groq(f"Conversation summary: {conversation_history}")

    # Optionally, save the summary
    save_summary(summary)

    return jsonify({"summary": summary})


@app.route('/negotiate', methods=['POST'])
def negotiate():
    user_input = request.json.get('text')
    if not user_input:
        return jsonify({"error": "No negotiation input provided."}), 400
    
    # Example negotiation logic: Sentiment analysis and counter-offer suggestion
    sentiment = analyze_sentiment(user_input)  # You can use Groq or another model for sentiment analysis
    negotiation_suggestion = generate_negotiation_suggestion(user_input, sentiment)
    
    return jsonify({"suggestion": negotiation_suggestion})





if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
