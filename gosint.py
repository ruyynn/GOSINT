#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOSINT v1.1 - PEMBELAJARAN OSINT
Author: Ruyynn (Untuk Tujuan Pembelajaran)
GitHub: https://github.com/ruyynn
"""

import os
import sys
import time
import json
import socket
import requests
import dns.resolver
import whois
from phonenumbers import (
    parse, is_valid_number, format_number,
    PhoneNumberFormat, carrier, geocoder, timezone
)
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import subprocess
import platform
from datetime import datetime, timedelta
import hashlib
import urllib.parse
import random
from colorama import init, Fore, Back, Style

# Rich untuk UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.padding import Padding
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    from rich.prompt import Prompt
    from rich.text import Text
    from rich.markdown import Markdown
    from rich.layout import Layout
    from rich.live import Live
    from rich.columns import Columns
    console = Console()
except:
    os.system('pip install -q rich')
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    console = Console()

init(autoreset=True)

# ==================== KONFIGURASI ====================
TIMEOUT = 10
MAX_THREADS = 30
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# ==================== LOGO GOSINT ====================
GOSINT_LOGO = f"""
{Fore.RED}   █████████     ███████     █████████  █████ ██████   █████ ███████████
  ███░░░░░███  ███░░░░░███  ███░░░░░███░░███ ░░██████ ░░███ ░█░░░███░░░█
 ███     ░░░  ███     ░░███░███    ░░░  ░███  ░███░███ ░███ ░   ░███  ░ 
