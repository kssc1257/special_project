from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from pathlib import Path
from functools import wraps
from werkzeug.security import check_password_hash
from db import get_connection

# Your HTML, CSS, JavaScript and images are in the sibling "sp" folder
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "sp"

app = Flask(
    __name__,
    template_folder=str(FRONTEND_DIR),
    static_folder=str(FRONTEND_DIR),
    static_url_path="/sp"
)

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

    if not username or not password:
        return render_template(
            "login.html",
            error="Please enter both username and password."
        )

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
            error="Invalid username or password."
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
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM academic_calender")
        records = cursor.fetchall()

        return render_template(
            "academic.html",
            records=records
        )
    finally:
        cursor.close()
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

            if cursor.rowcount == 0:
                connection.rollback()
                return (
                    "A matching attendance record was not updated. "
                    "Check that every student has a record for this date.",
                    404
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

@app.route('/voice')
def voice_page():
    return render_template('voice.html') 

from flask import jsonify, request
# Ensure you are importing your audio processing logic
# from voice_service import transcribe_audio 

from flask import jsonify, request
import os
# Import the function from your project's voice service module
from voice_service import transcribe_audio 

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"success": False, "error": "No audio file provided"}), 400
        
    audio_file = request.files['audio']
    audio_path = "temp_recording.wav"
    
    try:
        # Save the live recorded audio file
        audio_file.save(audio_path)
        
        # ─── REAL TRANSCRIPTION ENGINE ───
        # This uses your faster-whisper logic to convert speech to text
                # ─── REAL TRANSCRIPTION ENGINE ───
        result = transcribe_audio(audio_path)
        
        # Check if result is the standard faster-whisper (segments, info) tuple
        if isinstance(result, tuple):
            segments, _ = result
            text = "".join([segment.text for segment in segments])
        # Check if result is a raw list/generator of segments
        elif hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            text = "".join([getattr(s, 'text', str(s)) for s in result])
        # Fallback if it's already a dictionary or string
        elif isinstance(result, dict):
            text = result.get('text', str(result))
        else:
            text = str(result)
 
        
        # Optional: Clean up the temporary audio file after transcription
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return jsonify({"success": True, "text": text})
        
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500



if __name__ == "__main__":
    print("MY UPDATED ERP APP IS RUNNING")
    app.run(debug=True)

