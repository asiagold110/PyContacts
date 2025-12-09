import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont, filedialog
from tkinter import font
import json
import os
import re
import quopri
import base64

# مسیر فایل تنظیمات
SETTINGS_FILE = "phonebook_settings.json"

# توابع کار با فایل تنظیمات
def load_settings():
    """خواندن تنظیمات از فایل"""
    default_settings = {
        "font_family": "B Homa",
        "font_size": 11
    }
    
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                default_settings.update(settings)
        except:
            pass
    
    return default_settings

def save_settings(settings):
    """ذخیره تنظیمات در فایل"""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در ذخیره تنظیمات: {str(e)}")

# ایجاد پایگاه داده و جدول مخاطبین
def init_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# کلاس اصلی برنامه
class PhoneBookApp:
    # کلاس پنجره افزودن مخاطب
    class AddContactWindow:
        def __init__(self, parent, settings, callback):
            self.parent = parent
            self.settings = settings
            self.callback = callback
            
            # ایجاد پنجره
            self.window = tk.Toplevel(parent)
            self.window.title("➕ افزودن مخاطب جدید")
            self.window.geometry("350x350")
            self.window.resizable(False, False)
            self.window.configure(bg="#f0f0f0")
            
            # تنظیم پنجره به عنوان مودال
            self.window.transient(parent)
            self.window.grab_set()
            
            # ایجاد فریم اصلی
            self.frame = ttk.Frame(self.window, padding="20")
            self.frame.pack(fill=tk.BOTH, expand=True)
            
            # ایجاد ویجت‌ها
            self.create_widgets()
            
            # تنظیم موقعیت پنجره
            self.center_window()
            
            # انتظار برای بستن پنجره
            self.window.wait_window()
        
        def create_widgets(self):
            # نام مخاطب
            ttk.Label(self.frame, text="نام:", font=(self.settings["font_family"], 11)).pack(pady=5)
            self.name_entry = ttk.Entry(self.frame, font=(self.settings["font_family"], 11))
            self.name_entry.pack(fill=tk.X, pady=5)
            self.name_entry.focus_set()
            
            # شماره تلفن
            ttk.Label(self.frame, text="شماره تلفن:", font=(self.settings["font_family"], 11)).pack(pady=5)
            self.phone_entry = ttk.Entry(self.frame, font=(self.settings["font_family"], 11))
            self.phone_entry.pack(fill=tk.X, pady=5)
            
            # دکمه ذخیره
            self.save_button = ttk.Button(self.frame, text="💾 ذخیره", 
                                        command=self.save_contact, 
                                        style="Accent.TButton")
            self.save_button.pack(pady=15)
            
            # دکمه لغو
            self.cancel_button = ttk.Button(self.frame, text="❌ لغو", 
                                         command=self.window.destroy, 
                                         style="Danger.TButton")
            self.cancel_button.pack(pady=5)
            
            # اتصال کلید Enter به دکمه ذخیره
            self.window.bind('<Return>', lambda e: self.save_contact())
        
        def center_window(self):
            self.window.update_idletasks()
            x = (self.window.winfo_screenwidth() // 2) - (350 // 2)
            y = (self.window.winfo_screenheight() // 2) - (250 // 2)
            self.window.geometry(f"350x350+{x}+{y}")
        
        def save_contact(self):
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            
            if not name or not phone:
                messagebox.showwarning("هشدار", "تمامی فیلدها باید پر شوند!", parent=self.window)
                return
            
            try:
                conn = sqlite3.connect('contacts.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
                conn.commit()
                conn.close()
                
                self.callback()  # به‌روزرسانی لیست مخاطبین
                self.window.destroy()
                messagebox.showinfo("موفقیت", "مخاطب با موفقیت اضافه شد!", parent=self.parent)
                
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در ذخیره مخاطب: {str(e)}", parent=self.window)

    # کلاس پنجره ویرایش مخاطب
    class EditContactWindow:
        def __init__(self, parent, settings, callback, contact_data):
            self.parent = parent
            self.settings = settings
            self.callback = callback
            self.contact_data = contact_data  # (id, name, phone)
            
            # ایجاد پنجره
            self.window = tk.Toplevel(parent)
            self.window.title("✏️ ویرایش مخاطب")
            self.window.geometry("350x350")
            self.window.resizable(False, False)
            self.window.configure(bg="#f0f0f0")
            
            # تنظیم پنجره به عنوان مودال
            self.window.transient(parent)
            self.window.grab_set()
            
            # ایجاد فریم اصلی
            self.frame = ttk.Frame(self.window, padding="20")
            self.frame.pack(fill=tk.BOTH, expand=True)
            
            # ایجاد ویجت‌ها
            self.create_widgets()
            
            # تنظیم موقعیت پنجره
            self.center_window()
            
            # انتظار برای بستن پنجره
            self.window.wait_window()
        
        def create_widgets(self):
            # نام مخاطب
            ttk.Label(self.frame, text="نام:", font=(self.settings["font_family"], 11)).pack(pady=5)
            self.name_entry = ttk.Entry(self.frame, font=(self.settings["font_family"], 11))
            self.name_entry.insert(0, self.contact_data[1])
            self.name_entry.pack(fill=tk.X, pady=5)
            self.name_entry.focus_set()
            
            # شماره تلفن
            ttk.Label(self.frame, text="شماره تلفن:", font=(self.settings["font_family"], 11)).pack(pady=5)
            self.phone_entry = ttk.Entry(self.frame, font=(self.settings["font_family"], 11))
            self.phone_entry.insert(0, self.contact_data[2])
            self.phone_entry.pack(fill=tk.X, pady=5)
            
            # دکمه به‌روزرسانی
            self.update_button = ttk.Button(self.frame, text="💾 به‌روزرسانی", 
                                          command=self.update_contact, 
                                          style="Accent.TButton")
            self.update_button.pack(pady=15)
            
            # دکمه لغو
            self.cancel_button = ttk.Button(self.frame, text="❌ لغو", 
                                         command=self.window.destroy, 
                                         style="Danger.TButton")
            self.cancel_button.pack(pady=5)
            
            # اتصال کلید Enter به دکمه به‌روزرسانی
            self.window.bind('<Return>', lambda e: self.update_contact())
        
        def center_window(self):
            self.window.update_idletasks()
            x = (self.window.winfo_screenwidth() // 2) - (350 // 2)
            y = (self.window.winfo_screenheight() // 2) - (250 // 2)
            self.window.geometry(f"350x350+{x}+{y}")
        
        def update_contact(self):
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            
            if not name or not phone:
                messagebox.showwarning("هشدار", "تمامی فیلدها باید پر شوند!", parent=self.window)
                return
            
            try:
                conn = sqlite3.connect('contacts.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", 
                             (name, phone, self.contact_data[0]))
                conn.commit()
                conn.close()
                
                self.callback()  # به‌روزرسانی لیست مخاطبین
                self.window.destroy()
                messagebox.showinfo("موفقیت", "مخاطب با موفقیت ویرایش شد!", parent=self.parent)
                
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در ویرایش مخاطب: {str(e)}", parent=self.window)

    # کلاس پنجره تنظیمات فونت
    class SettingsWindow:
        def __init__(self, parent, settings, callback):
            self.parent = parent
            self.settings = settings
            self.callback = callback
            
            # ایجاد پنجره
            self.window = tk.Toplevel(parent)
            self.window.title("⚙️ تنظیمات فونت")
            self.window.geometry("400x400")
            self.window.resizable(False, False)
            self.window.configure(bg="#f0f0f0")
            
            # تنظیم پنجره به عنوان مودال
            self.window.transient(parent)
            self.window.grab_set()
            
            # ایجاد فریم اصلی
            self.frame = ttk.Frame(self.window, padding="20")
            self.frame.pack(fill=tk.BOTH, expand=True)
            
            # ایجاد ویجت‌ها
            self.create_widgets()
            
            # تنظیم موقعیت پنجره
            self.center_window()
            
            # انتظار برای بستن پنجره
            self.window.wait_window()
        
        def create_widgets(self):
            # لیست فونت‌های موجود
            available_fonts = sorted(tkfont.families())
            
            # نام فونت
            ttk.Label(self.frame, text="نام فونت:", font=(self.settings["font_family"], 11)).pack(pady=5)
            self.font_family_var = tk.StringVar(value=self.settings["font_family"])
            self.font_family_combo = ttk.Combobox(self.frame, textvariable=self.font_family_var, 
                                                values=available_fonts, 
                                                font=(self.settings["font_family"], 11),
                                                state="readonly")
            self.font_family_combo.pack(fill=tk.X, pady=5)

            # اندازه فونت
            ttk.Label(self.frame, text="اندازه فونت:", font=(self.settings["font_family"], 11)).pack(pady=5)
            self.font_size_var = tk.IntVar(value=self.settings["font_size"])
            self.font_size_entry = ttk.Entry(self.frame, textvariable=self.font_size_var, 
                                           font=(self.settings["font_family"], 11))
            self.font_size_entry.pack(fill=tk.X, pady=5)

            # پیش‌نمایش فونت انتخابی
            preview_frame = ttk.Frame(self.frame)
            preview_frame.pack(fill=tk.X, pady=10)
            ttk.Label(preview_frame, text="پیش‌نمایش:", 
                     font=(self.settings["font_family"], 10)).pack(side=tk.RIGHT, padx=(5, 0))
            self.preview_label = ttk.Label(preview_frame, text="این یک متن نمونه است", 
                                         font=(self.settings["font_family"], self.settings["font_size"]))
            self.preview_label.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 5))

            # دکمه اعمال تنظیمات
            self.apply_button = ttk.Button(self.frame, text="✅ اعمال تنظیمات", 
                                         command=self.apply_settings, 
                                         style="Info.TButton")
            self.apply_button.pack(pady=15)
            
            # دکمه لغو
            self.cancel_button = ttk.Button(self.frame, text="❌ لغو", 
                                         command=self.window.destroy, 
                                         style="Danger.TButton")
            self.cancel_button.pack(pady=5)
            
            # اتصال تغییرات به تابع پیش‌نمایش
            self.font_family_var.trace('w', self.update_preview)
            self.font_size_var.trace('w', self.update_preview)
            
            # اتصال کلید Enter به دکمه اعمال
            self.window.bind('<Return>', lambda e: self.apply_settings())
        
        def center_window(self):
            self.window.update_idletasks()
            x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
            y = (self.window.winfo_screenheight() // 2) - (300 // 2)
            self.window.geometry(f"400x400+{x}+{y}")
        
        def update_preview(self, *args):
            try:
                family = self.font_family_var.get()
                size = self.font_size_var.get()
                self.preview_label.configure(text=f"این یک متن نمونه است ({family}, {size})")
                self.preview_label.configure(font=(family, size))
            except:
                pass
        
        def apply_settings(self):
            try:
                new_family = self.font_family_var.get().strip()
                new_size = int(self.font_size_var.get())
                if new_size < 8 or new_size > 24:
                    messagebox.showwarning("هشدار", "اندازه فونت باید بین 8 تا 24 باشد!", parent=self.window)
                    return
                
                # به‌روزرسانی تنظیمات
                self.settings["font_family"] = new_family
                self.settings["font_size"] = new_size
                
                # ذخیره تنظیمات در فایل
                save_settings(self.settings)
                
                # اعمال تنظیمات به برنامه
                self.callback()  # به‌روزرسانی برنامه با تنظیمات جدید
                self.window.destroy()
                messagebox.showinfo("موفقیت", "تنظیمات فونت با موفقیت اعمال شد!", parent=self.parent)
                
            except ValueError:
                messagebox.showerror("خطا", "اندازه فونت باید یک عدد معتبر باشد!", parent=self.window)

    def __init__(self, root):
        self.root = root
        self.root.title("📞 دفترچه تلفن خطیبی")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # بارگذاری تنظیمات
        self.settings = load_settings()
        
        # تنظیم استایل کلی برنامه
        self.setup_styles()
        
        # تنظیم فونت پیش‌فرض برای برنامه بر اساس تنظیمات ذخیره شده
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(family=self.settings["font_family"], 
                                   size=self.settings["font_size"])
        self.root.option_add("*Font", self.default_font)

        # لیست تمام مخاطبین (برای جستجو)
        self.all_contacts = []

        # فریم اصلی
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # عنوان برنامه
        title_label = ttk.Label(self.main_frame, text="📞 دفترچه تلفن خطیبی", 
                              font=(self.settings["font_family"], 16, "bold"))
        title_label.pack(pady=(0, 15))

        # فریم جستجو
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="🔍 جستجو:", font=(self.settings["font_family"], 10)).pack(side=tk.RIGHT, padx=(5, 0))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                     font=(self.settings["font_family"], 10))
        self.search_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 5))
        self.search_var.trace('w', self.filter_contacts)

        # فریم دکمه‌ها
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        # دکمه‌های اصلی
        self.add_btn = ttk.Button(self.button_frame, text="➕ افزودن مخاطب", 
                                 command=self.open_add_window, style="Accent.TButton")
        self.add_btn.pack(side=tk.RIGHT, padx=5)

        self.edit_btn = ttk.Button(self.button_frame, text="✏️ ویرایش مخاطب", 
                                 command=self.open_edit_window, style="Accent.TButton")
        self.edit_btn.pack(side=tk.RIGHT, padx=5)

        self.delete_btn = ttk.Button(self.button_frame, text="❌ حذف مخاطب", 
                                   command=self.delete_contact, style="Danger.TButton")
        self.delete_btn.pack(side=tk.RIGHT, padx=5)

        # دکمه‌های جدید (Backup, Restore, Import VCF)
        self.import_vcf_btn = ttk.Button(self.button_frame, text="📥 وارد کردن VCF", 
                                       command=self.import_vcf, style="Info.TButton")
        self.import_vcf_btn.pack(side=tk.LEFT, padx=5)

        self.restore_btn = ttk.Button(self.button_frame, text="🔄 بازیابی پشتیبان", 
                                    command=self.restore_contacts, style="Info.TButton")
        self.restore_btn.pack(side=tk.LEFT, padx=5)

        self.backup_btn = ttk.Button(self.button_frame, text="💾 پشتیبان‌گیری", 
                                   command=self.backup_contacts, style="Info.TButton")
        self.backup_btn.pack(side=tk.LEFT, padx=5)

        self.settings_btn = ttk.Button(self.button_frame, text="⚙️ تنظیمات فونت", 
                                      command=self.open_settings_window, style="Info.TButton")
        self.settings_btn.pack(side=tk.LEFT, padx=5)

        # فریم جدول
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # اسکرول بار
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # جدول نمایش مخاطبین
        self.tree = ttk.Treeview(table_frame, columns=('id', 'name', 'phone'), 
                               show='headings', yscrollcommand=scrollbar.set,
                               style="Treeview")
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='نام')
        self.tree.heading('phone', text='شماره تلفن')
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('name', width=250, anchor='e')
        self.tree.column('phone', width=250, anchor='e')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # بارگذاری مخاطبین
        self.load_contacts()

    # تنظیم استایل‌های برنامه
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # استایل دکمه‌های اصلی
        style.configure("Accent.TButton", 
                       background="#4CAF50",
                       foreground="white",
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 5))
        style.map("Accent.TButton",
                 background=[('active', '#45a049')])
        
        # استایل دکمه خطر
        style.configure("Danger.TButton",
                       background="#f44336",
                       foreground="white",
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 5))
        style.map("Danger.TButton",
                 background=[('active', '#da190b')])
        
        # استایل دکمه اطلاعات
        style.configure("Info.TButton",
                       background="#2196F3",
                       foreground="white",
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 5))
        style.map("Info.TButton",
                 background=[('active', '#0b7dda')])
        
        # استایل جدول
        style.configure("Treeview",
                       background="#ffffff",
                       foreground="black",
                       rowheight=25,
                       fieldbackground="#ffffff",
                       borderwidth=1,
                       relief="solid")
        style.configure("Treeview.Heading",
                       background="#e1e1e1",
                       foreground="black",
                       relief="raised")
        style.map("Treeview",
                 background=[('selected', '#347083')])
        
        # استایل Entry
        style.configure("TEntry",
                       padding=5,
                       relief="solid",
                       borderwidth=1)
        
        # استایل Combobox
        style.configure("TCombobox",
                       padding=5,
                       relief="solid",
                       borderwidth=1)

    # بارگذاری مخاطبین از دیتابیس
    def load_contacts(self):
        # پاک کردن لیست و جدول
        self.all_contacts = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # خواندن از دیتابیس
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone FROM contacts")
        rows = cursor.fetchall()
        
        # ذخیره در لیست و نمایش در جدول
        for row in rows:
            self.all_contacts.append(row)
            self.tree.insert('', tk.END, values=row)
        
        conn.close()

    # فیلتر کردن مخاطبین بر اساس جستجو
    def filter_contacts(self, *args):
        search_term = self.search_var.get().lower()
        
        # پاک کردن جدول
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # اگر جستجو خالی است، تمام مخاطبین را نمایش بده
        if not search_term:
            for contact in self.all_contacts:
                self.tree.insert('', tk.END, values=contact)
            return
        
        # در غیر این صورت، مخاطبین منطبق با جستجو را نمایش بده
        for contact in self.all_contacts:
            name = str(contact[1]).lower()
            phone = str(contact[2]).lower()
            if search_term in name or search_term in phone:
                self.tree.insert('', tk.END, values=contact)

    # متد باز کردن پنجره افزودن مخاطب
    def open_add_window(self):
        self.AddContactWindow(self.root, self.settings, self.load_contacts)

    # متد باز کردن پنجره ویرایش مخاطب
    def open_edit_window(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("هشدار", "لطفاً یک مخاطب را انتخاب کنید!")
            return

        contact_data = self.tree.item(selected)['values']
        self.EditContactWindow(self.root, self.settings, self.load_contacts, contact_data)

    # متد باز کردن پنجره تنظیمات فونت
    def open_settings_window(self):
        self.SettingsWindow(self.root, self.settings, self.apply_font_settings)

    # متد اعمال تنظیمات فونت
    def apply_font_settings(self):
        # به‌روزرسانی فونت پیش‌فرض برنامه
        self.default_font.configure(family=self.settings["font_family"], 
                                   size=self.settings["font_size"])
        self.root.option_add("*Font", self.default_font)
        
        # به‌روزرسانی لیست مخاطبین
        self.load_contacts()

    # حذف مخاطب
    def delete_contact(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("هشدار", "لطفاً یک مخاطب را انتخاب کنید!")
            return

        contact = self.tree.item(selected)['values']
        if messagebox.askyesno("تأیید حذف", f"آیا از حذف مخاطب زیر مطمئن هستید؟\n\n📛 نام: {contact[1]}\n📞 شماره: {contact[2]}"):
            try:
                conn = sqlite3.connect('contacts.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM contacts WHERE id=?", (contact[0],))
                conn.commit()
                conn.close()
                
                self.load_contacts()
                messagebox.showinfo("موفقیت", "مخاطب با موفقیت حذف شد!")
                
            except Exception as e:
                messagebox.showerror("خطا", f"خطا در حذف مخاطب: {str(e)}")

    # پشتیبان‌گیری از مخاطبین
    def backup_contacts(self):
        # دریافت مسیر ذخیره فایل پشتیبان
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="ذخیره فایل پشتیبان"
        )
        
        if not file_path:
            return
        
        try:
            # خواندن تمام مخاطبین از دیتابیس
            conn = sqlite3.connect('contacts.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, phone FROM contacts")
            contacts = cursor.fetchall()
            conn.close()
            
            # تبدیل به دیکشنری برای ذخیره در JSON
            contacts_data = []
            for contact in contacts:
                contacts_data.append({
                    "name": contact[0],
                    "phone": contact[1]
                })
            
            # ذخیره در فایل JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(contacts_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("موفقیت", f"پشتیبان‌گیری با موفقیت انجام شد!\nمسیر: {file_path}")
        
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در پشتیبان‌گیری: {str(e)}")

    # بازیابی مخاطبین از فایل پشتیبان
    def restore_contacts(self):
        # دریافت مسیر فایل پشتیبان
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="انتخاب فایل پشتیبان"
        )
        
        if not file_path:
            return
        
        try:
            # خواندن فایل JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                contacts_data = json.load(f)
            
            # اتصال به دیتابیس
            conn = sqlite3.connect('contacts.db')
            cursor = conn.cursor()
            
            # شمارنده برای تعداد مخاطبین اضافه شده
            added_count = 0
            
            for contact in contacts_data:
                name = contact.get('name', '').strip()
                phone = contact.get('phone', '').strip()
                
                if name and phone:
                    # بررسی تکراری نبودن شماره تلفن
                    cursor.execute("SELECT id FROM contacts WHERE phone = ?", (phone,))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
                        added_count += 1
            
            conn.commit()
            conn.close()
            
            # به‌روزرسانی لیست مخاطبین
            self.load_contacts()
            
            messagebox.showinfo("موفقیت", f"بازیابی با موفقیت انجام شد!\nتعداد مخاطبین اضافه شده: {added_count}")
        
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در بازیابی: {str(e)}")

    # وارد کردن مخاطبین از فایل VCF - نسخه پیشرفته با تشخیص هوشمند کاراکترهای فارسی
    def import_vcf(self):
        # دریافت مسیر فایل VCF
        file_path = filedialog.askopenfilename(
            filetypes=[("VCF files", "*.vcf"), ("All files", "*.*")],
            title="انتخاب فایل VCF"
        )
        
        if not file_path:
            return
        
        # تابع دیکد کردن QUOTED-PRINTABLE
        def decode_quoted_printable(text):
            try:
                return quopri.decodestring(text.encode('latin-1')).decode('utf-8')
            except:
                return text
        
        # تابع تشخیص و دیکد کردن کاراکترهای فارسی کد شده
        def decode_persian_text(text):
            # الگوی 1: کدهای هگز با خط تیره (مانند D8-B5-D8)
            hex_pattern1 = re.compile(r'[Dd][0-9A-Fa-f]{2}(?:-[Dd][0-9A-Fa-f]{2})*')
            
            # الگوی 2: کدهای هگز بدون جداکننده (مانند D8B5D8)
            hex_pattern2 = re.compile(r'[Dd][0-9A-Fa-f]{2}[Dd][0-9A-Fa-f]{2}(?:[Dd][0-9A-Fa-f]{2})*')
            
            # الگوی 3: کدهای یونیکد با بک‌اسلش (مانند \xd8\xb5\xd8)
            unicode_pattern = re.compile(r'\\x[0-9a-fA-F]{2}(?:\\x[0-9a-fA-F]{2})*')
            
            # الگوی 4: کدهای یونیکد بدون بک‌اسلش (مانند xd8b5xd8)
            unicode_pattern2 = re.compile(r'x[0-9a-fA-F]{2}(?:x[0-9a-fA-F]{2})*')
            
            # تابع تبدیل هگز به کاراکتر
            def hex_to_char(hex_str):
                try:
                    # حذف جداکننده‌ها
                    clean_hex = hex_str.replace('-', '').replace('\\x', '').replace('x', '')
                    # اگر طول زوج باشد
                    if len(clean_hex) % 2 == 0:
                        return bytes.fromhex(clean_hex).decode('utf-8', errors='ignore')
                except:
                    pass
                return hex_str
            
            # اعمال الگوها
            text = hex_pattern1.sub(lambda m: hex_to_char(m.group(0)), text)
            text = hex_pattern2.sub(lambda m: hex_to_char(m.group(0)), text)
            text = unicode_pattern.sub(lambda m: hex_to_char(m.group(0)), text)
            text = unicode_pattern2.sub(lambda m: hex_to_char(m.group(0)), text)
            
            return text
        
        # تابع دیکد کردن متن با توجه به پارامترهای کدگذاری
        def decode_vcf_text(text, params):
            text = text.strip()
            
            # اگر QUOTED-PRINTABLE باشد
            if 'ENCODING=QUOTED-PRINTABLE' in params or 'ENCODING=QUOTED-PRINTABLE' in text:
                decoded = decode_quoted_printable(text)
                # تشخیص و دیکد کردن کاراکترهای فارسی کد شده
                decoded = decode_persian_text(decoded)
                return decoded
            
            # اگر BASE64 باشد
            if 'ENCODING=BASE64' in params or 'ENCODING=B' in params:
                try:
                    decoded = base64.b64decode(text).decode('utf-8')
                    decoded = decode_persian_text(decoded)
                    return decoded
                except:
                    return text
            
            # اگر CHARSET مشخص شده باشد
            charset = 'utf-8'
            if 'CHARSET=' in params:
                for param in params.split(';'):
                    if param.strip().startswith('CHARSET='):
                        charset = param.split('=')[1].strip().lower()
                        break
            
            # تلاش برای دیکد کردن با charset مشخص شده
            try:
                if charset == 'utf-8':
                    # بررسی وجود کاراکترهای کد شده در متن
                    if '=' in text and any(c in text for c in 'D8D9DADBDCDDDEDFE0E1E2E3E4E5E6E7E8E9EAEBECEDEEEFF0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF'):
                        # ممکن است متن ترکیبی از انگلیسی و کدهای QUOTED-PRINTABLE باشد
                        parts = text.split('=')
                        result = parts[0]
                        for i in range(1, len(parts)):
                            if len(parts[i]) >= 2:
                                hex_code = parts[i][:2]
                                try:
                                    char = bytes.fromhex(hex_code).decode('utf-8', errors='ignore')
                                    result += char
                                    result += parts[i][2:]
                                except:
                                    result += '=' + parts[i]
                            else:
                                result += '=' + parts[i]
                        result = decode_persian_text(result)
                        return result
                    else:
                        return decode_persian_text(text)
                elif charset == 'iso-8859-6':
                    decoded = text.encode('iso-8859-6').decode('utf-8', errors='ignore')
                    return decode_persian_text(decoded)
                elif charset == 'windows-1256':
                    decoded = text.encode('windows-1256').decode('utf-8', errors='ignore')
                    return decode_persian_text(decoded)
                else:
                    return decode_persian_text(text)
            except:
                return decode_persian_text(text)
        
        # تابع استخراج نام از فیلدهای مختلف
        def extract_name_from_card(lines):
            name = ""
            
            for line in lines:
                line = line.strip()
                
                # استخراج نام (FN) با پشتیبانی از فرمت‌های مختلف
                if line.startswith('FN') or line.startswith('fn'):
                    if ':' in line:
                        parts = line.split(':', 1)
                        params = parts[0]
                        value = parts[1]
                        
                        # دیکد کردن مقدار
                        decoded_name = decode_vcf_text(value, params)
                        
                        # اگر نام خالی بود، از پارامترها استفاده کن
                        if not decoded_name and ';' in params:
                            name_parts = params.split(';')
                            for part in name_parts[1:]:
                                if '=' not in part and part:
                                    decoded_name = part
                                    break
                        
                        if decoded_name:
                            name = decoded_name
                            break
                
                # استخراج نام از فیلد N (نام خانوادگی)
                elif line.startswith('N:') or line.startswith('n:'):
                    if not name and ':' in line:
                        parts = line.split(':', 1)
                        params = parts[0]
                        value = parts[1]
                        
                        # دیکد کردن مقدار
                        decoded_value = decode_vcf_text(value, params)
                        
                        # فرمت N معمولاً به صورت: خانوادگی;نام;میانام;پیشوند;پسوند
                        name_parts = decoded_value.split(';')
                        if len(name_parts) >= 2:
                            first_name = name_parts[1].strip()
                            last_name = name_parts[0].strip()
                            if first_name and last_name:
                                name = f"{first_name} {last_name}"
                            elif first_name:
                                name = first_name
                            elif last_name:
                                name = last_name
                            break
                
                # استخراج نام از فیلد ORG (سازمان)
                elif line.startswith('ORG:') or line.startswith('org:'):
                    if not name and ':' in line:
                        parts = line.split(':', 1)
                        params = parts[0]
                        value = parts[1]
                        
                        # دیکد کردن مقدار
                        name = decode_vcf_text(value, params)
                        break
            
            return name
        
        try:
            # تلاش برای خواندن فایل با کدینگ‌های مختلف
            content = None
            encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'windows-1256', 'iso-8859-6']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                messagebox.showerror("خطا", "نمی‌توان فایل VCF را با کدینگ‌های رایج بخواند!")
                return
            
            # تقسیم محتوا به کارت‌های جداگانه
            vcf_cards = content.split('BEGIN:VCARD')
            
            # اتصال به دیتابیس
            conn = sqlite3.connect('contacts.db')
            cursor = conn.cursor()
            
            # شمارنده برای تعداد مخاطبین اضافه شده
            added_count = 0
            skipped_count = 0
            
            for card in vcf_cards:
                if not card.strip():
                    continue
                
                # استخراج نام و شماره تلفن
                name = ""
                phone = ""
                
                # تقسیم کارت به خطوط
                lines = card.strip().split('\n')
                
                # پردازش خطوط چند بخشی (خطوطی که با فاصله شروع می‌شوند)
                processed_lines = []
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if line and not line.startswith(' ') and i + 1 < len(lines) and lines[i+1].startswith(' '):
                        # خط چند بخشی
                        full_line = line
                        i += 1
                        while i < len(lines) and lines[i].startswith(' '):
                            full_line += lines[i].strip()
                            i += 1
                        processed_lines.append(full_line)
                    else:
                        processed_lines.append(line)
                        i += 1
                
                # استخراج نام
                name = extract_name_from_card(processed_lines)
                
                # استخراج شماره تلفن
                for line in processed_lines:
                    line = line.strip()
                    
                    if line.startswith('TEL') or line.startswith('tel'):
                        if ':' in line:
                            parts = line.split(':', 1)
                            params = parts[0]
                            value = parts[1]
                            
                            # دیکد کردن مقدار
                            decoded_value = decode_vcf_text(value, params)
                            
                            # پاک‌سازی شماره تلفن از کاراکترهای غیرضروری
                            phone = re.sub(r'[^\d+]', '', decoded_value.strip())
                            break
                
                # اگر هنوز نام پیدا نشد، از شماره تلفن به عنوان نام استفاده کن
                if not name and phone:
                    name = f"مخاطب {phone[-7:]}"  # 7 رقم آخر شماره
                
                # اگر نام و شماره تلفن وجود داشت
                if name and phone:
                    # بررسی تکراری نبودن شماره تلفن
                    cursor.execute("SELECT id FROM contacts WHERE phone = ?", (phone,))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
                        added_count += 1
                    else:
                        skipped_count += 1
            
            conn.commit()
            conn.close()
            
            # به‌روزرسانی لیست مخاطبین
            self.load_contacts()
            
            # نمایش پیام نتیجه
            message = f"وارد کردن مخاطبین با موفقیت انجام شد!\n\n"
            message += f"✅ تعداد مخاطبین اضافه شده: {added_count}\n"
            if skipped_count > 0:
                message += f"⚠️ تعداد مخاطبین تکراری (وارد نشد): {skipped_count}"
            
            messagebox.showinfo("موفقیت", message)
        
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در وارد کردن فایل VCF: {str(e)}")

# اجرای برنامه
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = PhoneBookApp(root)
    root.mainloop()