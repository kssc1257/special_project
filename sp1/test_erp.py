from erp_commands import prepare_attendance_update

entities = {
    "student": "Rahul",
    "section": "E",
    "date": "2026-09-01",
    "session": "2",
    "status": "Absent"
}

result = prepare_attendance_update(entities)

print(result)