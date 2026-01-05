import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_login_test_lambdatest():
    print("--- Memulai Login Test (LambdaTest Playground) ---")

    # 1. KONFIGURASI DRIVER LOKAL
    options = ChromeOptions()
    options.add_argument("--start-maximized") 
    
    driver = webdriver.Chrome(options=options)

    try:
        print("1. Membuka halaman Login...")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        time.sleep(1)

        # 2. INPUT DATA
        # ---------------------------------------------------------
        # ⚠️ TUGAS ANDA:
        # Ganti email di bawah ini dengan email yang SUKSES terdaftar
        # dari output script 'run_registration_fix' yang baru Anda jalankan.
        # ---------------------------------------------------------
        email_login = "johndoe321@gmail.com"  # <--- GANTI INI
        password_login = "283128370 "

        print(f"2. Mengisi Email: {email_login}")
        driver.find_element(By.ID, "input-email").send_keys(email_login)
        time.sleep(1)

        print(f"   Mengisi Password...")
        driver.find_element(By.ID, "input-password").send_keys(password_login)
        time.sleep(1)

        # 3. KLIK LOGIN
        print("3. Klik tombol Login...")
        tombol_login = driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
        driver.execute_script("arguments[0].click();", tombol_login)

        # 4. VERIFIKASI (ASSERTION)
        wait = WebDriverWait(driver, 10)
        print("4. Verifikasi Login...")
        
        try:
            # Jika login sukses, URL akan berubah ke route=account/account
            # Atau Title halaman menjadi "My Account"
            wait.until(EC.title_is("My Account"))
            print("✅ TEST PASSED: Berhasil masuk ke halaman 'My Account'!")
            
            # Cek elemen spesifik di dashboard
            if driver.find_element(By.LINK_TEXT, "Edit your account information").is_displayed():
                print("   -> Menu akun terlihat valid.")

        except:
            # Jika gagal, ambil pesan error merah
            try:
                error_msg = driver.find_element(By.CSS_SELECTOR, "div.alert-danger").text
                print(f"❌ TEST FAILED: Login Gagal. Pesan: {error_msg}")
                print("   (Pastikan email yang dipakai sudah benar-benar terdaftar)")
            except:
                print("❌ TEST FAILED: Judul halaman bukan 'My Account'.")

    except Exception as e:
        print("Terjadi Error System:", e)
        
    finally:
        print("Test Selesai. Browser akan menutup dalam 5 detik...")
        time.sleep(5)
        driver.quit()
        print("Sesi ditutup.")

if __name__ == "__main__":
    run_login_test_lambdatest()