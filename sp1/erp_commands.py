
from db import get_connection


# Actual timetable columns from your MySQL table.
TIME_SLOTS = {
    "9:30 - 10:20": "9:30 - 10:20",
    "10:20 - 11:10": "10:20 - 11:10",
    "11:25 - 12:15": "11:25 - 12:15",
    "12:15 - 1:05": "12:15 - 1:05",
    "1:45 - 2:35": "1:45 - 2:35",
    "2:35 - 3:20": "2:35 - 3:20",
    "3:20 - 4:15": "3:20 - 4:15"
}


# --------------------------------------------------
# 1. VIEW ATTENDANCE
# --------------------------------------------------

def view_attendance(entities):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        conditions = []
        values = []

        section = entities.get("section")
        student = entities.get("student")
        date = entities.get("date")

        if section:
            conditions.append("Section = %s")
            values.append(section)

        if student:
            conditions.append("LOWER(Name) = LOWER(%s)")
            values.append(student)

        if date:
            conditions.append("Date = %s")
            values.append(date)

        query = """
            SELECT Enroll_No, Name, Course,
                   Section, Session, Date, Status, year
            FROM attendence
        """

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY Date DESC, Session"

        cursor.execute(query, tuple(values))
        records = cursor.fetchall()

        if not records:
            return {
                "success": False,
                "message": "No matching attendance records found."
            }

        return {
            "success": True,
            "message": "Attendance records retrieved successfully.",
            "data": records
        }

    except Exception as e:
        print("Attendance Error:", e)

        return {
            "success": False,
            "message": "Unable to retrieve attendance."
        }

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------
# 2. VIEW ACADEMIC CALENDAR
# --------------------------------------------------

def view_academic_calendar(entities):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        requested_date = entities.get("date")
        upcoming_holiday = entities.get("upcoming_holiday")

        if upcoming_holiday:

            query = """
                SELECT Activity, Date
                FROM academic_calender
                WHERE LOWER(Activity) LIKE '%holiday%'
                  AND Date >= CURDATE()
                ORDER BY Date ASC
                LIMIT 1
            """

            cursor.execute(query)

        elif requested_date:

            query = """
                SELECT Activity, Date
                FROM academic_calender
                WHERE Date = %s
                ORDER BY Date ASC
            """

            cursor.execute(query, (requested_date,))

        else:

            query = """
                SELECT Activity, Date
                FROM academic_calender
                ORDER BY Date ASC
            """

            cursor.execute(query)

        records = cursor.fetchall()

        if not records:
            return {
                "success": False,
                "message": "No matching academic calendar activity found."
            }

        return {
            "success": True,
            "message": "Academic calendar retrieved successfully.",
            "data": records
        }

    except Exception as e:
        print("Academic Calendar Error:", e)

        return {
            "success": False,
            "message": "Unable to retrieve academic calendar."
        }

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------
# 3. VIEW TIMETABLE
# --------------------------------------------------



def view_timetable(entities):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        day = entities.get("day")
        requested_slot = entities.get("time_slot")
        session = entities.get("session")

        session_slots = {
            "1": "9:30 - 10:20",
            "2": "10:20 - 11:10",
            "3": "11:25 - 12:15",
            "4": "12:15 - 1:05",
            "5": "1:45 - 2:35",
            "6": "2:35 - 3:20",
            "7": "3:20 - 4:15"
        }

        # Convert session number into its time slot
        if session:
            requested_slot = session_slots.get(str(session))

            if not requested_slot:
                return {
                    "success": False,
                    "message": "Invalid session. Please specify a session from 1 to 7."
                }

        # General timetable: show all days and all periods
        if not day and not requested_slot:
            cursor.execute("SELECT * FROM timetable")

        # Exact period requires a day
        elif requested_slot:
            if not day:
                return {
                    "success": False,
                    "message": "Please specify the day for the requested timetable."
                }

            slot = TIME_SLOTS.get(requested_slot)

            if not slot:
                return {
                    "success": False,
                    "message": "That time slot is not available."
                }

            query = f"""
                SELECT Day, `{slot}` AS Time_Slot_Details
                FROM timetable
                WHERE LOWER(Day) = LOWER(%s)
            """
            cursor.execute(query, (day,))

        # Specific day: show all periods for that day
        else:
            query = """
                SELECT *
                FROM timetable
                WHERE LOWER(Day) = LOWER(%s)
            """
            cursor.execute(query, (day,))

        records = cursor.fetchall()

        if not records:
            return {
                "success": False,
                "message": "No matching timetable records found."
            }

        return {
            "success": True,
            "message": "Timetable retrieved successfully.",
            "data": records
        }

    except Exception as e:
        print("Timetable Error:", e)
        return {
            "success": False,
            "message": "Unable to retrieve timetable."
        }

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------
# 4. PREPARE ATTENDANCE UPDATE
# --------------------------------------------------

