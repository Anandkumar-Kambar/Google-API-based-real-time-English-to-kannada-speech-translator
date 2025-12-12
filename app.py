# Import Necessary Libraries
import speech_recognition as spr
from gtts import gTTS
import os
import platform
from deep_translator import GoogleTranslator

# Initialize Recognizers and Microphone
recog1 = spr.Recognizer()
recog2 = spr.Recognizer()

# Find the correct microphone device
print("Available microphones:")
for index, name in enumerate(spr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

mc = spr.Microphone(device_index=0)  # Replace 0 with your microphone index from the list

# Function to Play Audio
def play_audio(file_path):
    if platform.system() == "Windows":
        os.system(f"start {file_path}")
    elif platform.system() == "Darwin":  # macOS
        os.system(f"open {file_path}")
    else:  # Linux
        os.system(f"xdg-open {file_path}")

# Function for Translation and Text-to-Speech
def translate_and_speak(from_lang, to_lang):
    with mc as source:
        print("Speak a sentence...")
        audio = recog2.listen(source)

        try:
            # Recognize and translate speech
            get_sentence = recog2.recognize_google(audio, language=from_lang) # type: ignore
            print(f"Phrase to be Translated ({from_lang} → {to_lang}): {get_sentence}")

            # Using GoogleTranslator for translation
            translated_text = GoogleTranslator(source=from_lang, target=to_lang).translate(get_sentence)
            print(f"Translated Phrase: {translated_text}")

            # Convert text to speech 
            speak = gTTS(text=translated_text, lang=to_lang, slow=False)
            speak.save("captured_voice.mp3")
            play_audio("captured_voice.mp3")
        except spr.UnknownValueError:
            print("Unable to understand the input.")
        except spr.RequestError as e:
            print(f"Error with the recognition service: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Main Logic
try:
    with mc as source:
        print("Speak 'Hello' for English → Kannada OR 'Namaskara' for Kannada → English.")
        print("-------------------------------------------------------------")
        audio = recog1.listen(source)

    # Recognize the initial command to decide the translation direction
    command = recog1.recognize_google(audio) # type: ignore

    if "hello" in command.lower():
        print("English → Kannada Translation Selected")
        translate_and_speak(from_lang="en", to_lang="kn")
    elif "namaskara" in command.lower():
        print("Kannada → English Translation Selected")
        translate_and_speak(from_lang="kn", to_lang="en")
    else:
        print("Keyword not recognized. Please say 'Hello' or 'Namaskara'.")
except spr.UnknownValueError:
    print("Speech not understood. Please try again.")
except spr.RequestError as e:
    print(f"Error with the recognition service: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}") 