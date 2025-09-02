# YouTube Downloader PRO

Bu program, **Windows üzerinde çalışan bir Python tabanlı YouTube video indiricisidir**.  
Tekli veya çoklu video indirme, paralel indirme, 1080p’ye kadar çözünürlük desteği, tema seçimi ve otomatik klasör düzenleme gibi özellikler sunar.

---

## Özellikler

- **Tekli ve çoklu indirme**: URL’leri tek tek veya çoklu olarak ekleyebilirsiniz.
- **Clipboard izleme**: Kopyaladığınız YouTube URL’leri otomatik olarak eklenir.
- **Paralel indirme**: Birden fazla video aynı anda indirilir, GUI donmaz.
- **Otomatik klasör düzenleme**: Videolar tarih ve kanal adına göre klasörlere kaydedilir.
- **Çözünürlük seçimi**: Varsayılan olarak en yüksek çözünürlük seçilir (720p/1080p).
- **Kopya video isimlendirme**: Aynı video tekrar indirildiğinde `(1)`, `(2)` gibi isimlendirilir.
- **Tema desteği**: White ve Dark tema seçenekleri.
- **Log yönetimi**: İndirilen videolar, tarih, başlık ve çözünürlük bilgisi ile `log.txt` dosyasına kaydedilir.

---

## Gereksinimler

- Python 3.x
- Tkinter (`pip install tk` – genellikle Python ile birlikte gelir)
- PyTubeFix (`pip install pytubefix`)
- Pyperclip (`pip install pyperclip`)
- FFMPEG (komut satırından çalışacak şekilde PATH’e eklenmiş olmalı)

---

## Kullanım

1. Projeyi bilgisayarınıza indirin.
2. Terminal veya VS Code ile programı çalıştırın:
   ```bash
   python youtube_downloader.py