def prepare_attendance_update(entities):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        student = entities.get("student")
        section = entities.get("section")
        date = entities.get("date")
        session = entities.get("session")
        status = entities.get("status")

        if not all([student, section, date, session, status]):
            return {
                "success": False,
                "message": (
                    "Student, section, date, session and status "
                    "are required."
                )
            }

        if status not in ["Present", "Absent"]:
            return {
                "success": False,
                "message": "Invalid attendance status."
            }

        query = """
            SELECT Enroll_No, Name, Course, Section,
                   Session, Date, Status
            FROM attendence
            WHERE LOWER(Name) = LOWER(%s)
              AND Section = %s
              AND Date = %s
              AND Session = %s
        """

        cursor.execute(
            query,
            (student, section, date, str(session))
        )

        records = cursor.fetchall()

        if len(records) == 0:
            return {
                "success": False,
                "message": "No matching attendance record found."
            }

        if len(records) > 1:
            return {
                "success": False,
                "message": (
                    "Multiple records found. Please identify "
                    "the student using enrollment number."
                )
            }

        record = records[0]

        if record["Status"] == status:
            return {
                "success": False,
                "message": "Attendance already has this status."
            }

        return {
            "success": True,
            "message": "Record found. Confirmation required.",
            "data": {
                "enrollment_number": record["Enroll_No"],
                "student": record["Name"],
                "section": record["Section"],
                "date": str(record["Date"]),
                "session": record["Session"],
                "old_status": record["Status"],
                "new_status": status
            }
        }

    except Exception as e:
        print("Attendance Preparation Error:", e)

        return {
            "success": False,
            "message": "Unable to prepare attendance update."
        }

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------
# 5. CONFIRM ATTENDANCE UPDATE
# --------------------------------------------------

def confirm_attendance_update(data):

    connection = None
    cursor = None

    try:
        enrollment_number = data.get("enrollment_number")
        section = data.get("section")
        date = data.get("date")
        session = data.get("session")
        new_status = data.get("new_status")
        old_status = data.get("old_status")

        if not all([
            enrollment_number, section, date, session
        ]):
            return {
                "success": False,
                "message": "Missing attendance details."
            }

        if new_status not in ["Present", "Absent"]:
            return {
                "success": False,
                "message": "Invalid attendance status."
            }

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE attendence
            SET Status = %s
            WHERE Enroll_No = %s
              AND Section = %s
              AND Date = %s
              AND Session = %s
              AND Status <=> %s
        """

        cursor.execute(
            query,
            (
                new_status,
                enrollment_number,
                section,
                date,
                str(session),
                old_status
            )
        )

        if cursor.rowcount != 1:
            connection.rollback()

            return {
                "success": False,
                "message": "Attendance was not updated."
            }

        connection.commit()

        return {
            "success": True,
            "message": "Attendance updated successfully!"
        }

    except Exception as e:

        if connection:
            connection.rollback()

        print("Attendance Update Error:", e)

        return {
            "success": False,
            "message": "Unable to update attendance."
        }

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# --------------------------------------------------
# 6. COMMAND DISPATCHER
# --------------------------------------------------


def execute_command(result):

    intent = result.get("intent")
    entities = result.get("entities", {})

    if intent == "VIEW_ATTENDANCE":
        return view_attendance(entities)

    elif intent == "VIEW_ACADEMIC_CALENDAR":
        return view_academic_calendar(entities)

    elif intent == "VIEW_TIMETABLE":
        return view_timetable(entities)

    elif intent == "MARK_ATTENDANCE":

        # First validate the requested attendance record
        prepared = prepare_attendance_update(entities)

        if not prepared.get("success"):
            return prepared

        # Directly update MySQL without another confirmation
        return confirm_attendance_update(prepared.get("data", {}))

    else:
        return {
            "success": False,
            "message": "Sorry, I could not understand that command."
        }
