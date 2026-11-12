
import re
import joblib

from pathlib import Path
from datetime import date, timedelta, datetime


# --------------------------------------------------
# 1. LOAD TRAINED INTENT MODEL
# --------------------------------------------------

MODEL_PATH = Path(__file__).resolve().parent / "intent_model.joblib"

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# 2. TEXT PREPROCESSING
# --------------------------------------------------

def preprocess(text):

    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)

    return text


# --------------------------------------------------
# 3. ENTITY EXTRACTION
# --------------------------------------------------

def extract_entities(text):

    entities = {}
    text = text.lower().strip()

    # A. SECTION
    section = re.search(r"\bsection\s+([a-z])\b", text)

    if section:
        entities["section"] = section.group(1).upper()

    # B. ATTENDANCE STATUS
    if re.search(r"\babsent\b", text):
        entities["status"] = "Absent"

    elif re.search(r"\bpresent\b", text):
        entities["status"] = "Present"

    # C. STUDENT NAME
    student_patterns = [

        # Mark Rahul absent
        r"\b(?:mark|record|enter)\s+"
        r"([a-z]+(?:\s+[a-z]+)?)\s+"
        r"(?:as\s+)?(?:absent|present)\b",

        # Mark attendance for Rahul as absent
        r"\b(?:mark|record|enter)\s+attendance\s+for\s+"
        r"([a-z]+(?:\s+[a-z]+)?)\s+"
        r"(?:as\s+)?(?:absent|present)\b",

        # Update Rahul's attendance
        r"\bupdate\s+"
        r"([a-z]+(?:\s+[a-z]+)?)'s\s+attendance\s+"
        r"(?:as|to)\s+(?:absent|present)\b",

        # Change Rahul's attendance
        r"\bchange\s+"
        r"([a-z]+(?:\s+[a-z]+)?)'s\s+attendance\s+"
        r"to\s+(?:absent|present)\b",

        # Show Rahul's attendance
        r"\b(?:show|display|get|check|view)\s+"
        r"(?:me\s+)?"
        r"([a-z]+(?:\s+[a-z]+)?)'s\s+attendance\b",

        # Show attendance for Rahul
        r"\b(?:show|display|get|check|view)\s+"
        r"(?:me\s+)?attendance\s+for\s+"
        r"([a-z]+(?:\s+[a-z]+)?)\b",

        # Show attendance of Rahul
        r"\b(?:show|display|get|check|view)\s+"
        r"(?:me\s+)?attendance\s+of\s+"
        r"([a-z]+(?:\s+[a-z]+)?)\b"
    ]

    for pattern in student_patterns:

        match = re.search(pattern, text)

        if match:
            student_name = match.group(1).strip()

            if student_name.lower().startswith("section "):
                continue

            entities["student"] = student_name.title()
            break

    # D. DATE: TODAY AND TOMORROW
    if re.search(r"\btoday\b", text):
        entities["date"] = date.today().isoformat()

    elif re.search(r"\btomorrow\b", text):
        entities["date"] = (
            date.today() + timedelta(days=1)
        ).isoformat()

    # E. EXPLICIT NUMERIC DATE
    date_patterns = [
        (r"\b(\d{2}-\d{2}-\d{4})\b", "%d-%m-%Y"),
        (r"\b(\d{4}-\d{2}-\d{2})\b", "%Y-%m-%d"),
        (r"\b(\d{2}/\d{2}/\d{4})\b", "%d/%m/%Y")
    ]

    for pattern, date_format in date_patterns:

        match = re.search(pattern, text)

        if match:
            try:
                parsed_date = datetime.strptime(
                    match.group(1), date_format
                )

                entities["date"] = parsed_date.strftime("%Y-%m-%d")
                break

            except ValueError:
                pass

    # F. MONTH-NAME DATE
    month_date = re.search(
        r"\b("
        r"january|february|march|april|may|june|"
        r"july|august|september|october|november|december|"
        r"jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec"
        r")\s+(\d{1,2})(?:st|nd|rd|th)?"
        r"(?:,?\s+(\d{4}))?\b",
        text
    )

    if not month_date:
        month_date = re.search(
            r"\b(\d{1,2})(?:st|nd|rd|th)?\s+"
            r"(january|february|march|april|may|june|"
            r"july|august|september|october|november|december|"
            r"jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)"
            r"(?:\s+(\d{4}))?\b",
            text
        )

        if month_date:
            month = month_date.group(2)
            day_number = month_date.group(1)
            year = month_date.group(3)
        else:
            month = None

    else:
        month = month_date.group(1)
        day_number = month_date.group(2)
        year = month_date.group(3)

    if month:
        try:
            year = int(year) if year else date.today().year

            parsed_date = datetime.strptime(
                f"{day_number} {month} {year}",
                "%d %B %Y"
            )

            entities["date"] = parsed_date.strftime("%Y-%m-%d")

        except ValueError:
            try:
                parsed_date = datetime.strptime(
                    f"{day_number} {month} {year}",
                    "%d %b %Y"
                )

                entities["date"] = parsed_date.strftime("%Y-%m-%d")

            except ValueError:
                pass

    # G. SESSION OR PERIOD
    session_match = re.search(
        r"\b(?:session|period)\s+(\d+)\b", text
    )

    if session_match:
        entities["session"] = session_match.group(1)

    # H. DAY OF THE WEEK
    days = [
        "monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"
    ]

    for day in days:
        if re.search(rf"\b{day}\b", text):
            entities["day"] = day.title()
            break

    if re.search(r"\btoday\b", text):
        entities["day"] = date.today().strftime("%A")

    elif re.search(r"\btomorrow\b", text):
        entities["day"] = (
            date.today() + timedelta(days=1)
        ).strftime("%A")

    # I. EXACT TIMETABLE TIME SLOT
    
    
    time_match = re.search(
        r"\b(?:from\s+)?"
        r"(\d{1,2})\s*[:.\-]?\s*(\d{2})\s*"
        r"(?:am|pm)?\s*"
        r"(?:to|until|[-–—])\s*"
        r"(\d{1,2})\s*[:.\-]?\s*(\d{2})"
        r"(?:am|pm)?\b",
        text
    )

    if time_match:
        start_hour = int(time_match.group(1))
        start_minute = int(time_match.group(2))
        end_hour = int(time_match.group(3))
        end_minute = int(time_match.group(4))

        if (
            start_hour <= 23
            and end_hour <= 23
            and start_minute <= 59
            and end_minute <= 59
        ):
            start_time = f"{start_hour}:{start_minute:02d}"
            end_time = f"{end_hour}:{end_minute:02d}"

            entities["time_slot"] = f"{start_time} - {end_time}"

    # J. UPCOMING HOLIDAY
    if re.search(r"\b(upcoming|next)\s+holiday\b", text):
        entities["upcoming_holiday"] = True

    return entities