░███         ░███      ░███░░█████████  ░███  ░███░░███░███     ░███    
░███    █████░███      ░███ ░░░░░░░░███ ░███  ░███ ░░██████     ░███    
░░███  ░░███ ░░███     ███  ███    ░███ ░███  ░███  ░░█████     ░███    
 ░░█████████  ░░░███████░  ░░█████████  █████ █████  ░░█████    █████   
  ░░░░░░░░░     ░░░░░░░     ░░░░░░░░░  ░░░░░ ░░░░░    ░░░░░    ░░░░░ {Style.RESET_ALL}
{Fore.CYAN}                      G O S I N T   v 1 . 1   -   P E M B E L A J A R A N{Style.RESET_ALL}
{Fore.YELLOW}                      Author: Ruyynn | GitHub: https://github.com/ruyynn{Style.RESET_ALL}
"""

# ==================== PENDAHULUAN ====================
PENDAHULUAN = f"""
{Fore.WHITE}╔════════════════════════════════════════════════════════════════════════════╗
║  {Fore.GREEN}SELAMAT DATANG DI GOSINT - TOOL PEMBELAJARAN OSINT{Fore.WHITE}                        ║
╠════════════════════════════════════════════════════════════════════════════╣
║  • Tool ini dibuat untuk MEMPELAJARI cara kerja OSINT                      ║
║  • Data yang ditampilkan adalah ILUSTRASI untuk pembelajaran               ║
║  • Gunakan untuk memahami pentingnya menjaga data pribadi                  ║
║  • Setiap modul dilengkapi penjelasan dan tips pencegahan                  ║
╚════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# ==================== MODUL PEMBELAJARAN PHONE ====================
class PhonePembelajaran:
    """
    Modul pembelajaran Phone OSINT
    Menampilkan ilustrasi bagaimana nomor telepon bisa dilacak
    """
    
    def __init__(self):
        # Database prefix provider (edukasi)
        self.provider_db = {
            '0811': 'Telkomsel', '0812': 'Telkomsel', '0813': 'Telkomsel',
            '0814': 'Indosat', '0815': 'Indosat', '0816': 'Indosat',
            '0851': 'Telkomsel', '0852': 'Telkomsel', '0853': 'Telkomsel',
            '0855': 'Indosat', '0856': 'Indosat', '0857': 'Indosat',
            '0858': 'XL', '0859': 'XL', '0877': 'XL', '0878': 'XL',
            '0831': 'Axis', '0832': 'Axis', '0833': 'Axis',
            '0895': 'Tri', '0896': 'Tri', '0897': 'Tri', '0898': 'Tri', '0899': 'Tri',
            '0881': 'Smartfren', '0882': 'Smartfren', '0883': 'Smartfren'
        }
        
    def pelajari(self, nomor, negara='ID'):
        print(f"\n{Fore.CYAN}[MEMULAI PEMBELAJARAN PHONE OSINT]{Style.RESET_ALL}")
        time.sleep(1)
        
        print(f"\n{Fore.YELLOW}📘 STUDI KASUS: Nomor {nomor}{Style.RESET_ALL}")
        print("=" * 60)
        
        # Langkah 1: Validasi Nomor
        print(f"\n{Fore.GREEN}LANGKAH 1: Validasi Nomor{Style.RESET_ALL}")
        print("   OSINT dimulai dengan memvalidasi format nomor internasional")
        
        try:
            num = parse(nomor, negara)
            if is_valid_number(num):
                print(f"\n   ✓ Format nomor VALID")
                national = format_number(num, PhoneNumberFormat.NATIONAL)
                international = format_number(num, PhoneNumberFormat.INTERNATIONAL)
                print(f"     Format Nasional : {national}")
                print(f"     Format Internasional: {international}")
            else:
                print(f"\n   ✗ Format nomor TIDAK VALID")
                print("     Pelajaran: Gunakan format +62 untuk Indonesia")
                return
        except:
            print(f"\n   ✗ Error parsing nomor")
            print("     Pelajaran: Pastikan format +628xxxxxxxxx")
            return
        
        time.sleep(1)
        
        # Langkah 2: Deteksi Provider
        print(f"\n{Fore.GREEN}LANGKAH 2: Deteksi Provider{Style.RESET_ALL}")
        print("   Provider bisa dideteksi dari prefix nomor")
        
        prefix = national[:4] if len(national) >= 4 else national
        provider = self.provider_db.get(prefix, "Provider tidak dikenal")
        
        print(f"\n   ✓ Prefix: {prefix}")
        print(f"   ✓ Provider: {provider}")
        print(f"\n   Penjelasan: Setiap provider memiliki blok nomor tertentu")
        print(f"   yang diberikan oleh pemerintah/regulator.")
        
        time.sleep(1)
        
        # Langkah 3: Cek Platform Digital
        print(f"\n{Fore.GREEN}LANGKAH 3: Cek Platform Digital{Style.RESET_ALL}")
        print("   OSINT bisa mengecek apakah nomor terdaftar di platform")
        
        # Simulasi untuk pembelajaran
        status_wa = random.choice([True, False])
        status_tg = random.choice([True, False])
        
        print(f"\n   📱 WhatsApp: {'TERDAFTAR' if status_wa else 'Tidak terdaftar'}")
        if status_wa:
            jam = random.randint(1, 23)
            menit = random.randint(0, 59)
            print(f"      • Terakhir online: {jam} jam {menit} menit yang lalu")
            print(f"      • Perangkat: {random.choice(['iPhone', 'Samsung', 'Xiaomi', 'OPPO'])}")
        
        print(f"\n   ✈️ Telegram: {'TERDAFTAR' if status_tg else 'Tidak terdaftar'}")
        if status_tg:
            print(f"      • Terakhir online: {random.choice(['Online', '5 menit lalu', '1 jam lalu'])}")
        
        print(f"\n   Penjelasan: WhatsApp dan Telegram memiliki cara pengecekan")
        print(f"   publik yang bisa digunakan untuk melihat aktivitas.")
        
        time.sleep(1)
        
        # Langkah 4: Analisis Risiko
        print(f"\n{Fore.GREEN}LANGKAH 4: Analisis Risiko Privasi{Style.RESET_ALL}")
        
        risiko = Table(title="RISIKO PRIVASI", box=box.ROUNDED)
        risiko.add_column("Informasi", style="cyan")
        risiko.add_column("Sumber", style="white")
        risiko.add_column("Dampak", style="red")
        
        risiko.add_row(
            "Provider & Lokasi",
            "Prefix nomor",
            "Targeting iklan, spam"
        )
        risiko.add_row(
            "Aktivitas WhatsApp",
            "Status online",
            "Mengetahui kebiasaan"
        )
        risiko.add_row(
            "Perangkat",
            "User-agent",
            "Fingerprinting"
        )
        
        console.print(risiko)
        
        # Langkah 5: Tips Pencegahan
        print(f"\n{Fore.GREEN}LANGKAH 5: Tips Melindungi Nomor{Style.RESET_ALL}")
        tips = [
            "1. Nonaktifkan 'Last Seen' di WhatsApp & Telegram",
            "2. Gunakan nomor kedua untuk registrasi publik",
            "3. Atur privasi hanya kontak yang bisa melihat foto",
            "4. Hati-hati memberikan nomor ke website tidak dikenal",
            "5. Cek keamanan nomor di haveibeenpwned.com"
        ]
        
        for tip in tips:
            print(f"   • {tip}")
        
        print(f"\n{Fore.YELLOW}[KESIMPULAN]{Style.RESET_ALL}")
        print("   Nomor telepon adalah data sensitif yang bisa")
        print("   digunakan untuk melacak aktivitas digital seseorang.")

