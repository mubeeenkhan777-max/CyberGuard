import os
import re
import ipaddress
from functools import wraps
from urllib.parse import urlparse

from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)


# -------------------------
# Basic configuration
# -------------------------

app.secret_key = os.environ.get("SECRET_KEY", "cyberguard-dev-secret-key")

db = SQL("sqlite:///cyberguard.db")


# -------------------------
# Security headers
# -------------------------

@app.after_request
def security_headers(response):
    response.headers.update({
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    })
    return response


# -------------------------
# Login protection
# -------------------------

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")

        return view(*args, **kwargs)

    return wrapper


# -------------------------
# Home
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")


# -------------------------
# Register
# -------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not username or not email or not password:
            return "All fields are required."

        if len(username) > 50 or len(email) > 120:
            return "Input is too long."

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return "Invalid email address."

        if password != confirmation:
            return "Passwords do not match."

        if db.execute(
            "SELECT id FROM users WHERE username = ?",
            username
        ):
            return "Username already exists."

        if db.execute(
            "SELECT id FROM users WHERE email = ?",
            email
        ):
            return "Email already exists."

        db.execute(
            """
            INSERT INTO users (username, email, hash)
            VALUES (?, ?, ?)
            """,
            username,
            email,
            generate_password_hash(password)
        )

        return redirect("/login")

    return render_template("register.html")


# -------------------------
# Login
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return "Username and password are required."

        users = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        if len(users) != 1 or not check_password_hash(
            users[0]["hash"],
            password
        ):
            return "Invalid username or password."

        session.clear()

        session["user_id"] = users[0]["id"]
        session["username"] = users[0]["username"]

        return redirect("/dashboard")

    return render_template("login.html")


# -------------------------
# Logout
# -------------------------

@app.route("/logout")
@login_required
def logout():

    session.clear()

    return redirect("/")


# -------------------------
# Dashboard
# -------------------------

@app.route("/dashboard")
@login_required
def dashboard():

    user_id = session["user_id"]

    scores = db.execute(
        """
        SELECT score, total
        FROM quiz_scores
        WHERE user_id = ?
        """,
        user_id
    )

    percentages = [
        row["score"] / row["total"] * 100
        for row in scores
        if row["total"] and row["total"] > 0
    ]

    scans = db.execute(
        """
        SELECT id
        FROM url_scans
        WHERE user_id = ?
        """,
        user_id
    )

    average = (
        sum(percentages) / len(percentages)
        if percentages
        else 0
    )

    return render_template(
        "dashboard.html",
        username=session["username"],
        quiz_count=len(scores),
        scan_count=len(scans),
        best_score=round(max(percentages, default=0)),
        average_score=round(average)
    )


# -------------------------
# Learning pages
# -------------------------

@app.route("/password-checker")
@login_required
def password_checker():
    return render_template("password_checker.html")


@app.route("/learning")
@login_required
def learning():
    return render_template("learning.html")


@app.route("/learning/phishing")
@login_required
def phishing():
    return render_template("phishing.html")


@app.route("/learning/malware")
@login_required
def malware():
    return render_template("malware.html")


@app.route("/learning/social-engineering")
@login_required
def social_engineering():
    return render_template("social_engineering.html")


@app.route("/learning/two-factor")
@login_required
def two_factor():
    return render_template("two_factor.html")


@app.route("/learning/safe-browsing")
@login_required
def safe_browsing():
    return render_template("safe_browsing.html")


@app.route("/security-tips")
@login_required
def security_tips():
    return render_template("security_tips.html")


# -------------------------
# URL Security Checker
# -------------------------

