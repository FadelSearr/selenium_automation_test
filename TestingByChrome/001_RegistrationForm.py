import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_registration_ecommerce_local():
    print("--- Memulai Tes Registrasi (E-Commerce) Secara Lokal ---")

    # 1. KONFIGURASI DRIVER
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)

    try:
        print("1. Membuka halaman Registrasi...")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/register")
        time.sleep(1)

        # 2. PENGISIAN DATA
        print("2. Mulai mengisi formulir...")

        # A. Personal Details
        driver.find_element(By.ID, "input-firstname").send_keys("Jhon")
        driver.find_element(By.ID, "input-lastname").send_keys("Doe")
        
        # B. EMAIL UNIK
        timestamp = int(time.time())
        email_unik = f"Jhondoe.{timestamp}@contoh.com"
        
        print(f"   -> Menggunakan Email: {email_unik}")
        driver.find_element(By.ID, "input-email").send_keys(email_unik)
        
        driver.find_element(By.ID, "input-telephone").send_keys("08123456789")

        # C. Password & Confirm
        print("   -> Mengisi Password...")
        driver.find_element(By.ID, "input-password").send_keys("Rahasia123!")
        driver.find_element(By.ID, "input-confirm").send_keys("Rahasia123!")
        time.sleep(1)

        # D. Subscribe Newsletter (Pilih No) - BAGIAN PERBAIKAN
        print("   -> Memilih Newsletter: No...")
        # Kita cari elemennya, lalu paksa klik dengan JavaScript
        newsletter_radio = driver.find_element(By.CSS_SELECTOR, "input[name='newsletter'][value='0']")
        driver.execute_script("arguments[0].click();", newsletter_radio)

        # E. Privacy Policy
        print("   -> Mencentang Privacy Policy...")
        checkbox_policy = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].click();", checkbox_policy)
        time.sleep(1)

        # 3. SUBMIT
        print("3. Klik tombol Continue...")
        tombol_continue = driver.find_element(By.CSS_SELECTOR, "input[value='Continue']")
        driver.execute_script("arguments[0].click();", tombol_continue)

        # 4. VERIFIKASI (ASSERTION)
        wait = WebDriverWait(driver, 10)
        
        print("4. Menunggu konfirmasi sukses...")
        wait.until(EC.title_contains("Created"))
        
        header_text = driver.find_element(By.TAG_NAME, "h1").text
        print(f"   Judul Halaman: {header_text}")

        if "Has Been Created" in header_text:
            print("✅ TEST PASSED: Akun baru berhasil dibuat!")
        else:
            print("❌ TEST FAILED: Tidak masuk ke halaman sukses.")

    except Exception as e:
        print("Terjadi Error:", e)
        
    finally:
        print(f"Test Selesai. (Email: {email_unik})")
        print("Browser akan menutup dalam 5 detik...")
        time.sleep(5)
        driver.quit()
        print("Sesi ditutup.")

if __name__ == "__main__":
    run_registration_ecommerce_local()