# ==================== MODUL PEMBELAJARAN EMAIL ====================
class EmailPembelajaran:
    """
    Modul pembelajaran Email OSINT
    """
    
    def pelajari(self, email):
        print(f"\n{Fore.CYAN}[MEMULAI PEMBELAJARAN EMAIL OSINT]{Style.RESET_ALL}")
        time.sleep(1)
        
        print(f"\n{Fore.YELLOW}📘 STUDI KASUS: Email {email}{Style.RESET_ALL}")
        print("=" * 60)
        
        # Langkah 1: Validasi
        print(f"\n{Fore.GREEN}LANGKAH 1: Validasi Format Email{Style.RESET_ALL}")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            print(f"\n   ✓ Format email VALID")
            domain = email.split('@')[1]
            print(f"     Domain: {domain}")
        else:
            print(f"\n   ✗ Format email TIDAK VALID")
            return
        
        time.sleep(1)
        
        # Langkah 2: Analisis Domain
        print(f"\n{Fore.GREEN}LANGKAH 2: Analisis Domain{Style.RESET_ALL}")
        print("   OSINT bisa menganalisis domain untuk informasi lebih")
        
        # Simulasi MX record
        mx = [
            f"mail.{domain}",
            f"mx1.{domain}",
            f"mx2.{domain}"
        ]
        
        print(f"\n   • MX Records:")
        for m in mx:
            print(f"     - {m}")
        
        # Simulasi WHOIS
        print(f"\n   • Informasi Domain:")
        print(f"     - Registrar: {random.choice(['Namecheap', 'GoDaddy', 'Google Domains'])}")
        print(f"     - Created: {random.randint(2010, 2023)}")
        
        time.sleep(1)
        
        # Langkah 3: Gravatar
        print(f"\n{Fore.GREEN}LANGKAH 3: Gravatar{Style.RESET_ALL}")
        print("   Gravatar menghubungkan email dengan foto profil global")
        
        email_hash = hashlib.md5(email.lower().encode()).hexdigest()
        print(f"\n   • Hash MD5: {email_hash[:20]}...")
        print(f"   • Status: {'TERDAFTAR' if random.choice([True, False]) else 'Tidak terdaftar'}")
        
        time.sleep(1)
        
        # Langkah 4: Breach Check
        print(f"\n{Fore.GREEN}LANGKAH 4: Cek Kebocoran Data{Style.RESET_ALL}")
        print("   OSINT bisa mengecek apakah email pernah bocor")
        
        breaches = [
            "LinkedIn 2021",
            "Facebook 2019",
            "Adobe 2013",
            "Canva 2019",
        ]
        
        if random.choice([True, False]):
            print(f"\n   ⚠ Ditemukan dalam {random.randint(1,3)} breach:")
            for b in random.sample(breaches, random.randint(1,2)):
                print(f"     • {b}")
        else:
            print(f"\n   ✓ Tidak ditemukan dalam breach")
        
        time.sleep(1)
        
        # Langkah 5: Tips Keamanan
        print(f"\n{Fore.GREEN}LANGKAH 5: Tips Keamanan Email{Style.RESET_ALL}")
        tips = [
            "1. Gunakan email berbeda untuk layanan berbeda",
            "2. Aktifkan 2FA di semua akun penting",
            "3. Cek haveibeenpwned.com secara rutin",
            "4. Gunakan password manager",
            "5. Jangan klik link mencurigakan"
        ]
        
        for tip in tips:
            print(f"   • {tip}")
        
        print(f"\n{Fore.YELLOW}[KESIMPULAN]{Style.RESET_ALL}")
        print("   Email bisa mengungkap banyak informasi:")
        print("   • Domain tempat bekerja")
        print("   • Foto profil via Gravatar")
        print("   • Riwayat kebocoran data")

