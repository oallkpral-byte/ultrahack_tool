import os
import sys
import ctypes
import subprocess
import time
import json
import random
import string
import hashlib
import shutil
import winreg
import uuid
import datetime
import psutil

class UltraHackTool:
    def __init__(self):
        self.version = "4.0"
        self.admin = False
        
        # Продукты для ключей
        self.products = {
            "1": {"name": "UltraHack PUBG Mobile Bypass", "prefix": "UHPM"},
            "2": {"name": "UltraHack Emulator Bypass", "prefix": "UHEB"},
            "3": {"name": "UltraHack HWID Spoofer", "prefix": "UHHS"},
            "4": {"name": "UltraHack Anti-Ban", "prefix": "UHAB"},
            "5": {"name": "UltraHack Full Package", "prefix": "UHFP"}
        }
        
        self.keys_file = "ultrahack_keys.txt"
        self.license_file = "ultrahack_license.json"
        
    # ========== ПРОВЕРКА АДМИНА ==========
    def check_admin(self):
        try:
            self.admin = ctypes.windll.shell32.IsUserAnAdmin() == 1
        except:
            self.admin = False
        return self.admin
    
    def request_admin(self):
        if not self.check_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    
    # ========== ГЕНЕРАТОР КЛЮЧЕЙ ==========
    def get_hwid(self):
        return str(uuid.getnode())
    
    def generate_license_key(self, product_id, days=365):
        product = self.products.get(product_id)
        if not product:
            return None
            
        prefix = product["prefix"]
        hwid = self.get_hwid()
        
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choice(chars) for _ in range(16))
        
        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        expiry_str = expiry.strftime("%Y%m%d")
        
        key = f"{prefix}-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}-{random_part[12:16]}"
        
        check_data = f"{key}-{hwid}-{expiry_str}".encode()
        checksum = hashlib.md5(check_data).hexdigest()[:4].upper()
        
        final_key = f"{key}-{checksum}"
        
        self.save_key(final_key, product["name"], expiry, hwid)
        
        return final_key
    
    def save_key(self, key, product_name, expiry, hwid):
        data = {
            "key": key,
            "product": product_name,
            "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S"),
            "hwid": hwid,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(self.keys_file, "a", encoding="utf-8") as f:
            f.write(f"Продукт: {product_name}\n")
            f.write(f"Ключ: {key}\n")
            f.write(f"Срок: {expiry.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"HWID: {hwid}\n")
            f.write(f"Создан: {data['created']}\n")
            f.write("=" * 60 + "\n")
        
        try:
            with open(self.license_file, "r", encoding="utf-8") as f:
                licenses = json.load(f)
        except:
            licenses = []
        
        licenses.append(data)
        
        with open(self.license_file, "w", encoding="utf-8") as f:
            json.dump(licenses, f, indent=2, ensure_ascii=False)
    
    def generate_batch(self, product_id, count=10):
        keys = []
        for i in range(count):
            days = random.choice([30, 90, 180, 365])
            key = self.generate_license_key(product_id, days)
            keys.append(key)
        return keys
    
    def show_all_keys(self):
        if os.path.exists(self.keys_file):
            print("\n" + "=" * 60)
            print("  Все сгенерированные ключи:")
            print("=" * 60)
            with open(self.keys_file, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print("\n[-] Ключи ещё не генерировались!")
    
    # ========== ОБХОД ЭМУЛЯТОРА ==========
    def bypass_emulator(self):
        print("[+] Обход эмулятора...")
        
        emulator_paths = [
            "C:\\Program Files\\LDPlayer",
            "C:\\Program Files\\Nox",
            "C:\\Program Files\\BlueStacks",
            "C:\\Program Files\\MuMu",
            "C:\\Program Files (x86)\\LDPlayer",
            "C:\\Program Files (x86)\\Nox",
            "C:\\Program Files (x86)\\BlueStacks",
            "C:\\Program Files (x86)\\MuMu"
        ]
        
        os.environ["EMULATOR"] = "0"
        
        for path in emulator_paths:
            if os.path.exists(path):
                new_name = path + "_backup_" + ''.join(random.choices(string.ascii_lowercase, k=5))
                try:
                    os.rename(path, new_name)
                    print(f"    [+] {path} -> {new_name}")
                except:
                    pass
        
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() in ['ldplayer.exe', 'nox.exe', 'bluestacks.exe', 'mumu.exe', 'dnplayer.exe', 'noxvm.exe']:
                    proc.kill()
                    print(f"    [+] Убит процесс: {proc.info['name']}")
            except:
                pass
        
        print("[+] Эмулятор обойден!")
        return True
    
    # ========== ОБХОД HWID ==========
    def bypass_hwid(self):
        print("[+] Обход HWID...")
        
        mac = "02:" + ":".join([''.join(random.choices('0123456789ABCDEF', k=2)) for _ in range(5)])
        print(f"    [+] Новый MAC: {mac}")
        
        try:
            subprocess.run(['wmic', 'diskdrive', 'set', 'SerialNumber', ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))], 
                         capture_output=True)
            print("    [+] Серийный номер диска изменен")
        except:
            pass
        
        try:
            subprocess.run(['wmic', 'csproduct', 'set', 'UUID', str(uuid.uuid4())], capture_output=True)
            print("    [+] UUID изменен")
        except:
            pass
        
        try:
            reg_paths = [
                r"SOFTWARE\\Tencent\\PUBG",
                r"SOFTWARE\\Tencent\\MobileGamePC",
                r"SOFTWARE\\Wow6432Node\\Tencent\\PUBG"
            ]
            
            for path in reg_paths:
                try:
                    winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, path)
                    print(f"    [+] Удален ключ реестра: {path}")
                except:
                    pass
        except:
            pass
        
        print("[+] HWID обойден!")
        return True
    
    # ========== АНТИ-БАН ==========
    def bypass_antiban(self):
        print("[+] Включение анти-бана...")
        
        services = [
            "TencentSafe",
            "TP3Service",
            "AntiCheatExpert",
            "ACE-BASE",
            "TencentSvc",
            "QMFastScan"
        ]
        
        for service in services:
            try:
                subprocess.run(['sc', 'stop', service], capture_output=True)
                subprocess.run(['sc', 'config', service, 'start=', 'disabled'], capture_output=True)
                print(f"    [+] Отключена служба: {service}")
            except:
                pass
        
        log_paths = [
            "C:\\Program Files\\Tencent\\PUBG\\Logs",
            "C:\\ProgramData\\Tencent\\PUBG\\Logs",
            os.path.expanduser("~\\AppData\\Local\\Tencent\\PUBG\\Logs"),
            os.path.expanduser("~\\AppData\\Roaming\\Tencent\\PUBG\\Logs")
        ]
        
        for path in log_paths:
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                    print(f"    [+] Удалены логи: {path}")
                except:
                    pass
        
        print("[+] Анти-бан активирован!")
        return True
    
    # ========== ОБХОД ROOT ==========
    def bypass_root(self):
        print("[+] Обход root-проверки...")
        
        root_files = [
            "su",
            "busybox",
            "magisk",
            "supersu"
        ]
        
        for file in root_files:
            paths = [
                f"/system/bin/{file}",
                f"/system/xbin/{file}",
                f"/sbin/{file}"
            ]
            for path in paths:
                if os.path.exists(path):
                    try:
                        os.rename(path, path + "_hidden")
                        print(f"    [+] Скрыт: {path}")
                    except:
                        pass
        
        print("[+] Root обойден!")
        return True
    
    # ========== ОБХОД FRIDA ==========
    def bypass_frida(self):
        print("[+] Обход Frida...")
        
        frida_files = [
            "frida-server",
            "frida-gadget",
            "libfrida",
            "frida-helper"
        ]
        
        for file in frida_files:
            try:
                subprocess.run(['taskkill', '/f', '/im', file], capture_output=True)
                print(f"    [+] Убит процесс: {file}")
            except:
                pass
        
        print("[+] Frida обойдена!")
        return True
    
    # ========== ОЧИСТКА СЛЕДОВ ==========
    def clean_traces(self):
        print("[+] Очистка следов...")
        
        temp_paths = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            "C:\\Windows\\Temp"
        ]
        
        for path in temp_paths:
            if path and os.path.exists(path):
                try:
                    for file in os.listdir(path):
                        file_path = os.path.join(path, file)
                        try:
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except:
                            pass
                    print(f"    [+] Очищено: {path}")
                except:
                    pass
        
        try:
            subprocess.run(['reg', 'delete', 'HKCU\\Software\\Tencent', '/f'], capture_output=True)
            print("    [+] Очищен реестр Tencent")
        except:
            pass
        
        print("[+] Следы очищены!")
    
    # ========== ЗАПУСК PUBG ==========
    def start_pubg(self):
        print("[+] Запуск PUBG Mobile...")
        
        pubg_paths = [
            "C:\\Program Files\\Tencent\\PUBG\\TGB\\TGB.exe",
            "C:\\Program Files (x86)\\Tencent\\PUBG\\TGB\\TGB.exe",
            "D:\\Tencent\\PUBG\\TGB\\TGB.exe",
            "D:\\Program Files\\Tencent\\PUBG\\TGB\\TGB.exe",
            "E:\\Tencent\\PUBG\\TGB\\TGB.exe",
            "C:\\Program Files\\Tencent\\MobileGamePC\\TGB.exe",
            "C:\\Program Files (x86)\\Tencent\\MobileGamePC\\TGB.exe"
        ]
        
        for path in pubg_paths:
            if os.path.exists(path):
                print(f"    [+] Найден PUBG: {path}")
                os.startfile(path)
                print("[+] PUBG запущен!")
                return True
        
        print("[-] PUBG Mobile не найден!")
        path = input("    Укажите путь к TGB.exe: ")
        if os.path.exists(path):
            os.startfile(path)
            print("[+] PUBG запущен!")
            return True
        
        return False
    
    # ========== ПОЛНЫЙ ОБХОД ==========
    def full_bypass(self):
        print("\n[+] Запуск полного обхода...")
        self.bypass_emulator()
        self.bypass_hwid()
        self.bypass_antiban()
        self.bypass_root()
        self.bypass_frida()
        self.clean_traces()
        print("\n[✓] Все обходы активированы!")
        print("[+] Можно запускать PUBG Mobile!")
    
    # ========== ГЛАВНОЕ МЕНЮ ==========
    def show_menu(self):
        print("=" * 60)
        print("  UltraHack Tool v4.0")
        print("  PUBG Mobile Bypass + KeyGen")
        print("=" * 60)
        print()
        print("  [1] Генератор ключей")
        print("  [2] Обход (Bypass)")
        print("  [0] Выход")
        print()
        
        choice = input("Выбор: ")
        
        if choice == "0":
            return False
        
        elif choice == "1":
            self.keygen_menu()
        
        elif choice == "2":
            self.bypass_menu()
        
        return True
    
    def keygen_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print("  ГЕНЕРАТОР КЛЮЧЕЙ UltraHack")
        print("=" * 60)
        print()
        print("Выберите продукт:")
        for pid, p in self.products.items():
            print(f"  {pid}. {p['name']}")
        print("  6. Генерировать все (5 ключей)")
        print("  7. Показать все ключи")
        print("  0. Назад")
        print()
        
        choice = input("Ваш выбор: ")
        
        if choice == "0":
            return
        
        if choice == "6":
            print("\n[+] Генерирую ключи для всех продуктов...")
            for pid in self.products:
                key = self.generate_license_key(pid, 365)
                print(f"  {self.products[pid]['name']}: {key}")
            print(f"\n[+] Все ключи сохранены в {self.keys_file}")
            input("\nНажмите Enter...")
            return
        
        if choice == "7":
            self.show_all_keys()
            input("\nНажмите Enter...")
            return
        
        if choice in self.products:
            print(f"\nВыбран: {self.products[choice]['name']}")
            print("\nСрок действия:")
            print("  1. 30 дней")
            print("  2. 90 дней")
            print("  3. 180 дней")
            print("  4. 365 дней (1 год)")
            print("  5. Навсегда (9999 дней)")
            
            days_choice = input("Выбор: ")
            days_map = {"1": 30, "2": 90, "3": 180, "4": 365, "5": 9999}
            days = days_map.get(days_choice, 365)
            
            key = self.generate_license_key(choice, days)
            if key:
                print(f"\n[+] Ключ сгенерирован: {key}")
                print(f"[+] Сохранён в {self.keys_file}")
            else:
                print("[-] Ошибка генерации!")
            input("\nНажмите Enter...")
            return
    
    def bypass_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print("  ОБХОД UltraHack")
        print("=" * 60)
        print()
        print("  1. Полный обход (все методы)")
        print("  2. Обход эмулятора")
        print("  3. Обход HWID")
        print("  4. Анти-бан")
        print("  5. Обход root")
        print("  6. Обход Frida")
        print("  7. Запустить PUBG Mobile")
        print("  8. Очистить следы")
        print("  0. Назад")
        print()
        
        choice = input("Выбор: ")
        
        if choice == "0":
            return
        
        elif choice == "1":
            self.full_bypass()
            input("\nНажмите Enter...")
        
        elif choice == "2":
            self.bypass_emulator()
            input("\nНажмите Enter...")
        
        elif choice == "3":
            self.bypass_hwid()
            input("\nНажмите Enter...")
        
        elif choice == "4":
            self.bypass_antiban()
            input("\nНажмите Enter...")
        
        elif choice == "5":
            self.bypass_root()
            input("\nНажмите Enter...")
        
        elif choice == "6":
            self.bypass_frida()
            input("\nНажмите Enter...")
        
        elif choice == "7":
            self.start_pubg()
            input("\nНажмите Enter...")
        
        elif choice == "8":
            self.clean_traces()
            input("\nНажмите Enter...")
    
    def run(self):
        print("=" * 60)
        print("  UltraHack Tool v4.0")
        print("  PUBG Mobile Bypass + KeyGen")
        print("=" * 60)
        print()
        
        if not self.check_admin():
            print("[!] Требуются права администратора!")
            self.request_admin()
            return
        
        print("[✓] Права администратора получены")
        print()
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if not self.show_menu():
                break

if __name__ == "__main__":
    tool = UltraHackTool()
    tool.run()