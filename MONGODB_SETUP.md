# MongoDB Setup Guide

## Option 1: Local MongoDB

### macOS (with Homebrew)
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

Verify installation:
```bash
mongosh
> exit
```

### Linux (Ubuntu)
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
```

### Windows
Download and install from: https://www.mongodb.com/try/download/community

---

## Option 2: MongoDB Atlas (Cloud - Recommended)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account and log in
3. Create a new project
4. Click "Create a Deployment" and select **M0 (Free Tier)**
5. Choose cloud provider and region
6. Create a database user (save username and password)
7. Add your IP to the IP Whitelist (or allow all: `0.0.0.0/0`)
8. Click "Connect" and copy the connection string
9. Replace `<username>`, `<password>`, and `<cluster>` with your actual values

---

## Setup in Your Project

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create `.env` file
```bash
cp .env.example .env
```

Edit `.env` and add your MongoDB connection URI:
```
MONGODB_URI=mongodb://localhost:27017/facebook_demo
```

Or for MongoDB Atlas:
```
MONGODB_URI=mongodb+srv://username:password@cluster0.mongodb.net/facebook_demo?retryWrites=true&w=majority
```

### 3. Run the app
```bash
python3 app.py
```

---

## Verify MongoDB Connection

In a Python shell:
```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.facebook_demo
print(db.logins.find_one())  # Should return None if empty, or a document
```

---

## View Data in MongoDB

### Using MongoDB Compass (GUI)
Download: https://www.mongodb.com/products/compass
- Paste your connection URI
- Navigate to `facebook_demo` database → `logins` collection

### Using mongosh (CLI)
```bash
mongosh
> use facebook_demo
> db.logins.find()
```
