
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime

from detector import detect_sensitive_data
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/dashboard")
def dashboard():
    return FileResponse("dashboard.html")

class PromptRequest(BaseModel):
    prompt: str


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "sentinel.db")


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            action TEXT,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()


create_database()


@app.get("/")
def home():
    return {
        "message": "Shadow AI Sentinel Backend is Running!"
    }


@app.post("/scan")
def scan_prompt(request: PromptRequest):

    prompt = request.prompt

    detection_result = detect_sensitive_data(prompt)

    emails = detection_result["emails"]
    phones = detection_result["phones"]
    names = detection_result["names"]
    locations = detection_result["locations"]
    organizations = detection_result["organizations"]

    risk_score = 0

    if emails:
        risk_score += 30

    if phones:
        risk_score += 30

    if names:
        risk_score += 20

    if locations:
        risk_score += 20

    if organizations:
        risk_score += 20

    if risk_score == 0:
        action = "ALLOW"
        risk_level = "LOW"
        final_prompt = prompt
    elif risk_score < 60:

        action = "REDACT"

        risk_level = "MEDIUM"

        final_prompt = prompt

        for email in emails:
            final_prompt = final_prompt.replace(email, "[REDACTED]")

        for phone in phones:
            final_prompt = final_prompt.replace(phone, "[REDACTED]")

        for name in names:
            final_prompt = final_prompt.replace(name, "[REDACTED]")

        for location in locations:
            final_prompt = final_prompt.replace(location, "[REDACTED]")

        for organization in organizations:
            final_prompt = final_prompt.replace(
                organization,
                "[REDACTED]"
            )
   

        for email in emails:
            final_prompt = final_prompt.replace(email, "[REDACTED]")

        for phone in phones:
            final_prompt = final_prompt.replace(phone, "[REDACTED]")

        for name in names:
            final_prompt = final_prompt.replace(name, "[REDACTED]")

        for location in locations:
            final_prompt = final_prompt.replace(location, "[REDACTED]")

        for organization in organizations:
            final_prompt = final_prompt.replace(
                organization,
                "[REDACTED]"
            )

    else:
        action = "BLOCK"
        risk_level = "HIGH"
        final_prompt = "[BLOCKED]"

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO scan_logs
        (prompt, risk_score, risk_level, action, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        prompt,
        risk_score,
        risk_level,
        action,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()

    return {
        "original_prompt": prompt,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "action": action,
        "emails_detected": emails,
        "phones_detected": phones,
        "names_detected": names,
        "locations_detected": locations,
        "organizations_detected": organizations,
        "final_prompt": final_prompt
    }


@app.get("/database-test")
def database_test():
    return {
        "database_path": DATABASE,
        "database_exists": os.path.exists(DATABASE)
    }


@app.get("/logs")
def get_logs():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, prompt, risk_score, risk_level, action, timestamp
        FROM scan_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    logs = []

    for row in rows:
        logs.append({
            "id": row[0],
            "prompt": row[1],
            "risk_score": row[2],
            "risk_level": row[3],
            "action": row[4],
            "timestamp": row[5]
        })

    return {
        "total_logs": len(logs),
        "logs": logs
    }


@app.get("/stats")
def get_stats():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_logs")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE risk_level = 'LOW'")
    low_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE risk_level = 'MEDIUM'")
    medium_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE risk_level = 'HIGH'")
    high_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE action = 'ALLOW'")
    allow_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE action = 'REDACT'")
    redact_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE action = 'BLOCK'")
    block_count = cursor.fetchone()[0]

    connection.close()

    return {
        "total_scans": total_scans,
        "risk_levels": {
            "low": low_count,
            "medium": medium_count,
            "high": high_count
        },
        "actions": {
            "allow": allow_count,
            "redact": redact_count,
            "block": block_count
        }
    }
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime

from detector import detect_sensitive_data
from fastapi.responses import FileResponse


app = FastAPI()


# =========================
# PROJECT PATH
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "sentinel.db")


# =========================
# DATABASE
# =========================

