from nlp_service import understand_command
from erp_commands import execute_command

transcript = "Show me the upcoming exams"

nlp_result = understand_command(transcript)

print("NLP Result:")
print(nlp_result)

erp_result = execute_command(nlp_result)

print("\nERP Result:")
print(erp_result)