# Food Rescue – Food Donation Platform

A beginner-friendly full-stack web application built with HTML, CSS, JavaScript, Python Flask and SQLite.

## Features
- Home page introducing the project
- Submit food donations
- View available food donations
- Submit a request for a listed donation
- Store donation and request information in an SQLite database
- About page and responsive layout

## Technologies
- Frontend: HTML, CSS (and browser-native JavaScript)
- Backend: Python Flask
- Database: SQLite
- Editor: Visual Studio Code

## Run locally

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open the VS Code terminal (`Terminal` → `New Terminal`).
4. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   ```

5. Activate it on Windows:

   ```powershell
   .venv\Scripts\Activate
   ```

6. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

7. Start the application:

   ```bash
   python app.py
   ```

8. Open `http://127.0.0.1:5000` in your browser.

The SQLite database file is created automatically the first time the app starts.

## Important note
This is an educational prototype. It does not verify food safety, donor identity, or collection arrangements. Do not use it to coordinate real food distribution without appropriate verification, privacy safeguards and food-safety procedures.

## GitHub
Create a new empty repository on GitHub, then follow the Git commands provided in the project setup instructions.
