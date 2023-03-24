import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# for voice in voices:
#     print('--')
#     print(f'Имя: {voice.name}')
#     print(f'ID: {voice.id}')
#     print(f'Язык: {voice.languages}')
#     print(f'Пол: {voice.gender}')
#     print(f'Возраст: {voice.age}')

engine.save_to_file('прикольный прикол' , 'test2.mp3')

engine.runAndWait()