# --------------------------------------------------
# 4. UNDERSTAND THE COMMAND
# --------------------------------------------------


def classify_intent(text):

    text = text.lower().strip()

    # 1. Attendance marking commands
    if (
        re.search(
            r"\b(mark|record|enter|update|change|set)\b",
            text
        )
        and re.search(
            r"\b(attendance|absent|present)\b",
            text
        )
    ):
        return "MARK_ATTENDANCE"

    # 2. Attendance viewing commands
    if (
        re.search(
            r"\b(attendance|attendence)\b",
            text
        )
        and re.search(
            r"\b(show|display|get|check|view|retrieve|see)\b",
            text
        )
    ):
        return "VIEW_ATTENDANCE"

    # Student-specific attendance viewing
    if re.search(
        r"\b(show|display|get|check|view)\b.*"
        r"\battendance\b",
        text
    ):
        if not re.search(
            r"\b(mark|record|enter|update|change|set)\b",
            text
        ):
            return "VIEW_ATTENDANCE"

    # 3. Academic calendar commands
    if re.search(
        r"\b(calendar|holiday|holidays|academic event|"
        r"academic events|college event|college events)\b",
        text
    ):
        return "VIEW_ACADEMIC_CALENDAR"

    if re.search(
        r"\b(event|activity|activities)\b",
        text
    ) and re.search(
        r"\b(when|what|show|display|next|upcoming|scheduled)\b",
        text
    ):
        return "VIEW_ACADEMIC_CALENDAR"

    # 4. Timetable commands
    if re.search(
        r"\b(timetable|lecture|lectures|class schedule|"
        r"class timings|classes)\b",
        text
    ):
        return "VIEW_TIMETABLE"

    # 5. Use trained ML model for other commands
    return model.predict([preprocess(text)])[0]


def understand_command(transcript):

    intent = classify_intent(transcript)

    entities = extract_entities(transcript)

    return {
        "transcript": transcript,
        "intent": intent,
        "entities": entities
    }

