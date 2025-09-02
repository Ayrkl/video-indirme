import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pytubefix import YouTube
import subprocess
import os
import pyperclip
import threading
from datetime import datetime

# Ana pencere
root = tk.Tk()
root.title("YouTube Downloader PRO")
root.geometry("700x600")

# Varsayılan indirme klasörü
indirilecek_klasor = r"C:\Users\ayure\Desktop\video indirme\videolar"
gecmis_dosyasi = os.path.join(indirilecek_klasor, "gecmis.txt")
log_dosyasi = os.path.join(indirilecek_klasor, "log.txt")

if not os.path.exists(gecmis_dosyasi):
    open(gecmis_dosyasi, "w").close()
if not os.path.exists(log_dosyasi):
    open(log_dosyasi, "w").close()

# Fonksiyonlar
def klasor_sec():
    global indirilecek_klasor
    secilen = filedialog.askdirectory()
    if secilen:
        indirilecek_klasor = secilen
        klasor_label.config(text=f"İndirilecek Klasör: {indirilecek_klasor}")

def temiz_baslik(baslik):
    for char in r'\/:*?"<>|':
        baslik = baslik.replace(char, "_")
    return baslik[:70]  # path limit için kısalttık

def cikis_dosyasi_uret(baslik, klasor):
    base_path = os.path.join(klasor, f"{baslik}.mp4")
    if not os.path.exists(base_path):
        return base_path

    i = 1
    while True:
        new_path = os.path.join(klasor, f"{baslik} ({i}).mp4")
        if not os.path.exists(new_path):
            return new_path
        i += 1

def mod_degistir():
    if mod_var.get() == "tekli":
        text_frame.pack_forget()
        entry_frame.pack(pady=5)
    else:
        entry_frame.pack_forget()
        text_frame.pack(pady=5)

def tema_degistir():
    if tema_var.get() == "dark":
        bg_color = "#2e2e2e"
        fg_color = "white"
        btn_bg = "#555555"
        entry_bg = "#4d4d4d"
    else:
        bg_color = "white"
        fg_color = "black"
        btn_bg = "#e0e0e0"
        entry_bg = "white"

    root.config(bg=bg_color)
    for widget in root.winfo_children():
        try:
            widget.config(bg=bg_color, fg=fg_color)
        except:
            pass
    for frame in [entry_frame, text_frame, tema_frame]:
        frame.config(bg=bg_color)
        for widget in frame.winfo_children():
            try:
                widget.config(bg=entry_bg, fg=fg_color)
            except:
                pass
    klasor_btn.config(bg=btn_bg, fg=fg_color)
    indir_btn.config(bg="green", fg="white")
    klasor_label.config(bg=bg_color, fg=fg_color)

# İndirme fonksiyonu (tek video)
def indir_video_thread(url, progress):
    try:
        with open(gecmis_dosyasi, "r") as f:
            gecmis = f.read().splitlines()
        if url in gecmis:
            return

        yt = YouTube(url)
        video_stream = yt.streams.filter(file_extension='mp4', progressive=False).order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if not video_stream or not audio_stream:
            messagebox.showerror("Hata", f"Video veya ses bulunamadı:\n{url}")
            return

        # Otomatik klasör: tarih/kanal adı
        tarih = datetime.now().strftime("%Y-%m-%d")
        kanal = temiz_baslik(yt.author)
        hedef_klasor = os.path.join(indirilecek_klasor, tarih, kanal)
        os.makedirs(hedef_klasor, exist_ok=True)

        video_path = os.path.join(hedef_klasor, "video_temp.mp4")
        audio_path = os.path.join(hedef_klasor, "audio_temp.mp4")
        output_path = cikis_dosyasi_uret(temiz_baslik(yt.title), hedef_klasor)

        video_stream.download(output_path=hedef_klasor, filename="video_temp.mp4")
        audio_stream.download(output_path=hedef_klasor, filename="audio_temp.mp4")

        command = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            output_path
        ]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove(video_path)
        os.remove(audio_path)

        # Geçmişe ekle
        with open(gecmis_dosyasi, "a") as f:
            f.write(url + "\n")

        # Log kaydı
        with open(log_dosyasi, "a", encoding="utf-8") as log:
            log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {yt.title} | {video_stream.resolution} | {url}\n")

        # Progress güncelle
        progress['value'] += 100 / max(len(urls_global), 1)

    except Exception as e:
        messagebox.showerror("Hata", f"{url} | {e}")

