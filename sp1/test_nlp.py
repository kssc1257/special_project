from nlp_service import understand_command

print("ERP NLP Testing")
print("Type exit to stop")

while True:

    sentence = input("\nEnter a command: ")

    if sentence.lower() == "exit":
        break

    result = understand_command(sentence)

    print("\nTranscript:", result["transcript"])
    print("Intent:", result["intent"])
    print("Entities:", result["entities"])