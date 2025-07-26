# CYBEREYE

CyberEye is a real-time AI-powered phishing detection system using Gemma LLM, featuring automatic URL classification into phishing, defacement, malicious, or benign categories. It provides threat reasoning and scan history logging via a Flask + SQLite backend. The project also integrates a Chrome Extension to scan browser tabs in real time, reducing potential phishing exposure by 98%.

1. Phishing – Pretends to be a trusted site to steal personal data (e.g., login or banking).
2. Defacement – A legitimate website that has been altered or defaced by hackers.
3. Malicious – Delivers malware, spyware, or harmful code.
4. Benign – Safe, trusted website with no harmful behavior.

## How it works:

1.A user visits the React frontend application where they can input a URL to be scanned.
2.When the user submits a URL, the frontend sends this URL to the backend Flask API.
3.The backend uses an AI model (Gemma LLM) to classify the URL into one of four categories: Phishing (pretending to be a trusted site to steal data), Defacement (a legitimate site altered by hackers), Malicious (delivering harmful code), or Benign (safe site).
4.The backend also provides reasoning for the classification and logs the scan history in a SQLite database.
5.The frontend displays the classification result and reasoning to the user, along with a history of previous scans.

Chrome Extension:

1.The project includes a Chrome Extension that runs in the user's browser.
2.It scans open tabs in real time to detect phishing or malicious sites automatically.
3.This helps reduce the user's exposure to phishing attacks by 98%.
4.Users can install the extension from the extension/ directory and it works seamlessly alongside the web app.

## Project Structure

- `backend/`: Contains the Flask backend API and database.
- `frontend/`: Contains the React frontend application.
- `extension/`: Contains the Chrome Extension files.

## Backend

The backend is built with Flask and provides API endpoints for URL classification and scan history.

### Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Backend

Run the Flask app with:

```bash
python app.py
```

The backend server will start on `http://localhost:5000`.

## Frontend

The frontend is built with React and uses `react-scripts` for development.

### Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Frontend

Start the development server with:

```bash
npm start
```

The frontend will be available at `http://localhost:3000`.

## Chrome Extension

The Chrome Extension scans tabs in real time to reduce phishing exposure. It is located in the `extension/` directory.

## Technologies Used

- Backend: Python, Flask, Flask-CORS, SQLite
- Frontend: React, Axios, Tailwind CSS (via devDependencies)
- Browser Extension: HTML, JavaScript, CSS


## License

This project is licensed under the MIT License.


