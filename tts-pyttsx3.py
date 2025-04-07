'''
Python implementation of converting Text-To-Speech (TTS) offline with the 
pyttsx3 library. The input text is entered in a GUI, along with the speech 
speed/rate, volume, and voice type (e.g., male/female). The output is an audio
speech that can be saved as an .mp3 audio file.

'''
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import tkinter.font as tkFont
import ctypes # to get screen size

engine = pyttsx3.init()
# Adding an argument gets a reference to an engine instance that will use the given driver.
# engine = pyttsx3.init(driverName='sapi5') #SAPI5  Windows
# engine = pyttsx3.init(driverName='nsss') # NSSpeechSynthesizer on Mac OS X
# engine = pyttsx3.init(driverName='espeak') # eSpeak on Linux and every other platform 
voices = engine.getProperty('voices')
voice_name_list = [voice.name for voice in voices]


def process_tts(text, speech_rate, volume_level, voice_name_selection, savefile):
    global engine
    # Set voice
    voice_index = voice_name_list.index(voice_name_selection)
    try:
        voice_index = int(voice_index)
        assert voice_index >= 0
    except Exception :
        error_msg = "Could not find selected voice"
        messagebox.showerror("Input Error", error_msg)
        return None
    engine.setProperty('voice', voices[voice_index].id)
    
    # Set speech rate
    # the rate is an integer which corresponds to the number of words per minute
    # default rate is 200
    # rate = engine.getProperty('rate')
    engine.setProperty('rate', speech_rate)

    # Set volume 
    # Volume level is between 0 and 1.0
    # The default volume is set to 1.0, which is the maximum volume.
    # volume = engine.getProperty('volume')
    engine.setProperty('volume', volume_level)
    
    # running text-to-speech
    engine.say(text)
    engine.runAndWait()
    if savefile: engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()


def submit_text(scrolledText, entry1_var, entry2_var, combo, savefile_var):
    input_text = scrolledText.get('1.0', 'end-1c')
    if not input_text:
        error_msg = "Enter a text to convert to speech"
        messagebox.showerror("Input Error", error_msg)
        return None
        
    speech_rate_str = entry1_var.get()
    try:
        speech_rate = int(speech_rate_str)
        assert speech_rate > 0
    except Exception :
        error_msg = "Enter a positive integer for the speech rate"
        messagebox.showerror("Input Error", error_msg)
        return None
    
    volume_level_str = entry2_var.get()
    try:
        volume_level = float(volume_level_str)
        assert volume_level > 0 and volume_level <= 1.0
    except Exception :
        error_msg = "Enter a positive floating point number between 0 and 1.0 for the volume level"
        messagebox.showerror("Input Error", error_msg)
        return None
    
    voice_name_selection = combo.get()
    savefile = savefile_var.get()
    process_tts(input_text, speech_rate, volume_level, voice_name_selection, savefile)


def main():
    user32 = ctypes.windll.user32
    (screensize_width, screensize_height) = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print("(screensize_width, screensize_height)", (screensize_width, screensize_height))
    input_window = tk.Tk()
    input_window.title("Input Text")
    input_window_width = int(0.3*screensize_width)
    input_window_height = int(0.45*screensize_height)
    input_window.geometry(f"{input_window_width}x{input_window_height}")
    input_window.eval('tk::PlaceWindow . center')
    tk.Label(input_window, text="Enter text to convert to speech", font=("Segoe UI", 14)).grid(row=0, pady=(10,0))
    scrolledText = scrolledtext.ScrolledText(input_window, wrap=tk.WORD, width=60, height=10) # width and height units are number of characters
    default_text_str = "Hello! My current volume is 1.0 and speaking rate is 200 words per minute."
    scrolledText.insert(tk.INSERT, default_text_str)
    scrolledText.grid(row=1, column=0, sticky="nsew", padx=10)
    input_window.columnconfigure(0, weight=1)

    # declaring string variable for storing 3 inputs
    entry1_var = tk.StringVar()
    entry2_var = tk.StringVar()
    voice_var = tk.StringVar()
    savefile_var = tk.BooleanVar()
    savefile_var.set(False)

    # Speech Rate
    tk.Label(input_window, text="Enter speech rate words/min (default=200)", font=("Segoe UI", 14)).grid(row=2, pady=(20,0))
    entry1 = tk.Entry(input_window, font=("Arial",14), textvariable=entry1_var, justify='center', width=7)
    entry1.insert(0, '200')
    entry1.grid(row=3, column=0)

    # Volume Level
    tk.Label(input_window, text="Enter volume level between 0 and 1.0 (default=1.0)", font=("Segoe UI", 14)).grid(row=4, pady=(10,0))
    entry2 = tk.Entry(input_window, font=("Arial",14), textvariable=entry2_var, justify='center', width=7)
    entry2.insert(0, '1.0')
    entry2.grid(row=5, column=0)
    
    # Voices Dropdown Menu
    combo = ttk.Combobox(state="readonly", values=voice_name_list)
    combo.set("Select a voice")
    combo.grid(row=6, column=0, pady=15)
    max_width_in_num_char = max(len(item) for item in voice_name_list)
    combo.configure(width=max_width_in_num_char)

    tk.Checkbutton(input_window, text="Save output.mp3 file", variable=savefile_var).grid(row=7, column=0)
    
    btn = tk.Button(input_window, text="Submit", command=lambda: submit_text(scrolledText, entry1_var, entry2_var, combo, savefile_var))
    btn.grid(row=8, column=0, pady=10)
    
    # Right click menu for copy and select all
    right_click_menu = tk.Menu(scrolledText, tearoff=0)
    # Menu options
    right_click_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: scrolledText.event_generate("<<Copy>>"))
    right_click_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: scrolledText.event_generate("<<Paste>>"))
    right_click_menu.add_command(label="Select All", accelerator="Ctrl+A", command=lambda: scrolledText.event_generate("<<SelectAll>>"))
    # Make menu pop up on right click event
    scrolledText.bind("<Button -3>", lambda event: right_click_menu.tk_popup(event.x_root, event.y_root))
    
    input_window.mainloop()

if __name__ == "__main__":
    main()