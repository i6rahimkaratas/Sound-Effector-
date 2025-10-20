import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import soundfile as sf
import sounddevice as sd
from scipy import signal
import threading

class SesEfektUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Ses Efekt Uygulaması")
        self.root.geometry("600x500")
        self.root.configure(bg='#2b2b2b')
        
        self.ses_verisi = None
        self.ornekleme_hizi = None
        self.orijinal_ses = None
        self.dosya_yolu = None
        self.oynatiliyor = False
        
        self.arayuz_olustur()
    
    def arayuz_olustur(self):
        # Başlık
        baslik = tk.Label(self.root, text="🎵 Ses Efekt Uygulaması 🎵", 
                         font=("Arial", 18, "bold"), bg='#2b2b2b', fg='#ffffff')
        baslik.pack(pady=20)
        
        # Dosya seçim çerçevesi
        dosya_frame = tk.Frame(self.root, bg='#2b2b2b')
        dosya_frame.pack(pady=10)
        
        self.dosya_btn = tk.Button(dosya_frame, text="📁 Ses Dosyası Seç", 
                                   command=self.ses_sec, font=("Arial", 12),
                                   bg='#4CAF50', fg='white', padx=20, pady=10,
                                   cursor='hand2')
        self.dosya_btn.pack()
        
        self.dosya_label = tk.Label(self.root, text="Dosya seçilmedi", 
                                    font=("Arial", 10), bg='#2b2b2b', fg='#cccccc')
        self.dosya_label.pack(pady=5)
        
        # Oynatma kontrolleri
        kontrol_frame = tk.Frame(self.root, bg='#2b2b2b')
        kontrol_frame.pack(pady=15)
        
        self.oynat_btn = tk.Button(kontrol_frame, text="▶ Oynat", 
                                   command=self.ses_oynat, font=("Arial", 11),
                                   bg='#2196F3', fg='white', padx=15, pady=8,
                                   state='disabled', cursor='hand2')
        self.oynat_btn.grid(row=0, column=0, padx=5)
        
        self.durdur_btn = tk.Button(kontrol_frame, text="⏹ Durdur", 
                                    command=self.ses_durdur, font=("Arial", 11),
                                    bg='#f44336', fg='white', padx=15, pady=8,
                                    state='disabled', cursor='hand2')
        self.durdur_btn.grid(row=0, column=1, padx=5)
        
        self.sifirla_btn = tk.Button(kontrol_frame, text="🔄 Sıfırla", 
                                     command=self.sifirla, font=("Arial", 11),
                                     bg='#FF9800', fg='white', padx=15, pady=8,
                                     state='disabled', cursor='hand2')
        self.sifirla_btn.grid(row=0, column=2, padx=5)
        
        # Efekt butonları
        efekt_label = tk.Label(self.root, text="Efektler:", 
                              font=("Arial", 14, "bold"), bg='#2b2b2b', fg='#ffffff')
        efekt_label.pack(pady=(20, 10))
        
        efekt_frame = tk.Frame(self.root, bg='#2b2b2b')
        efekt_frame.pack(pady=10)
        
        # İlk satır
        satir1 = tk.Frame(efekt_frame, bg='#2b2b2b')
        satir1.pack(pady=5)
        
        self.incelt_btn = tk.Button(satir1, text="🎤 Sesi İncelt", 
                                    command=self.sesi_incelt, font=("Arial", 10),
                                    bg='#9C27B0', fg='white', padx=20, pady=8,
                                    state='disabled', cursor='hand2', width=15)
        self.incelt_btn.grid(row=0, column=0, padx=5)
        
        self.kalinlastir_btn = tk.Button(satir1, text="🎸 Sesi Kalınlaştır", 
                                        command=self.sesi_kalinlastir, font=("Arial", 10),
                                        bg='#673AB7', fg='white', padx=20, pady=8,
                                        state='disabled', cursor='hand2', width=15)
        self.kalinlastir_btn.grid(row=0, column=1, padx=5)
        
        # İkinci satır
        satir2 = tk.Frame(efekt_frame, bg='#2b2b2b')
        satir2.pack(pady=5)
        
        self.robot_btn = tk.Button(satir2, text="🤖 Robot Sesi", 
                                   command=self.robot_ses, font=("Arial", 10),
                                   bg='#607D8B', fg='white', padx=20, pady=8,
                                   state='disabled', cursor='hand2', width=15)
        self.robot_btn.grid(row=0, column=0, padx=5)
        
        self.yankilan_btn = tk.Button(satir2, text="🔊 Yankı", 
                                     command=self.yankilan_ekle, font=("Arial", 10),
                                     bg='#009688', fg='white', padx=20, pady=8,
                                     state='disabled', cursor='hand2', width=15)
        self.yankilan_btn.grid(row=0, column=1, padx=5)
        
        # Üçüncü satır
        satir3 = tk.Frame(efekt_frame, bg='#2b2b2b')
        satir3.pack(pady=5)
        
        self.kedi_btn = tk.Button(satir3, text="🐱 Kedi Sesi", 
                                 command=self.kedi_ses, font=("Arial", 10),
                                 bg='#FF5722', fg='white', padx=20, pady=8,
                                 state='disabled', cursor='hand2', width=15)
        self.kedi_btn.grid(row=0, column=0, padx=5)
        
        self.canavar_btn = tk.Button(satir3, text="👹 Canavar Sesi", 
                                    command=self.canavar_ses, font=("Arial", 10),
                                    bg='#8B0000', fg='white', padx=20, pady=8,
                                    state='disabled', cursor='hand2', width=15)
        self.canavar_btn.grid(row=0, column=1, padx=5)
        
        # Kaydet butonu
        self.kaydet_btn = tk.Button(self.root, text="💾 Kaydet", 
                                    command=self.ses_kaydet, font=("Arial", 12, "bold"),
                                    bg='#4CAF50', fg='white', padx=30, pady=10,
                                    state='disabled', cursor='hand2')
        self.kaydet_btn.pack(pady=20)
        
        # Durum çubuğu
        self.durum_label = tk.Label(self.root, text="Hazır", 
                                   font=("Arial", 9), bg='#1a1a1a', fg='#00ff00',
                                   relief=tk.SUNKEN, anchor='w', padx=10)
        self.durum_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def ses_sec(self):
        dosya = filedialog.askopenfilename(
            title="Ses Dosyası Seç",
            filetypes=[("Ses Dosyaları", "*.wav *.mp3 *.flac *.ogg"), ("Tüm Dosyalar", "*.*")]
        )
        if dosya:
            try:
                self.ses_verisi, self.ornekleme_hizi = sf.read(dosya)
                if len(self.ses_verisi.shape) > 1:
                    self.ses_verisi = np.mean(self.ses_verisi, axis=1)
                
                self.orijinal_ses = self.ses_verisi.copy()
                self.dosya_yolu = dosya
                dosya_adi = dosya.split('/')[-1]
                self.dosya_label.config(text=f"📄 {dosya_adi}")
                self.durum_label.config(text=f"Dosya yüklendi: {dosya_adi}")
                
                # Butonları aktifleştir
                self.oynat_btn.config(state='normal')
                self.sifirla_btn.config(state='normal')
                self.incelt_btn.config(state='normal')
                self.kalinlastir_btn.config(state='normal')
                self.robot_btn.config(state='normal')
                self.yankilan_btn.config(state='normal')
                self.kedi_btn.config(state='normal')
                self.canavar_btn.config(state='normal')
                self.kaydet_btn.config(state='normal')
                
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken hata oluştu:\n{str(e)}")
    
    def ses_oynat(self):
        if self.ses_verisi is not None and not self.oynatiliyor:
            self.oynatiliyor = True
            self.durdur_btn.config(state='normal')
            self.durum_label.config(text="Oynatılıyor...")
            
            def oynat():
                sd.play(self.ses_verisi, self.ornekleme_hizi)
                sd.wait()
                self.oynatiliyor = False
                self.durdur_btn.config(state='disabled')
                self.durum_label.config(text="Oynatma tamamlandı")
            
            threading.Thread(target=oynat, daemon=True).start()
    
    def ses_durdur(self):
        sd.stop()
        self.oynatiliyor = False
        self.durdur_btn.config(state='disabled')
        self.durum_label.config(text="Durduruldu")
    
    def sifirla(self):
        if self.orijinal_ses is not None:
            self.ses_verisi = self.orijinal_ses.copy()
            self.durum_label.config(text="Ses orijinal haline döndürüldü")
            messagebox.showinfo("Sıfırla", "Ses orijinal haline döndürüldü!")
    
    def sesi_incelt(self):
        if self.ses_verisi is not None:
            # Pitch shifting - sesi yükselt
            self.ses_verisi = self._pitch_shift(self.ses_verisi, 1.5)
            self.durum_label.config(text="İnce ses efekti uygulandı")
            messagebox.showinfo("Efekt", "İnce ses efekti uygulandı! 🎤")
    
    def sesi_kalinlastir(self):
        if self.ses_verisi is not None:
            # Pitch shifting - sesi alçalt
            self.ses_verisi = self._pitch_shift(self.ses_verisi, 0.7)
            self.durum_label.config(text="Kalın ses efekti uygulandı")
            messagebox.showinfo("Efekt", "Kalın ses efekti uygulandı! 🎸")
    
    def robot_ses(self):
        if self.ses_verisi is not None:
            # Basit vocoder efekti
            modulasyon = np.sin(2 * np.pi * 30 * np.arange(len(self.ses_verisi)) / self.ornekleme_hizi)
            self.ses_verisi = self.ses_verisi * (0.5 + 0.5 * modulasyon)
            self.ses_verisi = np.clip(self.ses_verisi, -1, 1)
            self.durum_label.config(text="Robot sesi efekti uygulandı")
            messagebox.showinfo("Efekt", "Robot sesi efekti uygulandı! 🤖")
    
    def yankilan_ekle(self):
        if self.ses_verisi is not None:
            gecikme = int(0.3 * self.ornekleme_hizi)
            yankilan = np.zeros(len(self.ses_verisi) + gecikme)
            yankilan[:len(self.ses_verisi)] = self.ses_verisi
            yankilan[gecikme:] += self.ses_verisi * 0.5
            self.ses_verisi = yankilan[:len(self.ses_verisi)]
            self.ses_verisi = np.clip(self.ses_verisi, -1, 1)
            self.durum_label.config(text="Yankı efekti uygulandı")
            messagebox.showinfo("Efekt", "Yankı efekti uygulandı! 🔊")
    
    def kedi_ses(self):
        if self.ses_verisi is not None:
            # Kedi sesi için yüksek pitch + titreşim
            self.ses_verisi = self._pitch_shift(self.ses_verisi, 2.0)
            vibrato = np.sin(2 * np.pi * 5 * np.arange(len(self.ses_verisi)) / self.ornekleme_hizi)
            self.ses_verisi = self.ses_verisi * (1 + 0.1 * vibrato)
            self.ses_verisi = np.clip(self.ses_verisi, -1, 1)
            self.durum_label.config(text="Kedi sesi efekti uygulandı")
            messagebox.showinfo("Efekt", "Kedi sesi efekti uygulandı! 🐱")
    
    def canavar_ses(self):
        if self.ses_verisi is not None:
            # Canavar sesi için çok düşük pitch + distortion
            self.ses_verisi = self._pitch_shift(self.ses_verisi, 0.5)
            self.ses_verisi = np.tanh(self.ses_verisi * 3) * 0.8
            self.durum_label.config(text="Canavar sesi efekti uygulandı")
            messagebox.showinfo("Efekt", "Canavar sesi efekti uygulandı! 👹")
    
    def _pitch_shift(self, ses, faktor):
        # Basit resampling ile pitch shifting
        indices = np.arange(0, len(ses), faktor)
        indices = indices[indices < len(ses)].astype(int)
        return ses[indices]
    
    def ses_kaydet(self):
        if self.ses_verisi is not None:
            dosya = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV Dosyası", "*.wav"), ("Tüm Dosyalar", "*.*")]
            )
            if dosya:
                try:
                    sf.write(dosya, self.ses_verisi, self.ornekleme_hizi)
                    self.durum_label.config(text=f"Kaydedildi: {dosya.split('/')[-1]}")
                    messagebox.showinfo("Başarılı", "Ses dosyası başarıyla kaydedildi! 💾")
                except Exception as e:
                    messagebox.showerror("Hata", f"Kaydetme hatası:\n{str(e)}")

if __name__ == "__main__":
    root = tk.TK()
    app = SesEfektUygulamasi(root)
    root.mainloop()