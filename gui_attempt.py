import tkinter as tk
from tkinter import messagebox
from time import sleep
import pygame
from os import listdir
from random import randint
import threading
import time 

# --- PLACEHOLDER FOR EXTERNAL FUNCTIONS ---

# This simulates importing 'cat' from ascii_art.py
# In your full environment, you would ensure ascii_art.py exists and contains the full 'cat' function.
def cat(message, loop):
    """
    Simulates the cat function from ascii_art.py.
    The real function's output would be displayed in the Text widget.
    """
    # Simply returns the message for the status and uses the loop number for cycling effect
    frame_indicator = loop % 22  # Assuming 22 frames in the real cat function
    
    # Return a stylized string that shows the countdown and frame number
    if "TIME IS UP" in message:
        return f"\n\n\n\n\n\nLE TEMPS EST FINIT"
    
    return f"Frame: {frame_indicator:02d}\n{message}"

# --- TIMER APPLICATION CLASS ---

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("Python Tkinter ASCII Timer")

        try:
            pygame.mixer.init()
        except pygame.error as e:
            messagebox.showerror("Pygame Error", f"Could not initialize pygame mixer: {e}. Check if sound drivers are installed.")
            master.destroy()
            return

        self.timer_running = False
        self.alarm_file = None
        self.waiting_song_file = None
        self.alarm_options = self.get_alarm_options()
        self.message_loop_tracker = 0 # To track which cat frame to display

        self.create_widgets()

    def get_alarm_options(self):
        """Gets list of available sound files from the 'sounds' directory."""
        try:
            return [f for f in listdir("sounds") if f.endswith(('.mp3', '.wav', '.ogg'))]
        except FileNotFoundError:
            messagebox.showerror("Error", "The 'sounds' directory was not found. Please create it and add sound files.")
            return []

    def create_widgets(self):
        """Sets up the GUI layout."""
        
        # 1. Time Limit Input
        tk.Label(self.master, text="Timer Length (M:S):").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.time_limit_entry = tk.Entry(self.master)
        self.time_limit_entry.insert(0, "00:15") # Default to 15 seconds for testing
        self.time_limit_entry.grid(row=0, column=1, padx=10, pady=5)

        # 2. Alarm Selection (Dropdown)
        tk.Label(self.master, text="Select Alarm Sound:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        if self.alarm_options:
            self.selected_alarm = tk.StringVar(self.master)
            self.selected_alarm.set(self.alarm_options[0]) # Default value
            alarm_menu = tk.OptionMenu(self.master, self.selected_alarm, *self.alarm_options)
            alarm_menu.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        else:
            tk.Label(self.master, text="No sounds found!").grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        # --- ASCII Art Display (Using a Text widget) ---
        # A Text widget is necessary to display multi-line ASCII art properly.
        tk.Label(self.master, text="--- ASCII Art Timer Display ---").grid(row=2, column=0, columnspan=2, pady=5)
        self.ascii_display = tk.Text(self.master, height=15, width=80, font=('Courier', 8), bg='black', fg='lime', borderwidth=2, relief="sunken")
        self.ascii_display.insert(tk.END, cat("Ready to start the timer!", 0))
        self.ascii_display.config(state=tk.DISABLED) # Make it read-only
        self.ascii_display.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # 4. Control Buttons
        self.start_button = tk.Button(self.master, text="Start Timer", command=self.start_timer_thread)
        self.start_button.grid(row=4, column=0, padx=10, pady=10, sticky='ew')

        self.stop_alarm_button = tk.Button(self.master, text="Stop Alarm", command=self.stop_alarm, state=tk.DISABLED)
        self.stop_alarm_button.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

    def update_ascii_display(self, message):
        """Safely updates the Text widget from the background thread."""
        self.ascii_display.config(state=tk.NORMAL)
        self.ascii_display.delete(1.0, tk.END)
        self.ascii_display.insert(tk.END, message)
        self.ascii_display.config(state=tk.DISABLED)

    def convert_time_to_seconds(self, time_str):
        """Converts 'M:S' string to total seconds."""
        try:
            minutes, seconds = map(int, time_str.split(':'))
            return minutes * 60 + seconds
        except ValueError:
            return None

    def start_timer_thread(self):
        """Initializes and starts the timer in a separate thread."""
        if self.timer_running:
            return

        time_limit_str = self.time_limit_entry.get()
        self.time_limit_seconds = self.convert_time_to_seconds(time_limit_str)

        if self.time_limit_seconds is None or self.time_limit_seconds <= 0:
            messagebox.showerror("Input Error", "Invalid time format or time limit. Use M:S format (e.g., 00:15).")
            return

        if not self.alarm_options:
            messagebox.showerror("Error", "Cannot start without alarm sound options.")
            return

        self.alarm_file = f"sounds/{self.selected_alarm.get()}"
        
        self.timer_running = True
        self.start_button.config(state=tk.DISABLED)
        self.message_loop_tracker = 0 # Reset frame tracker

        # Start the non-blocking timer logic in a thread
        threading.Thread(target=self.track_time, daemon=True).start()

    def track_time(self):
        """The core timer logic, running in a separate thread."""
        
        # --- Start Waiting Song ---
        song_options = self.alarm_options
        random_song = song_options[randint(0, len(song_options) - 1)]
        self.waiting_song_file = f'sounds/{random_song}'
        try:
            pygame.mixer.music.load(self.waiting_song_file)
            pygame.mixer.music.play(loops=-1)
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Playback Error", f"Error playing waiting song: {e}"))
            self.timer_running = False
            self.master.after(0, self.reset_gui_controls)
            return

        duration = self.time_limit_seconds
        
        # --- Timer Loop (Countdown) ---
        for i in range(duration, -1, -1):
            if not self.timer_running:
                break 

            minutes = i // 60
            seconds = i % 60
            time_left = f"You have {minutes:02d}:{seconds:02d} seconds left"
            
            # 1. Generate the ASCII art using the imported 'cat' function
            # The 'cat' function handles the cycling of frames (0-21)
            ascii_message = cat(time_left, self.message_loop_tracker)

            # 2. Update GUI display using self.master.after
            self.master.after(0, lambda m=ascii_message: self.update_ascii_display(m))
            
            # 3. Advance the frame counter (cycles 0-21)
            self.message_loop_tracker = (self.message_loop_tracker + 1) % 22
            
            # Sleep for 1 second
            time.sleep(1)
        
        # --- Timer Finished ---
        if self.timer_running:
            self.timer_running = False
            self.master.after(0, self.timer_finished)

    def timer_finished(self):
        """Called when the timer hits zero."""
        pygame.mixer.music.stop()
        
        final_ascii = cat('LE TEMPS EST FINIT', 0)
        self.update_ascii_display(final_ascii)
        
        self.play_alarm()
    
    def play_alarm(self):
        """Plays the selected alarm sound."""
        try:
            pygame.mixer.music.load(self.alarm_file)
            pygame.mixer.music.play(loops=-1)
            self.stop_alarm_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Playback Error", f"Error playing alarm: {e}")
            self.stop_alarm_button.config(state=tk.DISABLED)
            self.reset_gui_controls()

    def stop_alarm(self):
        """Stops the alarm music and resets controls."""
        pygame.mixer.music.stop()
        self.update_ascii_display(cat("Alarm Stopped", 0))
        self.reset_gui_controls()

    def reset_gui_controls(self):
        """Resets buttons after a run."""
        self.timer_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_alarm_button.config(state=tk.DISABLED)

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
