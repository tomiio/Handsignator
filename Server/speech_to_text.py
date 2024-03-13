import speech_recognition as sr

def convert_speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)  # Read the audio file
        
    try:
        text = recognizer.recognize_sphinx(audio, language='vi-VN')  # Perform Vietnamese speech recognition
        return text
    except sr.UnknownValueError:
        print("Cannot recognize speech.")
    except sr.RequestError as e:
        print(f"Error: {e}")


audio_file = "/home/pihand/Documents/file.wav"  # Replace with the path to your WAV audio file
text = convert_speech_to_text(audio_file)
print(text)