# ==================== MODUL PEMBELAJARAN USERNAME ====================
class UsernamePembelajaran:
    """
    Modul pembelajaran Username OSINT
    """
    
    def pelajari(self, username):
        console.print(f"\n[cyan][MEMULAI PEMBELAJARAN USERNAME OSINT][/cyan]")
        time.sleep(1)

        console.print(f"\n[yellow]📘 STUDI KASUS: Username '{username}'[/yellow]")
        console.print("=" * 60)

        # Langkah 1: Pemahaman
        console.print(f"\n[green]LANGKAH 1: Memahami Username OSINT[/green]")
        console.print("   Username adalah identitas digital yang sering digunakan")
        console.print("   di berbagai platform secara bersamaan.")
        time.sleep(1)

        # Langkah 2: Cek Platform
        console.print(f"\n[green]LANGKAH 2: Cek Keberadaan di Platform[/green]")

        platforms = {
            'GitHub': f"https://github.com/{username}",
            'Twitter': f"https://twitter.com/{username}",
            'Instagram': f"https://instagram.com/{username}",
            'Reddit': f"https://reddit.com/user/{username}",
            'Medium': f"https://medium.com/@{username}",
            'TikTok': f"https://tiktok.com/@{username}",
            'Telegram': f"https://t.me/{username}",
        }

        # Simulasi platform aktif
        aktif = random.sample(list(platforms.items()), random.randint(2, 4))

        table = Table(title="PLATFORM TERDETEKSI", box=box.ROUNDED)
        table.add_column("Platform", style="cyan")
        table.add_column("URL", style="white")

        for plat, url in aktif:
            table.add_row(plat, url)

        console.print(table)

        # ==================== CATATAN PENTING ====================
        console.print("\n📌 [bold yellow]Catatan Penting[/bold yellow]:")
        console.print("   Beberapa platform memiliki informasi publik tergantung pengaturan privasi pengguna.\n")
        time.sleep(1)

        # Langkah 3: Analisis
        console.print(f"\n[green]LANGKAH 3: Analisis Informasi[/green]")
        console.print("   Dari berbagai platform, bisa didapatkan:")
        info = [
            "📍 Lokasi (dari bio/profile)",
            "💼 Pekerjaan",
            "🎓 Pendidikan",
            "📧 Email",
            "📱 Hobi & Minat"
        ]
        for i in info:
            console.print(f"   • {i} (contoh)")
        time.sleep(1)

        # Langkah 4: Risiko
        console.print(f"\n[green]LANGKAH 4: Risiko Keamanan[/green]")
        risiko = Table(box=box.ROUNDED)
        risiko.add_column("Risiko", style="red")
        risiko.add_column("Dampak", style="yellow")
        risiko.add_row("Social Engineering", "Tinggi")
        risiko.add_row("Doxxing", "Sedang")
        risiko.add_row("Stalking", "Sedang")
        risiko.add_row("Password Cracking", "Rendah")
        console.print(risiko)
        time.sleep(1)

        # Langkah 5: Tips Proteksi
        console.print(f"\n[green]LANGKAH 5: Tips Proteksi[/green]")
        tips = [
            "1. Gunakan username berbeda tiap platform",
            "2. Jangan pakai username = nama asli",
            "3. Batasi info pribadi di profil",
            "4. Atur privasi maksimal",
            "5. Hapus akun lama yang tidak dipakai"
        ]
        for tip in tips:
            console.print(f"   • {tip}")
        console.print(f"\n[yellow][KESIMPULAN][/yellow]")
        console.print("   Username adalah kunci pencarian OSINT.")
        console.print("   Satu username bisa menghubungkan banyak profil.")

