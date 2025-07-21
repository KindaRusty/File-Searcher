import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import ctypes
from pathlib import Path
import threading
import queue

def check_and_install_dependencies():
    required_packages = {
        'docx': 'python-docx',
        'fitz': 'PyMuPDF',
        'pytesseract': 'pytesseract',
        'PIL': 'Pillow'
    }
    
    print(">>> Checking required Python libraries...")
    missing_packages = []
    for import_name, install_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  [OK] '{install_name}' is already installed.")
        except ImportError:
            print(f"  [!] '{install_name}' is missing.")
            missing_packages.append(install_name)
    
    if missing_packages:
        print(f"\n>>> Attempting to install {len(missing_packages)} missing packages using pip...")
        for package in missing_packages:
            try:
                print(f"    -> Installing '{package}'...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"    -> Successfully installed '{package}'.")
            except subprocess.CalledProcessError:
                print(f"    [ERROR] Failed to install '{package}'. Please install it manually.")
                messagebox.showerror(
                    "Installation Error",
                    f"Failed to install '{package}'.\nPlease run 'pip install {package}' in your terminal."
                )
                sys.exit(1)
        print("\n>>> All required libraries are now installed.")
    else:
        print(">>> All libraries are present.")

try:
    check_and_install_dependencies()
    import docx
    import fitz
    import pytesseract
    from PIL import Image
    LIBS_LOADED = True
except Exception as e:
    messagebox.showerror("Error", f"An error occurred during library setup: {e}")
    LIBS_LOADED = False

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

LANGUAGES = {
    'vi': {
        'title': "Công cụ Tìm kiếm File (Phiên bản Ổn định)",
        'folder_frame_label': "1. Chọn thư mục để tìm kiếm",
        'browse_button': "Chọn Thư Mục...",
        'phrase_frame_label': "2. Nhập cụm từ cần tìm",
        'ext_frame_label': "3. Chọn loại file để tìm kiếm",
        'run_button': "Bắt đầu Tìm kiếm",
        'reset_button': "Làm lại",
        'results_frame_label': "Kết quả tìm kiếm",
        'libs_warning_title': "!!! CẢNH BÁO:",
        'libs_warning_msg1': "Một số thư viện (docx, fitz, pytesseract) chưa được cài đặt.",
        'libs_warning_msg2': "Chức năng tìm kiếm trong file .docx, .pdf, và ảnh sẽ không hoạt động.",
        'error_title': "Lỗi",
        'warning_title': "Cảnh báo",
        'info_title': "Thông báo",
        'invalid_path_error': "Đường dẫn thư mục không hợp lệ.",
        'missing_phrase_error': "Bạn chưa nhập cụm từ để tìm kiếm.",
        'missing_ext_error': "Bạn chưa chọn loại file để tìm kiếm.",
        'search_start_msg': "--- Bắt đầu tìm kiếm '{phrase}' trong: {folder_path} ---",
        'scan_types_msg': "Các loại file sẽ được quét: {exts}",
        'found_in_msg': "  [OK] Tìm thấy trong: {file}",
        'found_in_line_msg': "     -> Dòng {line_num}: {line}",
        'fatal_error_msg': "!!! LỖI NGHIÊM TRỌNG: {e}",
        'search_complete_title': "Hoàn thành",
        'search_complete_msg': "Đã tìm kiếm xong!\n\nTổng số kết quả tìm thấy: {count}",
        'summary_header': "--- HOÀN THÀNH ---",
        'lang_button': "English"
    },
    'en': {
        'title': "File Search Tool (Stable Version)",
        'folder_frame_label': "1. Select a folder to search in",
        'browse_button': "Browse...",
        'phrase_frame_label': "2. Enter the phrase to find",
        'ext_frame_label': "3. Select file types to search",
        'run_button': "Start Search",
        'reset_button': "Reset",
        'results_frame_label': "Search Results",
        'libs_warning_title': "!!! WARNING:",
        'libs_warning_msg1': "Some libraries (docx, fitz, pytesseract) are not installed.",
        'libs_warning_msg2': "Searching in .docx, .pdf, and image files will not work.",
        'error_title': "Error",
        'warning_title': "Warning",
        'info_title': "Information",
        'invalid_path_error': "The selected folder path is invalid.",
        'missing_phrase_error': "Please enter a phrase to search for.",
        'missing_ext_error': "Please select at least one file type to search.",
        'search_start_msg': "--- Starting search for '{phrase}' in: {folder_path} ---",
        'scan_types_msg': "File types to be scanned: {exts}",
        'found_in_msg': "  [OK] Found in: {file}",
        'found_in_line_msg': "     -> Line {line_num}: {line}",
        'fatal_error_msg': "!!! FATAL ERROR: {e}",
        'search_complete_title': "Finished",
        'search_complete_msg': "Search complete!\n\nTotal results found: {count}",
        'summary_header': "--- FINISHED ---",
        'lang_button': "Tiếng Việt"
    }
}

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception: return ""

def extract_text_from_pdf(file_path):
    try:
        with fitz.open(file_path) as doc:
            return "\n".join([page.get_text() for page in doc])
    except Exception: return ""

def extract_text_from_image(file_path):
    try:
        return pytesseract.image_to_string(Image.open(file_path))
    except Exception: return ""

class AdvancedSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("750x600")
        self.root.minsize(600, 500)

        self.source_folder = tk.StringVar()
        self.search_phrase = tk.StringVar()
        self.file_types = {".png": tk.BooleanVar(value=True), ".jpg": tk.BooleanVar(value=True), ".jpeg": tk.BooleanVar(value=True), ".pdf": tk.BooleanVar(value=True), ".docx": tk.BooleanVar(value=True), ".txt": tk.BooleanVar(value=True)}
        self.is_searching = False
        self.current_lang = tk.StringVar(value='vi')

        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, padx=10, pady=(10,0))
        self.lang_button = tk.Button(top_frame, text="", command=self.toggle_language)
        self.lang_button.pack(side=tk.RIGHT)
        
        main_frame = tk.Frame(root, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.folder_frame = tk.LabelFrame(main_frame, text="", padx=10, pady=10, font=('Helvetica', 10, 'bold'))
        self.folder_frame.pack(fill=tk.X, expand=True)
        self.dir_entry = tk.Entry(self.folder_frame, textvariable=self.source_folder, font=('Helvetica', 10))
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self.browse_btn = tk.Button(self.folder_frame, text="", command=self.browse_folder)
        self.browse_btn.pack(side=tk.LEFT, padx=(10, 0))

        self.phrase_frame = tk.LabelFrame(main_frame, text="", padx=10, pady=10, font=('Helvetica', 10, 'bold'))
        self.phrase_frame.pack(fill=tk.X, expand=True, pady=10)
        self.phrase_entry = tk.Entry(self.phrase_frame, textvariable=self.search_phrase, font=('Helvetica', 10))
        self.phrase_entry.pack(fill=tk.X, expand=True, ipady=4)

        self.ext_frame = tk.LabelFrame(main_frame, text="", padx=10, pady=10, font=('Helvetica', 10, 'bold'))
        self.ext_frame.pack(fill=tk.X, expand=True)
        self.check_buttons = {}
        col = 0
        for ext, var in self.file_types.items():
            cb = tk.Checkbutton(self.ext_frame, text=ext.upper(), variable=var, onvalue=True, offvalue=False)
            cb.grid(row=0, column=col, padx=5, sticky='w'); col += 1
            self.check_buttons[ext] = cb
            
        action_frame = tk.Frame(main_frame)
        action_frame.pack(fill=tk.X, expand=True, pady=10)
        self.run_button = tk.Button(action_frame, text="", command=self.start_search, font=('Helvetica', 11, 'bold'), bg="#007ACC", fg="white")
        self.run_button.pack(side=tk.LEFT, ipady=5, ipadx=10)
        self.reset_button = tk.Button(action_frame, text="", command=self.reset, font=('Helvetica', 11, 'bold'), bg="#c0392b", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=(10, 0), ipady=5, ipadx=10)

        self.results_frame = tk.LabelFrame(main_frame, text="", padx=10, pady=10, font=('Helvetica', 10, 'bold'))
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.results_text = scrolledtext.ScrolledText(self.results_frame, wrap=tk.WORD, state='disabled', font=('Courier New', 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        self.update_ui_text()
        
        if not LIBS_LOADED:
            texts = LANGUAGES[self.current_lang.get()]
            self.log(f"{texts['libs_warning_title']} {texts['libs_warning_msg1']}")
            self.log(f"-> {texts['libs_warning_msg2']}")

    def update_ui_text(self):
        lang_code = self.current_lang.get()
        texts = LANGUAGES[lang_code]
        self.root.title(texts['title'])
        self.folder_frame.config(text=texts['folder_frame_label'])
        self.browse_btn.config(text=texts['browse_button'])
        self.phrase_frame.config(text=texts['phrase_frame_label'])
        self.ext_frame.config(text=texts['ext_frame_label'])
        self.run_button.config(text=texts['run_button'])
        self.reset_button.config(text=texts['reset_button'])
        self.results_frame.config(text=texts['results_frame_label'])
        self.lang_button.config(text=texts['lang_button'])
        
    def toggle_language(self):
        new_lang = 'en' if self.current_lang.get() == 'vi' else 'vi'
        self.current_lang.set(new_lang)
        self.update_ui_text()

    def log(self, message):
        self.results_text.config(state='normal'); self.results_text.insert(tk.END, message + "\n"); self.results_text.config(state='disabled'); self.results_text.see(tk.END)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(title="Select folder")
        if folder_selected: self.source_folder.set(folder_selected)

    def get_selected_extensions(self):
        return [ext for ext, var in self.file_types.items() if var.get()]

    def start_search(self):
        lang_code = self.current_lang.get()
        texts = LANGUAGES[lang_code]
        folder_path = Path(self.source_folder.get())
        phrase = self.search_phrase.get()
        selected_exts = self.get_selected_extensions()
        
        if not folder_path.is_dir(): messagebox.showerror(texts['error_title'], texts['invalid_path_error']); return
        if not phrase: messagebox.showerror(texts['error_title'], texts['missing_phrase_error']); return
        if not selected_exts: messagebox.showwarning(texts['warning_title'], texts['missing_ext_error']); return

        self.run_button.config(state='disabled')
        self.reset_button.config(state='disabled')
        self.results_text.config(state='normal'); self.results_text.delete('1.0', tk.END); self.results_text.config(state='disabled')
        
        self.results_queue = queue.Queue()
        self.is_searching = True
        
        self.search_thread = threading.Thread(target=self.search_worker, args=(folder_path, phrase, selected_exts, self.results_queue, lang_code))
        self.search_thread.start()
        
        self.check_queue()

    def check_queue(self):
        if not self.is_searching: return

        try:
            message = self.results_queue.get_nowait()
            if isinstance(message, tuple) and message[0] == 'FINAL_COUNT':
                self.is_searching = False
                self.run_button.config(state='normal')
                self.reset_button.config(state='normal')
                lang_code = self.current_lang.get()
                texts = LANGUAGES[lang_code]
                self.log("\n" + "="*50)
                self.log(texts['summary_header'])
                messagebox.showinfo(texts['search_complete_title'], texts['search_complete_msg'].format(count=message[1]))
            else:
                self.log(message)
                self.root.after(100, self.check_queue)
        except queue.Empty:
            self.root.after(100, self.check_queue)

    def search_worker(self, folder_path, phrase, selected_exts, q, lang_code):
        texts = LANGUAGES[lang_code]
        q.put(texts['search_start_msg'].format(phrase=phrase, folder_path=folder_path))
        q.put(texts['scan_types_msg'].format(exts=', '.join(selected_exts)))
        
        found_count = 0
        try:
            for file in folder_path.rglob('*'):
                if not self.is_searching: break
                if file.is_file() and file.suffix.lower() in selected_exts:
                    file_ext = file.suffix.lower()
                    if file_ext == '.txt':
                        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, line in enumerate(f, 1):
                                if phrase in line:
                                    q.put(texts['found_in_msg'].format(file=file))
                                    q.put(texts['found_in_line_msg'].format(line_num=line_num, line=line.strip()))
                                    found_count += 1
                        continue
                    
                    extracted_text = ""
                    if LIBS_LOADED:
                        if file_ext == '.docx': extracted_text = extract_text_from_docx(file)
                        elif file_ext == '.pdf': extracted_text = extract_text_from_pdf(file)
                        elif file_ext in ['.png', '.jpg', '.jpeg']: extracted_text = extract_text_from_image(file)
                    
                    if phrase in extracted_text:
                        q.put(texts['found_in_msg'].format(file=file))
                        found_count += 1
        except Exception as e:
            q.put(texts['fatal_error_msg'].format(e=e))
        
        q.put(('FINAL_COUNT', found_count))

    def reset(self):
        self.is_searching = False 
        self.source_folder.set(""); self.search_phrase.set("")
        self.results_text.config(state='normal'); self.results_text.delete('1.0', tk.END); self.results_text.config(state='disabled')
        for var in self.file_types.values(): var.set(True)
        self.run_button.config(state='normal')
        self.reset_button.config(state='normal')

if __name__ == '__main__':
    if LIBS_LOADED is not False:
        root = tk.Tk()
        app = AdvancedSearchApp(root)
        root.mainloop()
    else:
        print("Could not start the application due to missing critical libraries.")

def main():
    """Hàm chính để khởi chạy ứng dụng."""
    # Đoạn này trước đây nằm trong if __name__ == '__main__':
    root = tk.Tk()
    app = AdvancedSearchApp(root)
    root.mainloop()

if __name__ == '__main__':
    # Gọi hàm main để chạy ứng dụng khi thực thi trực tiếp
    main()