import tkinter as tk
import pyperclip
from deep_translator import GoogleTranslator
import json
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
from bs4 import BeautifulSoup
from tkinter import filedialog

class TranscriptViewer:
   def __init__(self, root):
       self.root = root
       self.root.title("Transcript Viewer")
       self.root.geometry("1200x800")
       
       self.theme = {
           'bg': '#1e1e1e',
           'text_bg': '#1e1e1e', 
           'translation_bg': '#1e1e1e',
           'fg': '#e0e0e0',
           'button_bg': '#3d8f40',
           'button_fg': 'white'
       }
       
       self.translator = GoogleTranslator(source='en', target='tr')
       self.is_translated = False
       self.original_text = ""
       self.save_file = 'transcript_data.json'
       self.executor = ThreadPoolExecutor(max_workers=1)
       self.translation_in_progress = False
       
       self.setup_ui()
       self.current_index = self.load_position()
       self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
       self.bind_shortcuts()

   def show_url_dialog(self):
       file_path = filedialog.askopenfilename(
           title="Select HTML File",
           filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
       )
       if file_path:
           self.load_transcript_from_url(file_path)

   def load_transcript_from_url(self, html_path):
       try:
           with open(html_path, 'r', encoding='utf-8') as file:
               html_content = file.read()
           
           soup = BeautifulSoup(html_content, 'html.parser')
           script = soup.find(id="script")
           
           self.lines = []
           if script:
               lines = script.get_text().split('\n')
               for line in lines:
                   line = line.strip()
                   if line and not line.startswith('END') and not line.startswith('ACT'):
                       self.lines.append(line)
           
           self.save_position()
           self.show_current()
           
       except Exception as e:
           self.lines = [f"Error loading transcript: {e}"]
           self.show_current()

   def setup_ui(self):
       self.main_container = tk.Frame(self.root, padx=20, pady=0, bg=self.theme['bg'])
       self.main_container.pack(fill=tk.BOTH, expand=True)

       self.text_frame = tk.Frame(self.main_container, bg=self.theme['bg'])
       self.text_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

       self.text_area = tk.Text(self.text_frame,
                             font=('Arial', 28),
                             wrap=tk.WORD,
                             height=8,
                             bg=self.theme['text_bg'],
                             fg=self.theme['fg'],
                             relief=tk.FLAT,
                             padx=20,
                             pady=10,
                             state='disabled')
       self.text_area.tag_configure("center", justify='center')
       self.text_area.pack(fill=tk.BOTH, expand=True, padx=40)

       self.translation_area = tk.Text(self.text_frame,
                                   font=('Arial', 28),
                                   wrap=tk.WORD,
                                   height=8,
                                   bg=self.theme['translation_bg'],
                                   fg=self.theme['fg'],
                                   relief=tk.FLAT,
                                   padx=20,
                                   pady=10,
                                   state='disabled')
       self.translation_area.tag_configure("center", justify='center')
       
       self.setup_buttons()

       self.counter_label = tk.Label(self.main_container,
                                 text="0/0",
                                 font=('Arial', 14),
                                 bg=self.theme['bg'],
                                 fg=self.theme['fg'])
       self.counter_label.pack(pady=(10, 0))

   def setup_buttons(self):
       self.button_frame = tk.Frame(self.main_container, bg=self.theme['bg'])
       self.button_frame.pack(pady=(20, 0))

       button_style = {
           'font': ('Arial', 14),
           'width': 15,
           'height': 2,
           'bg': self.theme['button_bg'],
           'fg': self.theme['button_fg'],
           'relief': 'raised'
       }

       self.prev_button = tk.Button(self.button_frame, text="◀ Previous", command=self.show_previous, **button_style)
       self.next_button = tk.Button(self.button_frame, text="Next ▶", command=self.show_next, **button_style)
       self.copy_button = tk.Button(self.button_frame, text="📋 Copy", command=self.copy_text, **button_style)
       self.translate_button = tk.Button(self.button_frame, text="🌐 Translate", command=self.toggle_translation, **button_style)
       self.load_url_button = tk.Button(self.button_frame, text="Load File", command=self.show_url_dialog, **button_style)

       self.goto_entry = tk.Entry(self.button_frame, width=5, font=('Arial', 14), justify='center')
       self.goto_button = tk.Button(self.button_frame, text="Go", command=self.goto_position, **button_style)

       for widget in [self.prev_button, self.next_button, self.copy_button,
                   self.translate_button, self.load_url_button,
                   self.goto_entry, self.goto_button]:
           widget.pack(side=tk.LEFT, padx=10)

   async def translate_text(self, text):
       if self.translation_in_progress:
           return
           
       self.translation_in_progress = True
       self.translate_button.config(state='disabled')
       
       try:
           if ':' not in text:
               translated = await asyncio.get_event_loop().run_in_executor(
                   self.executor,
                   lambda: self.translator.translate(text)
               )
           else:
               speaker, content = text.split(':', 1)
               translated_content = await asyncio.get_event_loop().run_in_executor(
                   self.executor,
                   lambda: self.translator.translate(content.strip())
               )
               translated = f"{speaker}: {translated_content}"
           
           if self.translation_area.winfo_ismapped():
               self.translation_area.config(state='normal')
               self.translation_area.delete(1.0, tk.END)
               self.translation_area.insert(1.0, translated)
               self.translation_area.tag_add("center", "1.0", "end")
               self.translation_area.config(state='disabled')
           
       except Exception as e:
           if self.translation_area.winfo_ismapped():
               self.translation_area.config(state='normal')
               self.translation_area.delete(1.0, tk.END)
               self.translation_area.insert(1.0, f"Translation failed: {str(e)}")
               self.translation_area.tag_add("center", "1.0", "end")
               self.translation_area.config(state='disabled')
       
       finally:
           self.translation_in_progress = False
           self.translate_button.config(state='normal')

   def start_translation(self):
       if not hasattr(self, 'loop'):
           self.loop = asyncio.new_event_loop()
           asyncio.set_event_loop(self.loop)
       
       self.translation_area.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 0))
       self.is_translated = True
       
       self.translation_area.config(state='normal')
       self.translation_area.delete(1.0, tk.END)
       self.translation_area.config(state='disabled')
       
       threading.Thread(target=self._run_translation, daemon=True).start()

   def _run_translation(self):
       asyncio.run(self.translate_text(self.original_text))

   def toggle_translation(self):
       if not self.is_translated:
           self.start_translation()
       else:
           self.translation_area.pack_forget()
           self.is_translated = False
           self.translation_in_progress = False
       self.translate_button.config(text="🌐 Hide" if self.is_translated else "🌐 Translate")

   def bind_shortcuts(self):
       self.root.bind('<Left>', lambda e: self.show_previous())
       self.root.bind('<Right>', lambda e: self.show_next())
       self.root.bind('<Control-c>', lambda e: self.copy_text())
       self.root.bind('<c>', lambda e: self.toggle_translation())
       self.root.bind('<C>', lambda e: self.toggle_translation())
       self.root.bind('<">', lambda e: self.toggle_translation())
       self.root.bind('<Return>', lambda e: self.goto_position())

   def goto_position(self):
       try:
           pos = int(self.goto_entry.get())
           if 1 <= pos <= len(self.lines):
               self.current_index = pos - 1
               self.is_translated = False
               self.translation_area.pack_forget()
               self.translate_button.config(text="🌐 Translate")
               self.show_current()
               self.save_position()
           self.goto_entry.delete(0, tk.END)
       except ValueError:
           pass

   def load_position(self):
       try:
           if os.path.exists(self.save_file):
               with open(self.save_file, 'r', encoding='utf-8') as f:
                   data = json.load(f)
                   self.lines = data.get('lines', [])
                   position = data.get('position', 0)
                   if self.lines:
                       self.current_index = position
                       self.show_current()
                   return position
           return 0
       except:
           return 0

   def save_position(self):
       try:
           data = {
               'position': self.current_index,
               'lines': self.lines if hasattr(self, 'lines') else []
           }
           with open(self.save_file, 'w', encoding='utf-8') as f:
               json.dump(data, f, ensure_ascii=False)
       except:
           pass

   def on_closing(self):
       self.save_position()
       if hasattr(self, 'executor'):
           self.executor.shutdown(wait=False)
       self.root.destroy()

   def show_current(self):
       if hasattr(self, 'lines') and 0 <= self.current_index < len(self.lines):
           self.text_area.config(state='normal')
           self.text_area.delete(1.0, tk.END)
           current_text = self.lines[self.current_index]
           self.original_text = current_text
           self.text_area.insert(1.0, current_text)
           self.text_area.tag_add("center", "1.0", "end")
           self.text_area.config(state='disabled')
           
           self.translation_area.pack_forget()
           self.is_translated = False
           self.translate_button.config(text="🌐 Translate")
           
           self.update_counter()

   def copy_text(self):
       text = self.text_area.get(1.0, tk.END).strip()
       if text:
           pyperclip.copy(text)

   def show_next(self):
       if hasattr(self, 'lines') and self.current_index < len(self.lines) - 1:
           self.current_index += 1
           self.show_current()
           self.save_position()

   def show_previous(self):
       if hasattr(self, 'lines') and self.current_index > 0:
           self.current_index -= 1
           self.show_current()
           self.save_position()

   def update_counter(self):
       if hasattr(self, 'lines'):
           self.counter_label.config(text=f"{self.current_index + 1}/{len(self.lines)}")

if __name__ == "__main__":
   root = tk.Tk()
   root.configure(bg='#1e1e1e')
   app = TranscriptViewer(root)
   root.mainloop()