from erp_commands import execute_command

result = {
    "intent": "VIEW_ACADEMIC_CALENDAR",
    "entities": {}
}

response = execute_command(result)

print(response)