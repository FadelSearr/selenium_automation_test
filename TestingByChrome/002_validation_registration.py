from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_tc010_password_confirmation_local():
    """
    TC-010: Form Validation pada Registration (LOKAL)
    Skenario: Password dan Confirm Password sengaja dibuat BEDA.
    Ekspektasi: Muncul pesan error.
    """
    print("--- Memulai Tes Validasi Password Secara Lokal ---")

    # 1. KONFIGURASI BROWSER LOKAL
    options = ChromeOptions()
    options.add_argument("--start-maximized") # Browser Full Screen
    
    # Inisialisasi driver Chrome lokal
    driver = webdriver.Chrome(options=options)
    print("✅ Browser terbuka.")

    wait = WebDriverWait(driver, 20)

    try:
        # ===============================
        # STEP 1: Open Register Page
        # ===============================
        print("🔹 Membuka halaman registrasi...")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/register")
        time.sleep(1) # Jeda visual

        # Tunggu elemen nama muncul
        wait.until(EC.presence_of_element_located((By.ID, "input-firstname")))

        # ===============================
        # STEP 2: Fill Form
        # ===============================
        print("🔹 Mengisi form registrasi...")

        # A. Data Diri
        driver.find_element(By.ID, "input-firstname").send_keys("John")
        driver.find_element(By.ID, "input-lastname").send_keys("Doe")
        time.sleep(0.5)

        # B. Email Unik
        unique_email = f"johndoe321{int(time.time())}@test.com"
        driver.find_element(By.ID, "input-email").send_keys(unique_email)
        
        # C. Telepon
        driver.find_element(By.ID, "input-telephone").send_keys("081234567890")
        time.sleep(0.5)

        # D. PASSWORD (SENGAJA DIBUAT BEDA)
        print("   -> Mengisi Password: '1234'")
        driver.find_element(By.ID, "input-password").send_keys("1234")
        
        print("   -> Mengisi Confirm : '456789' (Beda)")
        driver.find_element(By.ID, "input-confirm").send_keys("4567899")
        time.sleep(1) # Jeda agar Anda melihat perbedaannya

        # ===============================
        # STEP 3: Select Newsletter = No
        # ===============================
        print("🔹 Pilih Newsletter: No")
        newsletter_no = driver.find_element(By.XPATH, "//input[@name='newsletter' and @value='0']")
        driver.execute_script("arguments[0].click();", newsletter_no)

        # ===============================
        # STEP 4: Agree Privacy Policy
        # ===============================
        print("🔹 Centang Privacy Policy")
        agree = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].click();", agree)
        time.sleep(1)

        # ===============================
        # STEP 5: Submit Form
        # ===============================
        print("🔹 Klik tombol Continue...")
        continue_btn = driver.find_element(By.XPATH, "//input[@value='Continue']")
        driver.execute_script("arguments[0].click();", continue_btn)

        # ===============================
        # STEP 6: Verify Error Message
        # ===============================
        print("🔹 Memverifikasi pesan error...")

        # Kita tunggu pesan error berwarna merah muncul
        # Selector XPath ini mencari div text-danger yang berisi kata 'Password confirmation'
        error_message_elem = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'text-danger') and contains(text(),'Password confirmation')]")
            )
        )

        error_text = error_message_elem.text
        print(f"   Pesan Error Muncul: '{error_text}'")

        # VALIDASI
        if "Password confirmation does not match password" in error_text:
            print("✅ TEST PASSED: Sistem berhasil menolak password yang tidak sama!")
            
            #  
            # (Gambar ilustrasi: Biasanya pesan error muncul warna merah di bawah kolom input)
            
        else:
            print("❌ TEST FAILED: Pesan error tidak sesuai atau tidak muncul.")

    except Exception as e:
        print("❌ TEST FAILED (System Error):", e)

    finally:
        print("\nMenutup browser dalam 5 detik...")
        time.sleep(5)
        driver.quit()
        print("🧹 Sesi pengujian ditutup")


if __name__ == "__main__":
    run_tc010_password_confirmation_local()