# Çoklu indirme (paralel)
def indir_video():
    global urls_global
    mod = mod_var.get()
    if mod == "tekli":
        urls_global = [url_entry.get().strip()]
    else:
        urls_global = url_text.get("1.0", tk.END).strip().splitlines()

    if not urls_global:
        messagebox.showerror("Hata", "Lütfen URL girin!")
        return

    # Progressbar oluştur
    progress['value'] = 0
    progress.pack(pady=5)

    threads = []
    for url in urls_global:
        url = url.strip()
        if url:
            t = threading.Thread(target=indir_video_thread, args=(url, progress))
            t.start()
            threads.append(t)

    # Threadleri GUI donmadan bekletme
    def kontrol_threads():
        if any(t.is_alive() for t in threads):
            root.after(500, kontrol_threads)
        else:
            progress.pack_forget()
            messagebox.showinfo("Tamamlandı", "Videolar başarıyla indirildi!")

    kontrol_threads()

# Clipboard otomatik ekleme
eski_pano = ""
def clipboard_kontrol():
    global eski_pano
    try:
        pano = pyperclip.paste()
        if pano != eski_pano and pano.startswith("https://"):
            url_text.insert(tk.END, pano + "\n")
            url_text.see(tk.END)
            eski_pano = pano
    except:
        pass
    root.after(1000, clipboard_kontrol)  # 1 saniye aralık

# Arayüz
tk.Label(root, text="YouTube URL'lerini gir:", font=("Arial", 12)).pack(pady=10)

mod_var = tk.StringVar(value="tekli")
tk.Radiobutton(root, text="Tekli İndir", variable=mod_var, value="tekli", command=mod_degistir).pack()
tk.Radiobutton(root, text="Çoklu İndir", variable=mod_var, value="coklu", command=mod_degistir).pack()

# Tekli Entry widget
entry_frame = tk.Frame(root)
url_entry = tk.Entry(entry_frame, width=70)
url_entry.pack()

# Çoklu Text widget
text_frame = tk.Frame(root)
url_text = tk.Text(text_frame, width=70, height=10)
url_text.pack()

entry_frame.pack(pady=5)

# Tema seçim radiobuttonları
tema_var = tk.StringVar(value="white")
tema_frame = tk.Frame(root)
tk.Label(tema_frame, text="Tema:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(tema_frame, text="White", variable=tema_var, value="white", command=tema_degistir).pack(side=tk.LEFT)
tk.Radiobutton(tema_frame, text="Dark", variable=tema_var, value="dark", command=tema_degistir).pack(side=tk.LEFT)
tema_frame.pack(pady=5)

klasor_btn = tk.Button(root, text="Klasör Seç", command=klasor_sec, bg="blue", fg="white", font=("Arial", 12))
klasor_btn.pack(pady=5)

klasor_label = tk.Label(root, text=f"İndirilecek Klasör: {indirilecek_klasor}", font=("Arial", 10))
klasor_label.pack(pady=5)

indir_btn = tk.Button(root, text="İndir", command=indir_video, bg="green", fg="white", font=("Arial", 12))
indir_btn.pack(pady=10)

# Progressbar
progress = ttk.Progressbar(root, length=600, mode='determinate')

# Başlangıç tema ve clipboard kontrolü
tema_degistir()
clipboard_kontrol()
root.mainloop()