# ==================== MODUL PENCEGAHAN ====================
class ModulPencegahan:
    """
    Modul pencegahan OSINT
    """
    
    def tampilkan(self):
        print(f"\n{Fore.CYAN}[PANDUAN MELINDUNGI DATA PRIBADI]{Style.RESET_ALL}")
        time.sleep(1)
        
        panduan = """
# 📚 PANDUAN PRIVASI DIGITAL

## 1. **Nomor Telepon**
   • Nonaktifkan "Last Seen" di WhatsApp/Telegram
   • Gunakan nomor kedua untuk registrasi publik
   • Jangan tautkan nomor ke media sosial
   • Atur privasi hanya kontak yang bisa melihat foto

## 2. **Email**
   • Gunakan email berbeda untuk layanan berbeda
   • Aktifkan 2FA di semua akun penting
   • Cek haveibeenpwned.com secara rutin
   • Gunakan password manager

## 3. **Username**
   • Gunakan username berbeda tiap platform
   • Jangan pakai username = nama asli
   • Hindari username mengandung tahun lahir
   • Rutin googling username sendiri

## 4. **Media Sosial**
   • Atur profil ke private
   • Batasi postingan yang menunjukkan lokasi
   • Hati-hati dengan fitur check-in
   • Hapus metadata foto sebelum upload

## 5. **Kebiasaan Digital**
   • Gunakan VPN
   • Pasang extension pemblokir tracker
   • Hapus cookie secara rutin
   • Batasi izin aplikasi di smartphone

## Kesimpulan
Dengan memahami OSINT, kita bisa:
• Tahu data apa saja yang publik
• Melindungi informasi sensitif
• Lebih bijak dalam berbagi online
"""
        
        console.print(Markdown(panduan))
        input(f"\n{Fore.CYAN}Tekan Enter untuk kembali...{Style.RESET_ALL}")

# ==================== MODUL TENTANG OSINT ====================
class TentangOSINT:
    """
    Penjelasan umum tentang OSINT
    """
    
    def tampilkan(self):
        print(f"\n{Fore.CYAN}[APA ITU OSINT?]{Style.RESET_ALL}")
        print("=" * 60)
        
        penjelasan = """
OSINT (Open Source Intelligence) adalah teknik mengumpulkan
informasi dari sumber-sumber publik.

**Sumber Publik:**
• Media sosial
• Situs web dan forum
• Database publik
• Arsip internet
• Data pemerintah
• Berita dan artikel

**Tujuan Mempelajari OSINT:**
1. Memahami jejak digital sendiri
2. Melindungi privasi
3. Keamanan siber
4. Penelitian
5. Verifikasi identitas

**Etika OSINT:**
✓ Gunakan untuk kebaikan
✓ Hormati privasi orang lain
✓ Patuhi hukum
✓ Jangan untuk stalking/doxxing

**Tool ini untuk PEMBELAJARAN.**
Gunakan pengetahuan ini dengan bijak.
"""
        
        console.print(Markdown(penjelasan))
        input(f"\n{Fore.CYAN}Tekan Enter untuk kembali...{Style.RESET_ALL}")

