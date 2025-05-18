# tset.py - CATSEEK R1 GUI Core
import tkinter as tk
from tkinter import scrolledtext, font
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
        master.geometry("600x400")
        master.resizable(False, False)
        master.configure(bg="#1A1D27")

        # Custom font setup
        self.base_font = font.Font(family="Segoe UI", size=10)
        self.title_font = font.Font(family="Segoe UI", size=14, weight="bold")

        # Header
        header_frame = tk.Frame(master, bg="#1A1D27", height=50)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="🐱 CATSEEK R1", font=self.title_font, 
                bg="#1A1D27", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Frame(master, height=2, bg="#2D2F3B").pack(fill=tk.X)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            master, wrap=tk.WORD, bg="#1A1D27", fg="white", 
            font=self.base_font, insertbackground="white",
            relief=tk.FLAT, highlightthickness=0
        )
        self.chat_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.tag_config("user", foreground="#7BC0F8")
        self.chat_display.tag_config("bot", foreground="#C3D1DD")
        self.chat_display.tag_config("timestamp", foreground="#6B7280")

        # Input area
        input_frame = tk.Frame(master, bg="#2D2F3B", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.user_input = tk.Entry(
            input_frame, bg="#2D2F3B", fg="white", 
            insertbackground="white", relief=tk.FLAT,
            font=self.base_font
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3)
        self.user_input.bind("<Return>", lambda e: self.send_message())
        
        send_btn = tk.Button(
            input_frame, text="➤", command=self.send_message,
            bg="#7BC0F8", fg="#1A1D27", relief=tk.FLAT,
            font=font.Font(size=12), width=2
        )
        send_btn.pack(side=tk.LEFT, padx=(10,0))

        self.mind = CatMind()
        self.imagination_running = False
        self.typing_animation = None

    def send_message(self):
        user_text = self.user_input.get().strip()
        if not user_text:
            return
            
        self._show_message(user_text, "user")
        self.user_input.delete(0, tk.END)
        
        # Show typing indicator
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
            self.chat_display.insert(tk.END, "\nCat is thinking" + dots[count%4], "timestamp")
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

    def start_imagination(self):
        if self.imagination_running:
            return
            
        self.imagination_running = True
        imagine_window = tk.Toplevel(self.master)
        imagine_window.title("Cat Vision Matrix")
        imagine_window.geometry("300x200")
        imagine_window.resizable(False, False)
        imagine_window.configure(bg="#1A1D27")
        
        canvas = tk.Canvas(imagine_window, bg="#1A1D27", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        cat_art = [
            r" /\_/\  ",
            r"( o.o ) ",
            r" > ^ <  "
        ]
        
        def animate(frame=0):
            if not self.imagination_running:
                return
                
            canvas.delete("all")
            y_offset = 50 + int(10 * (1 + (frame % 60)/30))
            for i, line in enumerate(cat_art):
                canvas.create_text(150, y_offset + i*20, 
                                text=line, fill="#7BC0F8",
                                font=("Consolas", 14))
            imagine_window.after(16, animate, frame + 1)
        
        animate()
        imagine_window.protocol("WM_DELETE_WINDOW", 
                              lambda: self._stop_imagination(imagine_window))

    def _stop_imagination(self, window):
        self.imagination_running = False
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CatSeekGUI(root)
    root.mainloop()
