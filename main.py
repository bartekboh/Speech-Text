import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pyaudio
import wave
from tkinter import *

root = Tk()
root.title('Speach - Text')
root.geometry("400x600")

r = sr.Recognizer()


def get_large_audio_transcription(path):
    # open the audio file - pydub
    sound = AudioSegment.from_wav(path)
    # split audio when silence
    chunks = split_on_silence(sound,
                              min_silence_len=500,
                              silence_thresh=sound.dBFS - 14,
                              keep_silence=500)
    folder_name = "audio-chunks"
    # directory to store the audio
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process audio
    for i, audio_chunk in enumerate(chunks, start=1):
        # export and save audio
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # convert to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                if str(e):
                    print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                whole_text += text
    # return the text
    return whole_text


chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100
seconds = 3
filename = "output.wav"

p = pyaudio.PyAudio()

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []

for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

print("Recording finished!")

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()


# functions
def on_click():
    addTextBox.configure(state=NORMAL)
    addTextBox.delete(0, END)

    addTextBox.unbind('<Button-1>', on_click_id)


def reset():
    f = open(r"C:\Users\barte\PycharmProjects\pythonProject1\files\text.txt", "r+")
    f.truncate(0)


# def restart():
#     os.execv(sys.executable, ['python'] + sys.argv)

def add():
    addedLabel = Label(root, text=addTextBox.get())
    addedLabel.pack()
    addedLabel.place(x=160, y=50)

    addedText = addTextBox.get()
    f = open(r"C:\Users\barte\PycharmProjects\pythonProject1\files\text.txt", "a+")
    f.write(addedText + "\n")
    f.close()


def read():
    f = open(r"C:\Users\barte\PycharmProjects\pythonProject1\files\text.txt", "r")
    readLabel = Label(root, text=f.read())
    readLabel.pack()
    readLabel.place(x=160, y=100)


def quit():
    exit()


def inProgress():
    inProgressLabel = Label(root, text="In progress", height="2", width="12", bg="lightgrey", cursor="cross")
    inProgressLabel.pack()
    inProgressLabel.place(x=10, y=110)


# labels
whole_text = get_large_audio_transcription("output.wav")

f = open(r"C:\Users\barte\PycharmProjects\pythonProject1\files\text.txt", "a+")
f.write(whole_text + "\n")
f.close()

audio_label = Label(root, text="Added: " + whole_text)
audio_label.pack()
audio_label.place(x=160, y=10)

# entry(textBoxes)
addTextBox = Entry(root, width=30)
addTextBox.pack()
addTextBox.place(x=160, y=30)

# buttons
buttonSizew = 12
buttonSizeh = 2

addButton = Button(root, text="Add", command=add, background="lightgrey", width=buttonSizew, height=buttonSizeh)
addButton.place(x=10, y=10)


readButton = Button(root, text="Read", command=read, background="lightgrey", width=buttonSizew, height=buttonSizeh)
readButton.place(x=10, y=60, bordermode='ignore')

restartButton = Button(root, text="Restart", command=inProgress, background="lightgrey", width=buttonSizew,height=buttonSizeh)
restartButton.place(x=10, y=110)

resetButton = Button(root, text="Reset", command=reset, background="lightgrey", width=buttonSizew, height=buttonSizeh)
resetButton.place(x=10, y=160)

quitButton = Button(root, text="Quit", command=quit, background="lightgrey", width=buttonSizew, height=buttonSizeh)
quitButton.place(x=10, y=210)

on_click_id = addTextBox.bind('<Button-1>', on_click)

root.mainloop()