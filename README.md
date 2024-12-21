# Awaaz: Asynchronous News Aggregator  

**Awaaz** is a **Flask-based web application** that gathers and displays curated news articles using the **Google Open API**. The application focuses on delivering real-time updates based on the keyword **"Kashmir news"**, with user-friendly options to filter content by timeframe.  

## Project Structure  
```plaintext
├── app.py                # Main Flask application
├── templates/            # Jinja2 templates for the web interface
│   ├── index.html        # Homepage for filter selection
│   ├── results.html      # Displays fetched news
│   ├── error.html        # Error display page
├── static/               # Folder for static assets (CSS, images, JS)
├── encryption_key.key    # Encryption key for sensitive API data
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation

## Table of Contents  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Usage](#usage)  
- [How It Works](#how-it-works)  
- [Screenshots](#screenshots)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features  
- **Google Open API Integration:** Gathers real-time news updates with a focus on **"Kashmir news"**.  
- **Timeframe Filtering:** Enables filtering by recent, daily, weekly, or monthly news.  
- **Asynchronous Fetching:** Uses `aiohttp` and `asyncio` for fast and efficient data retrieval.  
- **Secure Data Handling:** Implements encryption using `cryptography.fernet` to protect sensitive URLs.  
- **Performance Optimization:** Uses Flask-Compress to reduce data transfer size and enhance speed.  
- **Custom Parsing:** Extracts and displays relevant information, such as headlines, summaries, timestamps, and links, using `BeautifulSoup`.  

---

## Tech Stack  
- **Backend:** Flask  
- **Frontend:** HTML5, CSS3, Jinja2 templates  
- **Libraries:**  
  - `aiohttp`  
  - `asyncio`  
  - `BeautifulSoup`  
  - `Flask-Compress`  
  - `cryptography`  

---
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/awaaz.git
cd awaaz
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Generate Encryption Key:
Run the following code to create an encryption key file:

python
Copy code
from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Save the key to a file
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)
Run the Application:

bash
Copy code
python app.py
Access the Application:
Open your browser and go to:

arduino
Copy code
http://127.0.0.1:55100