@app.route("/url-checker", methods=["GET", "POST"])
@login_required
def url_checker():

    url = ""
    result = False
    risk_score = 100
    risk_level = "low"

    warnings = []
    risk_breakdown = []

    checks = {
        "https": "Not checked",
        "ip_address": "Not checked",
        "domain": "Not checked",
        "subdomains": "Not checked",
        "length": "Not checked",
        "suspicious_characters": "Not checked",
        "encoding": "Not checked",
        "keywords": "Not checked"
    }

    if request.method == "POST":

        url = request.form.get("url", "").strip()

        if not url:

            warnings.append(
                "Please enter a URL to analyze."
            )

            return render_template(
                "url_checker.html",
                url=url,
                result=False,
                risk_level=risk_level,
                risk_score=risk_score,
                risk_breakdown=[],
                warnings=warnings,
                checks=checks
            )

        if len(url) > 2048:

            warnings.append(
                "URL is too long."
            )

            return render_template(
                "url_checker.html",
                url="",
                result=False,
                risk_level="high",
                risk_score=0,
                risk_breakdown=[],
                warnings=warnings,
                checks=checks
            )

        if not re.match(
            r"^https?://",
            url,
            re.IGNORECASE
        ):
            url = "https://" + url

        parsed = urlparse(url)
        hostname = parsed.hostname or ""

        if (
            parsed.scheme not in ("http", "https")
            or not hostname
        ):

            warnings.append(
                "Invalid URL."
            )

            return render_template(
                "url_checker.html",
                url=url,
                result=False,
                risk_level="high",
                risk_score=0,
                risk_breakdown=[],
                warnings=warnings,
                checks=checks
            )

        result = True

        # HTTPS

        checks["https"] = (
            "Yes"
            if parsed.scheme == "https"
            else "No"
        )

        if parsed.scheme != "https":

            warnings.append(
                "The URL does not use HTTPS."
            )

        # IP address

        try:
            ipaddress.ip_address(hostname)
            is_ip = True

        except ValueError:
            is_ip = False

        checks["ip_address"] = (
            "Yes"
            if is_ip
            else "No"
        )

        if is_ip:

            warnings.append(
                "The URL uses an IP address instead of a normal domain."
            )

        # Domain

        checks["domain"] = hostname

        # Subdomains

        parts = hostname.split(".")

        many_subdomains = len(parts) > 3

        checks["subdomains"] = (
            "Many"
            if many_subdomains
            else "Normal"
        )

        if many_subdomains:

            warnings.append(
                "The URL contains multiple subdomains."
            )

        # Length

        url_length = len(url)

        checks["length"] = (
            f"{url_length} characters"
        )

        if url_length > 100:

            warnings.append(
                "The URL is unusually long."
            )

        # Suspicious characters

        suspicious = re.search(
            r"[@]",
            url
        )

        checks["suspicious_characters"] = (
            "Detected"
            if suspicious
            else "None detected"
        )

        if suspicious:

            warnings.append(
                "The URL contains a potentially suspicious character."
            )

        # Encoding

        encoded = "%" in url

        checks["encoding"] = (
            "Detected"
            if encoded
            else "None detected"
        )

        # Keywords

        keywords = (
            "login",
            "verify",
            "account",
            "password",
            "secure",
            "update",
            "confirm"
        )

        found = [
            word
            for word in keywords
            if word in url.lower()
        ]

        checks["keywords"] = (
            ", ".join(found)
            if found
            else "None detected"
        )

        if found:

            warnings.append(
                "The URL contains words commonly seen in phishing links."
            )

        # Risk score

        penalties = [

            (
                checks["https"] == "No",
                20,
                "No HTTPS"
            ),

            (
                is_ip,
                30,
                "IP address used instead of a domain"
            ),

            (
                many_subdomains,
                15,
                "Multiple subdomains detected"
            ),

            (
                url_length > 100,
                10,
                "Unusually long URL"
            ),

            (
                bool(suspicious),
                15,
                "Suspicious character detected"
            ),

            (
                encoded,
                10,
                "URL encoding detected"
            ),

            (
                bool(found),
                10,
                "Suspicious keywords detected"
            )
        ]

        for condition, points, message in penalties:

            if condition:

                risk_score -= points

                risk_breakdown.append(
                    f"{message}: -{points} points"
                )

        risk_score = max(
            0,
            min(100, risk_score)
        )

        if risk_score >= 80:

            risk_level = "low"

        elif risk_score >= 50:

            risk_level = "medium"

        else:

            risk_level = "high"

        # Save scan

        db.execute(
            """
            INSERT INTO url_scans
            (user_id, url, risk_score, risk_level)
            VALUES (?, ?, ?, ?)
            """,
            session["user_id"],
            url,
            risk_score,
            risk_level
        )

    return render_template(
        "url_checker.html",
        url=url,
        result=result,
        risk_level=risk_level,
        risk_score=risk_score,
        risk_breakdown=risk_breakdown,
        warnings=warnings,
        checks=checks
    )


# -------------------------
# Scan history
# -------------------------

@app.route("/scan-history")
@login_required
def scan_history():

    scans = db.execute(
        """
        SELECT url, risk_score, risk_level, created_at
        FROM url_scans
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        session["user_id"]
    )

    return render_template(
        "scan_history.html",
        scans=scans
    )


# -------------------------
# Quiz
# -------------------------

@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():

    if request.method == "POST":

        answers = {
            "q1": "b",
            "q2": "d",
            "q3": "a",
            "q4": "c",
            "q5": "a"
        }

        score = sum(
            request.form.get(question) == answer
            for question, answer in answers.items()
        )

        db.execute(
            """
            INSERT INTO quiz_scores
            (user_id, score, total)
            VALUES (?, ?, ?)
            """,
            session["user_id"],
            score,
            len(answers)
        )

        return render_template(
            "quiz_result.html",
            score=score,
            total=len(answers)
        )

    return render_template("quiz.html")


# -------------------------
# Score history
# -------------------------

@app.route("/score-history")
@login_required
def score_history():

    scores = db.execute(
        """
        SELECT score, total
        FROM quiz_scores
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        session["user_id"]
    )

    return render_template(
        "score_history.html",
        scores=scores
    )


# -------------------------
# Errors
# -------------------------

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(413)
def request_too_large(error):

    return "Request is too large.", 413


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

