# Recommendation-and-negotiation
This is a Real-time AI sales intelligence and negotiation assistance. this project include an dynamic deal recommendation with LLM and GROQ API and AI insights also there is a post call summary process by using oauth2 authentication with google console and service, there is a negotiation coach to make the deal cancel by depending the benefits.
# Mutual Fund Assistant

## Overview
The Mutual Fund Assistant is a web-based application designed to provide users with detailed insights into mutual funds, aiding in decision-making. It features an intuitive interface for analyzing funds, entering negotiation details, and fetching post-call summaries. The application integrates Flask for the backend and JavaScript for dynamic functionality.

## Features
- **Text Input Analysis**: Allows users to input queries and receive detailed analysis.
- **Post-Call Summary**: Fetch summarized insights based on user interactions.
- **Negotiation Assistant**: Provides suggestions and tips for negotiation inputs.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## Technologies Used
- **Frontend**:
  - HTML5
  - CSS3 (Poppins font for styling)
  - JavaScript (external script file for dynamic functionality)
- **Backend**:
  - Flask (Python)
- **Database/Storage**:
  - Google Sheets integration for data storage and summary logs.
- **APIs**:
  - Custom APIs for processing text inputs and providing suggestions.

## Installation
Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/mutual-fund-assistant.git
   cd mutual-fund-assistant
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   flask run
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Project Structure
```
mutual-fund-assistant/
├── static/
│   ├── style.css        # CSS for styling
│   └── script.js        # JavaScript for interactivity
├── templates/
│   └── index.html       # Main HTML template
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Usage
1. Open the application in a web browser.
2. Navigate through the sections:
   - **Analysis**: Enter your query and get results.
   - **Negotiation**: Input details for negotiation assistance.
   - **Summary**: Fetch post-call summaries.
3. Interact with the responsive UI for a seamless experience.

## Screenshots
### Home Page

![Home Page](https://via.placeholder.com/800x400?text=Home+Page)
### Analysis Section
![Analysis Section](https://via.placeholder.com/800x400?text=Analysis+Section)

## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or feedback, please reach out at haswinraj.aiml@gmail.com.

---

Happy coding!

