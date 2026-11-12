from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from pathlib import Path
from functools import wraps
from werkzeug.security import check_password_hash
from db import get_connection

from nlp_service import understand_command
from erp_commands import execute_command, confirm_attendance_update

import os
import tempfile

from flask import request, jsonify
from voice_service import transcribe_audio

# Your HTML, CSS, JavaScript and images are in the sibling "sp" folder
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "sp"

app = Flask(
    __name__,
    template_folder=str(FRONTEND_DIR),
    static_folder=str(FRONTEND_DIR),
    static_url_path="/sp"
)

FACULTY_USERNAME = "abhivarma"
FACULTY_PASSWORD = "abhi1234"

# Replace this with a long, random secret before deployment.
app.secret_key = "replace-with-a-long-random-secret"


# Protect pages that require faculty login
def faculty_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if "faculty_username" not in session:
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    return wrapper


# Login page
@app.route("/")
def home():
    if "faculty_username" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


# Authenticate faculty
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # Hardcoded check for administrative fallback (Optional)
    if username == FACULTY_USERNAME and password == FACULTY_PASSWORD:
        session["faculty_username"] = username
        return redirect(url_for("dashboard"))

    # Database logic now properly handles the general authentication flow
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT username, password FROM users WHERE username = %s",
            (username,)
        )
        faculty = cursor.fetchone()

        if faculty and check_password_hash(
            faculty["password"], password
        ):
            session.clear()
            session["faculty_username"] = faculty["username"]
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password. Please try again."
        )

    except Exception:
        app.logger.exception("Login/database error")
        return render_template(
            "login.html",
            error="Unable to log in right now. Please try again."
        )

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()



# Dashboard
@app.route("/dashboard")
@faculty_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session["faculty_username"]
    )


# Logout
@app.route("/logout", methods=["POST"])
@faculty_required
def logout():
    session.clear()
    return redirect(url_for("login"))


# Timetable
@app.route("/timetable")
@faculty_required
def timetable():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM timetable")
        records = cursor.fetchall()

        return render_template(
            "timetable.html",
            records=records
        )

    except Exception:
        app.logger.exception("Timetable retrieval error")
        return "Unable to load timetable. Check the Flask terminal.", 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()



# Academic Calendar
@app.route("/academic")
@faculty_required
def academic():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT `Date`, `Activity`
            FROM academic_calender
            ORDER BY `Date` ASC
        """

        cursor.execute(query)
        records = cursor.fetchall()
        print("ACADEMIC RECORDS:", records)
        print("TOTAL RECORDS:", len(records))

        return render_template("academic.html", records=records)

    except Exception as e:
        app.logger.exception("Academic calendar retrieval error")
        return f"Academic Calendar Error: {e}", 500

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()





# Attendance: retrieve students using selected filters
@faculty_required
@app.route("/attendence", methods=["GET"])
def attendence_page():
    year = request.args.get("year", "").strip()
    section = request.args.get("section", "").strip()
    attendance_date = request.args.get("date", "").strip()

    records = []

    if year and section and attendance_date:
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT *
                FROM attendence
                WHERE year = %s
                  AND Section = %s
                  AND Date = %s
                ORDER BY Enroll_No
            """

            cursor.execute(
                query, (year, section, attendance_date)
            )
            records = cursor.fetchall()

        except Exception as e:
            app.logger.exception("Unable to retrieve attendance")
            return f"Attendance error: {e}", 500

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    total = len(records)
    present = sum(
        1 for row in records if row["Status"] == "Present"
    )
    absent = sum(
        1 for row in records if row["Status"] == "Absent"
    )

    return render_template(
        "attendance.html",
        records=records,
        selected_year=year,
        selected_section=section,
        selected_date=attendance_date,
        total=total,
        present=present,
        absent=absent
    )


# Attendance: save all selected student statuses
@app.route("/attendence/save", methods=["POST"])
@faculty_required
def save_attendence():
    year = request.form.get("year", "").strip()
    section = request.form.get("section", "").strip()
    attendance_date = request.form.get("date", "").strip()

    try:
        count = int(request.form.get("student_count", "0"))
    except ValueError:
        return "Invalid student count.", 400

    if (
        not year or not section or not attendance_date
        or count < 1 or count > 500
    ):
        return "Invalid attendance details.", 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        for i in range(count):
            enrollment = request.form.get(
                f"enrollment_{i}", ""
            ).strip()
            status = request.form.get(f"status_{i}", "")

            if not enrollment or status not in ("Present", "Absent"):
                connection.rollback()
                return "Invalid student or attendance status.", 400

            query = """
                UPDATE attendence
                SET Status = %s
                WHERE Enroll_No  = %s
                  AND year = %s
                  AND Section = %s
                  AND Date = %s
            """
        

            cursor.execute(
                query,
                (status, enrollment, year, section, attendance_date)
            )

    

        connection.commit()

        return redirect(
            url_for(
                "attendence_page",
                year=year,
                section=section,
                date=attendance_date
            )
        )

    except Exception:
        if connection is not None:
            connection.rollback()
        app.logger.exception("Attendance save failed")
        return "Unable to save attendance. Check the Flask terminal.", 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


            
@app.route("/voice")
@faculty_required
def voice_page():
    return render_template("voice.html")




@app.route("/transcribe", methods=["POST"])
@faculty_required
def transcribe():

    if "audio" not in request.files:
        return jsonify({
            "success": False,
            "message": "No audio file received."
        }), 400

    audio_file = request.files["audio"]

    if audio_file.filename == "":
        return jsonify({
            "success": False,
            "message": "Empty audio file."
        }), 400

    temp_path = None

    try:
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(
            suffix=".webm",
            delete=False
        ) as temp_audio:
            audio_file.save(temp_audio.name)
            temp_path = temp_audio.name

        # 1. Convert audio into text
        whisper_result = transcribe_audio(temp_path)
        transcript = whisper_result["text"].strip()

        if not transcript:
            return jsonify({
                "success": False,
                "message": "No speech detected. Please try again."
            })

        # 2. Understand the command
        nlp_result = understand_command(transcript)
        print("VOICE NLP RESULT:", nlp_result)

        # 3. Execute the ERP operation
        erp_result = execute_command(nlp_result)

        # 4. Return the result to the frontend
        return jsonify({
            "success": erp_result.get("success", False),
            "transcript": transcript,
            "intent": nlp_result.get("intent"),
            "message": erp_result.get("message", ""),
            "data": erp_result.get("data"),
            "display_type": nlp_result.get("intent")
        })

    except Exception:
        app.logger.exception("Voice assistant error")

        return jsonify({
            "success": False,
            "message": "Unable to process voice command. Check Flask terminal."
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)




if __name__ == "__main__":
    print("MY UPDATED ERP APP IS RUNNING")
    app.run(debug=True)