import os
import sys
import time
from PIL import Image

GAMBAR_SUMBER = "zee.jpg"

DURASI_ANIMASI = 0.1

KARAKTER_KODE = (
    "def process_data(d): "
    "if d is None: return; "
    "for i in d: print(i); "
    "class S: pass; "
    "import os; "
    "try: f = open('f.txt'); "
    "except: pass; "
    "data = [x*x for x in range(100)];"
).replace(" ", "")


def gambar_ke_terminal(path_gambar: str):
    try:
        gambar_asli = Image.open(path_gambar).convert("RGB")
        lebar_asli, tinggi_asli = gambar_asli.size
        lebar_terminal = os.get_terminal_size().columns
        tinggi_baru = int((tinggi_asli / lebar_asli) * lebar_terminal * 0.5) 
        
        gambar = gambar_asli.resize((lebar_terminal, tinggi_baru), Image.Resampling.LANCZOS)
        
        data_animasi = []
        indeks_karakter = 0
        for y in range(tinggi_baru):
            baris_data = []
            for x in range(lebar_terminal):
                r, g, b = gambar.getpixel((x, y))
                
                char = KARAKTER_KODE[indeks_karakter % len(KARAKTER_KODE)]
                indeks_karakter += 1
                
                baris_data.append((char, (r, g, b)))
            data_animasi.append(baris_data)
            
        total_karakter = tinggi_baru * lebar_terminal
        if total_karakter == 0:
            print("Tidak ada yang bisa ditampilkan.")
            return
            
        delay_per_karakter = DURASI_ANIMASI / total_karakter
        
        sys.stdout.write("\033[?25l") 
        sys.stdout.flush()

        for baris in data_animasi:
            for char, (r, g, b) in baris:
                warna_ansi = f"\033[38;2;{r};{g};{b}m"
                
                sys.stdout.write(f"{warna_ansi}{char}")
                sys.stdout.flush()
                time.sleep(delay_per_karakter)
        
        sys.stdout.write("\033[0m\n")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    except FileNotFoundError:
        print(f"Error: File tidak ditemukan di '{path_gambar}'")
        print("Pastikan Anda sudah mengganti 'GAMBAR_SUMBER' dengan path yang benar.")
    except Exception as e:
        sys.stdout.write("\033[0m\n")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        print(f"Terjadi error: {e}")


if __name__ == "__main__":
    gambar_ke_terminal(GAMBAR_SUMBER)