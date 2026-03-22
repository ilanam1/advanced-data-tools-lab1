import tkinter as tk
from tkinter import ttk, messagebox
import threading

from app.controllers.app_controller import AppController


class MainWindow:
    def __init__(self):
        self.controller = AppController()

        self.root = tk.Tk()
        self.root.title("Advanced Data Tools Lab")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        title_label = tk.Label(
            self.root,
            text="Data Collection System",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)

        subtitle_label = tk.Label(
            self.root,
            text="Choose which collection method to run",
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        self.youtube_button = tk.Button(
            button_frame,
            text="Run YouTube API",
            width=20,
            height=2,
            command=self._run_youtube_api
        )
        self.youtube_button.grid(row=0, column=0, padx=15)

        self.reddit_button = tk.Button(
            button_frame,
            text="Run Reddit Selenium",
            width=20,
            height=2,
            command=self._run_reddit_selenium
        )
        self.reddit_button.grid(row=0, column=1, padx=15)

        self.progress = ttk.Progressbar(
            self.root,
            mode="indeterminate",
            length=300
        )
        self.progress.pack(pady=15)

        log_label = tk.Label(
            self.root,
            text="System Log:",
            font=("Arial", 11, "bold")
        )
        log_label.pack(anchor="w", padx=20)

        self.log_text = tk.Text(
            self.root,
            height=10,
            width=68,
            state="disabled"
        )
        self.log_text.pack(padx=20, pady=10)

    def _append_log(self, message: str):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def _set_buttons_state(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.youtube_button.config(state=state)
        self.reddit_button.config(state=state)

    def _run_youtube_api(self):
        thread = threading.Thread(target=self._youtube_task, daemon=True)
        thread.start()

    def _run_reddit_selenium(self):
        thread = threading.Thread(target=self._reddit_task, daemon=True)
        thread.start()

    def _youtube_task(self):
        try:
            self.root.after(0, lambda: self._set_buttons_state(False))
            self.root.after(0, self.progress.start)
            self.root.after(0, lambda: self._append_log("Starting YouTube API collection..."))

            result = self.controller.run_youtube_api_collection()

            self.root.after(
                0,
                lambda: self._append_log(
                    f"[{result['source']}] Collected: {result['collected']} | Inserted: {result['inserted']}"
                )
            )
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success",
                    f"YouTube API finished successfully.\nCollected: {result['collected']}\nInserted: {result['inserted']}"
                )
            )

        except Exception as e:
            self.root.after(0, lambda: self._append_log(f"YouTube API error: {e}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"YouTube API failed:\n{e}"))

        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self._set_buttons_state(True))

    def _reddit_task(self):
        try:
            self.root.after(0, lambda: self._set_buttons_state(False))
            self.root.after(0, self.progress.start)
            self.root.after(0, lambda: self._append_log("Starting Reddit Selenium collection..."))

            result = self.controller.run_reddit_selenium_collection()

            self.root.after(
                0,
                lambda: self._append_log(
                    f"[{result['source']}] Collected: {result['collected']} | Inserted: {result['inserted']}"
                )
            )
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success",
                    f"Reddit Selenium finished successfully.\nCollected: {result['collected']}\nInserted: {result['inserted']}"
                )
            )

        except Exception as e:
            self.root.after(0, lambda: self._append_log(f"Reddit Selenium error: {e}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Reddit Selenium failed:\n{e}"))

        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self._set_buttons_state(True))

    def run(self):
        self.root.mainloop()