def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            action TEXT,
            timestamp TEXT
        )
    """)

    connection.commit()
    connection.close()


create_database()


# =========================
# DASHBOARD
# =========================

@app.get("/dashboard")
def dashboard():

    return FileResponse(
        os.path.join(BASE_DIR, "dashboard.html")
    )


# =========================
# REQUEST MODEL
# =========================

class PromptRequest(BaseModel):

    prompt: str


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "Shadow AI Sentinel Backend is Running!"
    }


# =========================
# SCAN PROMPT
# =========================

@app.post("/scan")
def scan_prompt(request: PromptRequest):

    prompt = request.prompt

    detection_result = detect_sensitive_data(prompt)

    emails = detection_result["emails"]
    phones = detection_result["phones"]
    names = detection_result["names"]
    locations = detection_result["locations"]
    organizations = detection_result["organizations"]

    risk_score = 0

    if emails:
        risk_score += 30

    if phones:
        risk_score += 30

    if names:
        risk_score += 20

    if locations:
        risk_score += 20

    if organizations:
        risk_score += 20


    # =========================
    # POLICY
    # =========================

    if risk_score == 0:

        action = "ALLOW"
        risk_level = "LOW"
        final_prompt = prompt


    elif risk_score < 60:

        action = "REDACT"
        risk_level = "MEDIUM"
        final_prompt = prompt

        for email in emails:
            final_prompt = final_prompt.replace(
                email,
                "[REDACTED]"
            )

        for phone in phones:
            final_prompt = final_prompt.replace(
                phone,
                "[REDACTED]"
            )

        for name in names:
            final_prompt = final_prompt.replace(
                name,
                "[REDACTED]"
            )

        for location in locations:
            final_prompt = final_prompt.replace(
                location,
                "[REDACTED]"
            )

        for organization in organizations:
            final_prompt = final_prompt.replace(
                organization,
                "[REDACTED]"
            )


    else:

        action = "BLOCK"
        risk_level = "HIGH"
        final_prompt = "[BLOCKED]"


    # =========================
    # SAVE LOG
    # =========================

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO scan_logs
        (prompt, risk_score, risk_level, action, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        prompt,
        risk_score,
        risk_level,
        action,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()


    # =========================
    # RESPONSE
    # =========================

    return {

        "original_prompt": prompt,

        "risk_score": risk_score,

        "risk_level": risk_level,

        "action": action,

        "emails_detected": emails,

        "phones_detected": phones,

        "names_detected": names,

        "locations_detected": locations,

        "organizations_detected": organizations,

        "final_prompt": final_prompt
    }


# =========================
# DATABASE TEST
# =========================

@app.get("/database-test")
def database_test():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()

    connection.close()

    return {
        "database": "Connected",
        "tables": tables
    }


# =========================
# GET LOGS
# =========================

@app.get("/logs")
def get_logs():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            prompt,
            risk_score,
            risk_level,
            action,
            timestamp
        FROM scan_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()


    logs = []

    for row in rows:

        logs.append({

            "id": row[0],

            "prompt": row[1],

            "risk_score": row[2],

            "risk_level": row[3],

            "action": row[4],

            "timestamp": row[5]
        })


    return {

        "total_logs": len(logs),

        "logs": logs
    }


# =========================
# DASHBOARD STATISTICS
# =========================

@app.get("/stats")
def get_stats():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM scan_logs"
    )

    total_scans = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM scan_logs WHERE risk_level = 'LOW'"
    )

    low_count = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM scan_logs WHERE risk_level = 'MEDIUM'"
    )

    medium_count = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM scan_logs WHERE risk_level = 'HIGH'"
    )

    high_count = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM scan_logs WHERE action = 'ALLOW'"
    )

    allow_count = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM scan_logs WHERE action = 'REDACT'"
    )

    redact_count = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM scan_logs WHERE action = 'BLOCK'"
    )

    block_count = cursor.fetchone()[0]


    connection.close()


    return {

        "total_scans": total_scans,

        "risk_levels": {

            "low": low_count,

            "medium": medium_count,

            "high": high_count
        },

        "actions": {

            "allow": allow_count,

            "redact": redact_count,

            "block": block_count
        }
    }


# =========================
# LLM TEST ENDPOINT
# =========================

@app.post("/llm-test")
def llm_test(request: PromptRequest):

    return {

        "message": "LLM integration endpoint is ready",

        "prompt_received": request.prompt,

        "status": "READY"
    }


# =========================
# SECURE LLM GATE
# =========================

@app.post("/secure-llm")
def secure_llm(request: PromptRequest):

    prompt = request.prompt

    detection_result = detect_sensitive_data(prompt)

    emails = detection_result["emails"]

    phones = detection_result["phones"]

    names = detection_result["names"]

    locations = detection_result["locations"]

    organizations = detection_result["organizations"]


    risk_score = 0


    if emails:

        risk_score += 30


    if phones:

        risk_score += 30


    if names:

        risk_score += 20


    if locations:

        risk_score += 20


    if organizations:

        risk_score += 20


    # =========================
    # BLOCK HIGH RISK
    # =========================

    if risk_score >= 60:

        return {

            "status": "BLOCKED",

            "risk_score": risk_score,

            "message":
            "Prompt blocked. Sensitive information detected."
        }


    # =========================
    # ALLOW SAFE PROMPT
    # =========================

    return {

        "status": "ALLOWED",

        "risk_score": risk_score,

        "message":
        "Prompt is safe to send to the LLM.",

        "prompt": prompt
    }