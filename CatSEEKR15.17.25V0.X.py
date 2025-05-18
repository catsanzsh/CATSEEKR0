# tset.py - CATSEEK R1 GUI Core (Modernized)
import tkinter as tk
from tkinter import scrolledtext, font, ttk
import random

class CatMind:
    def __init__(self):
        self.knowledge = {
            'responses': {
                'hello': ["Meow! Welcome human.", "Purr... Ready for questions?", 
                        "*head bump* Hello!"],
                'question': ["Ancient feline secret... but where's the tuna?", 
                           "Paw-sitive maybe, needs more nap time",
                           "Answer hidden in the litter box"],
                'default': ["*tail flick* Try again with fishier question",
                           "Napping engine engaged... Zzz"]
            }
        }
        
    def generate_response(self, input_text):
        if '?' in input_text:
            category = 'question'
        elif any(greet in input_text.lower() for greet in ['hi', 'hello', 'hey']):
            category = 'hello'
        else:
            category = 'default'
        return random.choice(self.knowledge['responses'][category])

class CatSeekGUI:
    def __init__(self, master):
        self.master = master
        master.title("CATSEEK R1")
        master.geometry("800x500")
        master.resizable(False, False)
        master.configure(bg="#FFFFFF")

        # Custom font setup
        self.base_font = font.Font(family="Segoe UI", size=12)
        self.title_font = font.Font(family="Segoe UI", size=14, weight="bold")

        # Create main layout containers
        self.sidebar_frame = tk.Frame(master, width=200, bg="#F5F5F5")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.main_frame = tk.Frame(master, bg="#FFFFFF")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configure sidebar
        self._create_sidebar()
        
        # Main chat components
        self._create_header()
        self._create_chat_display()
        self._create_input_box()

        self.mind = CatMind()
        self.imagination_running = False
        self.typing_animation = None

        # Add initial bot message
        self._show_message("Hi I'm Catseek. How can I help you today?", "bot")

    def _create_sidebar(self):
        """Create left sidebar with navigation options"""
        tk.Button(self.sidebar_frame, text="+ New Chat", font=self.base_font,
                bg="#F5F5F5", fg="#444444", relief=tk.FLAT, bd=0).pack(pady=10, padx=10, fill=tk.X)
        
        ttk.Separator(self.sidebar_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
        
        history_frame = tk.Frame(self.sidebar_frame, bg="#F5F5F5")
        history_frame.pack(fill=tk.X, padx=10)
        tk.Label(history_frame, text="History", bg="#F5F5F5", fg="#666666", 
                font=self.base_font).pack(anchor=tk.W)

    def _create_header(self):
        """Create top header bar"""
        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF", height=60)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="CATSEEK R1", font=self.title_font,
                bg="#FFFFFF", fg="#1A1A1A").pack(side=tk.LEFT, padx=20)

    def _create_chat_display(self):
        """Create chat display area with message bubbles"""
        self.chat_display = scrolledtext.ScrolledText(
            self.main_frame, wrap=tk.WORD, bg="#FFFFFF", fg="#1A1A1A", 
            font=self.base_font, insertbackground="#1A1A1A",
            relief=tk.FLAT, highlightthickness=0, padx=20, pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure message bubble styles
        self.chat_display.tag_config("user", 
            background="#007BFF", foreground="white",
            lmargin1=400, lmargin2=400, rmargin=20,
            spacing1=8, spacing3=8, relief=tk.FLAT,
            borderwidth=0, justify=tk.RIGHT
        )
        self.chat_display.tag_config("bot", 
            background="#F0F0F0", foreground="black",
            rmargin=400, lmargin1=20, lmargin2=20,
            spacing1=8, spacing3=8, relief=tk.FLAT,
            borderwidth=0, justify=tk.LEFT
        )

    def _create_input_box(self):
        """Create bottom input box with modern styling"""
        input_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        self.user_input = ttk.Entry(
            input_frame, font=self.base_font,
            style="Modern.TEntry"
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.user_input.bind("<Return>", lambda e: self.send_message())

        style = ttk.Style()
        style.configure("Modern.TButton", 
            background="#007BFF", foreground="white",
            borderwidth=0, focusthickness=0, focuscolor="#FFFFFF"
        )
        style.map("Modern.TButton",
            background=[("active", "#0069D9"), ("disabled", "#E0E0E0")]
        )

        send_btn = ttk.Button(
            input_frame, text="➤", style="Modern.TButton",
            command=self.send_message, width=3
        )
        send_btn.pack(side=tk.LEFT, padx=(10, 0))

    def send_message(self):
        user_text = self.user_input.get().strip()
        if not user_text:
            return
            
        self._show_message(user_text, "user")
        self.user_input.delete(0, tk.END)
        self._show_typing()
        self.master.after(800, self._generate_response, user_text)

    def _generate_response(self, user_text):
        if self.typing_animation:
            self.master.after_cancel(self.typing_animation)
            self.chat_display.delete("typing")
        response = self.mind.generate_response(user_text)
        self._show_message(response, "bot")

    def _show_typing(self):
        dots = ["", ".", "..", "..."]
        def animate(count=0):
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.delete("typing")
            self.chat_display.insert(tk.END, "\nCat is thinking" + dots[count%4], "bot")
            self.chat_display.tag_add("typing", "end-1c linestart", "end-1c lineend")
            self.chat_display.configure(state=tk.DISABLED)
            self.chat_display.yview(tk.END)
            self.typing_animation = self.master.after(300, animate, count + 1)
        animate()

    def _show_message(self, text, sender):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{text}\n", sender)
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CatSeekGUI(root)
    root.mainloop()