# ==================== MAIN APP ====================
class GOSINTPembelajaran:
    def __init__(self):
        self.phone = PhonePembelajaran()
        self.email = EmailPembelajaran()
        self.username = UsernamePembelajaran()
        self.pencegahan = ModulPencegahan()
        self.tentang = TentangOSINT()
        self.first_run = True
        
    def banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(GOSINT_LOGO)
        
        if self.first_run:
            print(PENDAHULUAN)
            self.first_run = False
            input(f"{Fore.CYAN}Tekan Enter untuk memulai...{Style.RESET_ALL}")
            os.system('cls' if os.name == 'nt' else 'clear')
            print(GOSINT_LOGO)
        
        info = Panel(
            f"[bold cyan]📚[/bold cyan] Mode: [green]PEMBELAJARAN[/green]\n"
            f"[bold cyan]⚡[/bold cyan] Platform: {platform.system()}\n"
            f"[bold cyan]🎯[/bold cyan] Tujuan: Memahami OSINT",
            title="STATUS",
            border_style="blue"
        )
        console.print(info)
        
    def menu(self):
        table = Table(box=box.HEAVY, border_style="cyan")
        table.add_column("#", style="yellow")
        table.add_column("Modul", style="white")
        table.add_column("Deskripsi", style="dim")
        
        table.add_row("1", "📱 PHONE OSINT", "Pelajari tracking nomor telepon")
        table.add_row("2", "📧 EMAIL OSINT", "Pelajari jejak digital email")
        table.add_row("3", "👥 USERNAME OSINT", "Pelajari cross-platform tracking")
        table.add_row("4", "🛡️ PENCEGAHAN", "Cara melindungi data pribadi")
        table.add_row("5", "📚 TENTANG OSINT", "Penjelasan umum OSINT")
        table.add_row("6", "🚪 KELUAR", "Selesai")
        
        console.print(Panel(table, title="MENU", border_style="yellow"))
        
    def run(self):
        while True:
            self.banner()
            self.menu()
            
            pilihan = Prompt.ask("[bold cyan]Pilih modul[/bold cyan]", choices=["1","2","3","4","5","6"])
            
            if pilihan == "6":
                print(f"\n{Fore.YELLOW}Terima kasih telah belajar OSINT!{Style.RESET_ALL}")
                break
                
            elif pilihan == "1":
                target = Prompt.ask("[bold yellow]Masukkan nomor (contoh: +62812...)[/bold yellow]")
                self.phone.pelajari(target)
                
            elif pilihan == "2":
                target = Prompt.ask("[bold yellow]Masukkan email[/bold yellow]")
                self.email.pelajari(target)
                
            elif pilihan == "3":
                target = Prompt.ask("[bold yellow]Masukkan username[/bold yellow]")
                self.username.pelajari(target)
                
            elif pilihan == "4":
                self.pencegahan.tampilkan()
                
            elif pilihan == "5":
                self.tentang.tampilkan()
            
            if pilihan in ["1","2","3","4","5"]:
                input(f"\n{Fore.CYAN}Tekan Enter untuk kembali...{Style.RESET_ALL}")

# ==================== INSTALL ====================
def install_deps():
    deps = [
        'requests', 'dnspython', 'python-whois', 'phonenumbers',
        'colorama', 'rich', 'beautifulsoup4'
    ]
    
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
        except:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

# ==================== START ====================
if __name__ == "__main__":
    print(f"{Fore.GREEN}[✓] GOSINT - Persiapan...{Style.RESET_ALL}")
    install_deps()
    
    try:
        app = GOSINTPembelajaran()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Terima kasih!{Style.RESET_ALL}")
        sys.exit(0)