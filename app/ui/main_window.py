import tkinter as tk
from tkinter import ttk, messagebox
import threading

from app.controllers.app_controller import AppController


class MainWindow:
    def __init__(self):
        self.controller = AppController()

        self.root = tk.Tk()
        self.root.title("GPT Data Analysis Dashboard")
        self.root.geometry("1050x780")
        self.root.resizable(False, False)

        self._build_ui()
        self._load_summary()

    def _build_ui(self):
        title_label = tk.Label(
            self.root,
            text="GPT Data Collection & Analysis Dashboard",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=15)

        subtitle_label = tk.Label(
            self.root,
            text="Collect GPT-related data and display analytical summaries from MongoDB",
            font=("Arial", 11)
        )
        subtitle_label.pack(pady=5)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        self.youtube_button = tk.Button(
            button_frame,
            text="Collect from YouTube API",
            width=24,
            height=2,
            command=self._run_youtube_api
        )
        self.youtube_button.grid(row=0, column=0, padx=10)

        self.reddit_button = tk.Button(
            button_frame,
            text="Collect from Reddit Selenium",
            width=24,
            height=2,
            command=self._run_reddit_selenium
        )
        self.reddit_button.grid(row=0, column=1, padx=10)

        self.refresh_button = tk.Button(
            button_frame,
            text="Refresh Summary",
            width=20,
            height=2,
            command=self._load_summary
        )
        self.refresh_button.grid(row=0, column=2, padx=10)

        self.progress = ttk.Progressbar(
            self.root,
            mode="indeterminate",
            length=350
        )
        self.progress.pack(pady=10)

        summary_frame = tk.LabelFrame(
            self.root,
            text="General GPT Dataset Summary",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        summary_frame.pack(fill="x", padx=20, pady=8)

        self.summary_text = tk.Text(
            summary_frame,
            height=12,
            width=120,
            state="disabled",
            font=("Courier New", 10)
        )
        self.summary_text.pack()

        monthly_frame = tk.LabelFrame(
            self.root,
            text="Monthly Analysis",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        monthly_frame.pack(fill="x", padx=20, pady=8)

        self.monthly_text = tk.Text(
            monthly_frame,
            height=12,
            width=120,
            state="disabled",
            font=("Courier New", 10)
        )
        self.monthly_text.pack()

        log_frame = tk.LabelFrame(
            self.root,
            text="System Log",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )
        log_frame.pack(fill="both", expand=True, padx=20, pady=8)

        self.log_text = tk.Text(
            log_frame,
            height=8,
            width=120,
            state="disabled"
        )
        self.log_text.pack(fill="both", expand=True)

    def _append_log(self, message: str):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def _set_buttons_state(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.youtube_button.config(state=state)
        self.reddit_button.config(state=state)
        self.refresh_button.config(state=state)

    def _format_general_summary(self, summary: dict) -> str:
        lines = []
        lines.append("=" * 75)
        lines.append("GENERAL SUMMARY")
        lines.append("=" * 75)
        lines.append(f"Total GPT-related records in database : {summary['total_records']}")
        lines.append(f"YouTube records                       : {summary['youtube_count']}")
        lines.append(f"Reddit records                        : {summary['reddit_count']}")
        lines.append(f"API-collected records                 : {summary['api_count']}")
        lines.append(f"Selenium-collected records            : {summary['scraping_count']}")
        lines.append(f"Average text length                   : {summary['avg_text_length']}")
        lines.append("")

        lines.append("=" * 75)
        lines.append("TOP 5 TOPICS")
        lines.append("=" * 75)
        for item in summary["top_topics"]:
            lines.append(f"{str(item['_id']):<35} -> {item['count']}")

        lines.append("")
        lines.append("=" * 75)
        lines.append("TOP 5 AUTHORS / CHANNELS")
        lines.append("=" * 75)
        for item in summary["top_authors"]:
            lines.append(f"{str(item['_id']):<35} -> {item['count']}")

        return "\n".join(lines)

    def _format_monthly_summary(self, summary: dict) -> str:
        lines = []
        lines.append("=" * 75)
        lines.append("POSTS ABOUT GPT BY MONTH")
        lines.append("=" * 75)

        if not summary["posts_per_month"]:
            lines.append("No monthly data available.")
        else:
            for item in summary["posts_per_month"]:
                year = item["_id"]["year"]
                month = item["_id"]["month"]
                count = item["count"]
                lines.append(f"{year}-{month:02d} -> {count} posts")

        lines.append("")
        lines.append("=" * 75)
        lines.append("POSTS BY MONTH AND SOURCE")
        lines.append("=" * 75)

        if not summary["posts_per_month_by_source"]:
            lines.append("No monthly/source data available.")
        else:
            for item in summary["posts_per_month_by_source"]:
                year = item["_id"]["year"]
                month = item["_id"]["month"]
                source = item["_id"]["source"]
                count = item["count"]
                lines.append(f"{year}-{month:02d} | {source:<10} -> {count} posts")

        return "\n".join(lines)

    def _update_summary_boxes(self, summary: dict):
        general_text = self._format_general_summary(summary)
        monthly_text = self._format_monthly_summary(summary)

        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, general_text)
        self.summary_text.config(state="disabled")

        self.monthly_text.config(state="normal")
        self.monthly_text.delete("1.0", tk.END)
        self.monthly_text.insert(tk.END, monthly_text)
        self.monthly_text.config(state="disabled")

    def _load_summary(self):
        try:
            summary = self.controller.get_gpt_data_summary()
            self._update_summary_boxes(summary)
            self._append_log("Summary refreshed successfully.")
        except Exception as e:
            self._append_log(f"Summary refresh error: {e}")
            messagebox.showerror("Error", f"Failed to load summary:\n{e}")

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

            self.root.after(0, self._load_summary)

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

            self.root.after(0, self._load_summary)

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