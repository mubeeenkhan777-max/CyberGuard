# CyberGuard 🛡️
PROJECT VIDEO URL-> https://youtu.be/Cz-8NhT428w

**CyberGuard** is a Flask-based cybersecurity awareness and security analysis platform designed to help users learn cybersecurity, analyze suspicious URLs, evaluate password strength, and develop safer online habits.

## Features

* 🔎 **URL Security Checker**

  * Analyzes URLs for common warning signs.
  * Checks HTTPS usage, IP addresses, subdomains, URL length, suspicious characters, URL encoding, and suspicious keywords.
  * Provides a security score and risk level.
  * Saves URL scan history for logged-in users.

* 🔐 **Password Checker**

  * Evaluates password strength.
  * Provides guidance for creating stronger passwords.

* 🧠 **Cybersecurity Quiz**

  * Tests users' cybersecurity knowledge.
  * Calculates quiz scores.
  * Stores quiz attempts for each user.

* 📚 **Learning Center**

  * Phishing
  * Malware
  * Social Engineering
  * Two-Factor Authentication
  * Safe Browsing

* 🛡️ **Security Tips**

  * Provides practical cybersecurity recommendations.

* 📊 **Personal Dashboard**

  * Displays quiz attempts.
  * Shows best and average quiz scores.
  * Displays the number of URL scans.
  * Provides quick access to CyberGuard tools and learning resources.

* 📋 **Scan History**

  * Allows users to review their previous URL security analyses.

* 👤 **User Authentication**

  * User registration and login.
  * Session-based authentication.
  * Password hashing using Werkzeug security utilities.

## Technologies Used

* **Python**
* **Flask**
* **SQLite**
* **CS50 SQL**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Jinja2**
* **Git & GitHub**

## Project Structure

```text
CyberGuard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── password.js
│       ├── phishing.js
│       └── score.js
│
└── templates/
    ├── layout.html
    ├── index.html
    ├── dashboard.html
    ├── login.html
    ├── register.html
    ├── url_checker.html
    ├── password_checker.html
    ├── quiz.html
    ├── quiz_result.html
    ├── scan_history.html
    ├── score_history.html
    ├── learning.html
    ├── phishing.html
    ├── malware.html
    ├── social_engineering.html
    ├── two_factor.html
    ├── safe_browsing.html
    ├── security_tips.html
    └── 404.html
```

## How It Works

### 1. Create an Account

Users can register with a username, email address, and password.

Passwords are hashed before being stored in the database.

### 2. Login

Registered users can securely log in and access their personal dashboard.

### 3. Analyze a URL

Users can enter a URL into the URL Security Checker.

CyberGuard performs several basic checks and calculates a security score based on detected warning signs.

### 4. Learn Cybersecurity

Users can study common cybersecurity threats and protective techniques through the Learning Center.

### 5. Test Your Knowledge

Users can take the cybersecurity quiz and track their performance through their dashboard.

## Security

CyberGuard includes several basic security practices:

* Password hashing
* Session-based authentication
* Login-protected security tools
* Parameterized SQL queries
* Input validation
* URL validation
* Security-related HTTP response headers
* Database isolation between users
* Exclusion of the local database from Git using `.gitignore`

> **Important:** The URL Security Checker is an educational tool. A low-risk result does not guarantee that a URL is safe, and a high-risk result does not necessarily prove that a URL is malicious.

## Installation

Clone the repository:

```bash
git clone https://github.com/mubeeenkhan777-max/CyberGuard.git
cd CyberGuard
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Set a Flask secret key for a production environment:

```bash
set SECRET_KEY=your-secure-secret-key
```

On Linux/macOS:

```bash
export SECRET_KEY="your-secure-secret-key"
```

Run the application:

```bash
flask run
```

Then open the local Flask address shown in the terminal.

## Database

CyberGuard uses SQLite through the CS50 SQL library.

The local database file is intentionally excluded from the Git repository because it contains user-specific data.

When setting up the project on a new environment, the required database tables must be created before using the application.

## Future Improvements

Possible future improvements include:

* More advanced URL analysis
* Real-time threat intelligence integration
* Improved password security analysis
* Two-factor authentication
* Email verification
* Password reset functionality
* More cybersecurity quizzes
* User progress tracking
* Improved dashboard analytics
* Deployment to a production hosting platform

## Educational Purpose

CyberGuard was created as an educational cybersecurity project.

Its purpose is to help users understand common cyber threats and develop safer digital habits.

It is **not intended to replace professional cybersecurity tools or threat intelligence services**.

## Author

**Mubeen Khan**

CyberGuard was developed as a Flask/Python cybersecurity project while learning web development, Python, databases, authentication, and cybersecurity concepts.

## License

This project is available for educational and learning purposes.
