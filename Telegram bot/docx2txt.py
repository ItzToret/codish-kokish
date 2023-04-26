import aspose.words as aw
import pyttsx3

doc = aw.Document("ts.docx")
doc.save("ts1.txt")

with open('ts1.txt') as old, open('ts2.txt', 'w') as new:
        lines = old.readlines()
        new.writelines(lines[2:-1])
file = open('ts2.txt', 'r', encoding="utf-8")
text = file.read()
engine = pyttsx3.init()
engine.save_to_file(text, 'ts2.mp3')
engine.runAndWait()