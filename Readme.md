# UseEx - Business Document Intelligence Tool

UseEx is a Django-based web application powered by GenAI that extracts **use cases, modules, functionalities**, and other structured insights from **unstructured business documents** like requirement specs or product briefs.

## Features

- Upload a '.docx','.pdf' or '.txt' business document
- Automatically extracts:
  - Module names
  - Functionalities
  - Use Cases
  - Stakeholders
  - Risks
  - Expected Timeline or Priority
- Powered by state-of-the-art NLP techniques
- Displays extracted data in a clean Bootstrap-styled UI
- Option to download structured results as a Word document

## 🛠️ Tech Stack

- Django (Backend)
- HTML5 + Bootstrap 5 (Frontend)
- Python-Docx (for Word document handling)
- Google GenerativeAPI (gemini-1.5-flash-latest model)

# How to run

- clone the repository
    git clone https://github.com/AKpal-codes/GenAI-UseEx.git
- create and activate a python virtual environment
    python -m venv venv
    source venv/bin/activate  # or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt
- go into the repository and run the server
    cd GenAI-UseEx
    python manage.py runserver

# Author 
Ankur Pal
👨‍💻 Data Science @ NIT Jalandhar
📧 pal.ankur.mail@gmail.com